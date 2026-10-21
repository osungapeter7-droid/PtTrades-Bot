import asyncio
from collections import deque
from typing import Deque, List, Optional


class MomentumStrategy:
    def __init__(self, lookback: int = 20, threshold: float = 0.8):
        self.lookback = lookback
        self.threshold = threshold

    def evaluate(self, prices: List[float]) -> Optional[str]:
        if len(prices) < self.lookback:
            return None

        recent = prices[-self.lookback:]
        average = sum(recent) / len(recent)
        current = recent[-1]

        if average == 0:
            return None

        momentum = (current - average) / average

        if momentum > self.threshold:
            return "CALL"
        if momentum < -self.threshold:
            return "PUT"
        return None


class DerivOptionsBot:
    def __init__(self, config, client):
        self.config = config
        self.client = client
        self.strategy = MomentumStrategy(
            lookback=config.lookback,
            threshold=config.threshold,
        )
        self.prices: Deque[float] = deque(maxlen=max(config.lookback, 10))

    async def run(self):
        print(f"Connecting to Deriv: {self.config.deriv_api_url}")
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
                signal = self.strategy.evaluate(list(self.prices))

                if signal is not None:
                    print(
                        f"Signal detected: {signal} @ price={tick_value:.4f} | "
                        f"lookback={len(self.prices)}"
                    )
                    trade_result = await self.client.buy_contract(
                        contract_type=signal,
                        symbol=self.config.symbol,
                        amount=self.config.amount,
                        duration=self.config.duration,
                        duration_unit=self.config.duration_unit,
                    )
                    print(f"Trade payload: {trade_result}")
                    await asyncio.sleep(self.config.trade_pause_seconds)

                await asyncio.sleep(0.5)
        finally:
            listen_task.cancel()
            await self.client.close()
