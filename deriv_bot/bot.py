import asyncio
import time
from collections import deque
from datetime import datetime
from typing import Deque, List, Optional, Tuple

from deriv_bot.logger import TradeLogger


class MomentumStrategy:
    def __init__(self, lookback: int = 20, threshold: float = 0.8):
        self.lookback = lookback
        self.threshold = threshold

    def evaluate(self, prices: List[float]) -> Tuple[Optional[str], float]:
        if len(prices) < self.lookback:
            return None, 0.0

        recent = prices[-self.lookback:]
        average = sum(recent) / len(recent)
        current = recent[-1]

        if average == 0:
            return None, 0.0

        momentum = (current - average) / average
        strength = abs(momentum)

        if momentum > self.threshold:
            return "CALL", strength
        if momentum < -self.threshold:
            return "PUT", strength
        return None, strength


class DerivOptionsBot:
    def __init__(self, config, client):
        self.config = config
        self.client = client
        self.strategy = MomentumStrategy(
            lookback=config.lookback,
            threshold=config.threshold,
        )
        self.prices: Deque[float] = deque(maxlen=max(config.lookback, 10))
        self.trade_logger = TradeLogger(config.trade_log_path)
        self.trade_count_today = 0
        self.daily_loss = 0.0
        self.last_trade_time = 0.0
        self.daily_reset_time = datetime.now().date()

    def _should_reset_daily_stats(self) -> None:
        today = datetime.now().date()
        if today != self.daily_reset_time:
            self.daily_reset_time = today
            self.trade_count_today = 0
            self.daily_loss = 0.0

    def _risk_ok(self, signal_strength: float, amount: float) -> bool:
        self._should_reset_daily_stats()

        if amount > self.config.max_trade_amount:
            print(
                f"Trade blocked: amount {amount} exceeds max_trade_amount "
                f"{self.config.max_trade_amount}."
            )
            return False

        if self.trade_count_today >= self.config.max_trades_per_day:
            print(
                f"Trade blocked: reached max_trades_per_day "
                f"({self.config.max_trades_per_day})."
            )
            return False

        if self.config.max_daily_loss > 0 and self.daily_loss >= self.config.max_daily_loss:
            print(
                f"Trade blocked: daily_loss {self.daily_loss} reached max_daily_loss "
                f"{self.config.max_daily_loss}."
            )
            return False

        if signal_strength < 0.01:
            print("Trade blocked: signal strength too weak.")
            return False

        now = time.time()
        if now - self.last_trade_time < self.config.cooldown_seconds:
            print(
                f"Trade blocked: cooldown active for {self.config.cooldown_seconds} seconds."
            )
            return False

        return True

    async def run(self):
        print(f"Connecting to Deriv: {self.config.deriv_api_url}")
        if self.config.dry_run:
            print("DRY RUN MODE: no actual trades will be placed.")

        await self.client.connect()
        await self.client.subscribe_ticks(self.config.symbol)
        print(f"Listening for ticks on {self.config.symbol}")

        listen_task = asyncio.create_task(self.client.listen())
        try:
            while True:
                tick = await self.client.next_tick()
                if tick is None:
                    await asyncio.sleep(0.5)
                    continue

                price = tick.get("quote")
                if price is None:
                    price = tick.get("price")
                if price is None:
                    price = tick.get("tick")
                if price is None:
                    continue

                tick_value = float(price)
                self.prices.append(tick_value)
                signal, strength = self.strategy.evaluate(list(self.prices))

                if signal is not None:
                    trade_amount = min(self.config.amount, self.config.max_trade_amount)
                    if self._risk_ok(strength, trade_amount):
                        print(
                            f"Signal detected: {signal} @ price={tick_value:.4f} | "
                            f"strength={strength:.4f} | lookback={len(self.prices)}"
                        )

                        if self.config.dry_run:
                            self.last_trade_time = time.time()
                            self.trade_count_today += 1
                            self.trade_logger.log_trade(
                                signal=signal,
                                symbol=self.config.symbol,
                                price=tick_value,
                                amount=trade_amount,
                                duration=self.config.duration,
                                duration_unit=self.config.duration_unit,
                                status="dry-run",
                                notes=f"signal_strength={strength:.4f}",
                            )
                            print(
                                f"DRY RUN: would buy {signal} contract for {self.config.symbol} "
                                f"amount={trade_amount}, duration={self.config.duration}{self.config.duration_unit}"
                            )
                            print(
                                f"Risk state: trades_today={self.trade_count_today}, "
                                f"daily_loss={self.daily_loss}, "
                                f"cooldown={self.config.cooldown_seconds}s"
                            )
                        else:
                            trade_result = await self.client.buy_contract(
                                contract_type=signal,
                                symbol=self.config.symbol,
                                amount=trade_amount,
                                duration=self.config.duration,
                                duration_unit=self.config.duration_unit,
                            )
                            self.last_trade_time = time.time()
                            self.trade_count_today += 1
                            self.trade_logger.log_trade(
                                signal=signal,
                                symbol=self.config.symbol,
                                price=tick_value,
                                amount=trade_amount,
                                duration=self.config.duration,
                                duration_unit=self.config.duration_unit,
                                status="submitted",
                                notes=f"signal_strength={strength:.4f}",
                            )
                            print(f"Trade payload: {trade_result}")
                            print(
                                f"Risk state: trades_today={self.trade_count_today}, "
                                f"daily_loss={self.daily_loss}, "
                                f"cooldown={self.config.cooldown_seconds}s"
                            )

                        await asyncio.sleep(self.config.trade_pause_seconds)
                    else:
                        self.trade_logger.log_trade(
                            signal=signal,
                            symbol=self.config.symbol,
                            price=tick_value,
                            amount=trade_amount,
                            duration=self.config.duration,
                            duration_unit=self.config.duration_unit,
                            status="blocked",
                            notes=f"signal_strength={strength:.4f}",
                        )

                await asyncio.sleep(0.5)
        finally:
            listen_task.cancel()
            await self.client.close()
