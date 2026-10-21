from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


@dataclass
class BotConfig:
    deriv_api_url: str = field(
        default_factory=lambda: os.getenv("DERIV_API_URL", "wss://ws.deriv.com/websockets/v3")
    )
    app_id: int = field(default_factory=lambda: int(os.getenv("DERIV_APP_ID", "1089")))
    token: str = field(default_factory=lambda: os.getenv("DERIV_TOKEN", ""))
    symbol: str = field(default_factory=lambda: os.getenv("DERIV_SYMBOL", "R_100"))
    amount: float = field(default_factory=lambda: float(os.getenv("DERIV_AMOUNT", "1")))
    contract_type: str = field(default_factory=lambda: os.getenv("DERIV_CONTRACT_TYPE", "CALL"))
    duration: int = field(default_factory=lambda: int(os.getenv("DERIV_DURATION", "5")))
    duration_unit: str = field(default_factory=lambda: os.getenv("DERIV_DURATION_UNIT", "m"))
    lookback: int = field(default_factory=lambda: int(os.getenv("DERIV_LOOKBACK", "20")))
    threshold: float = field(default_factory=lambda: float(os.getenv("DERIV_THRESHOLD", "0.8")))
    trade_pause_seconds: int = field(default_factory=lambda: int(os.getenv("DERIV_TRADE_PAUSE_SECONDS", "30")))
    max_trade_amount: float = field(default_factory=lambda: float(os.getenv("DERIV_MAX_TRADE_AMOUNT", "1")))
    max_daily_loss: float = field(default_factory=lambda: float(os.getenv("DERIV_MAX_DAILY_LOSS", "50")))
    max_trades_per_day: int = field(default_factory=lambda: int(os.getenv("DERIV_MAX_TRADES_PER_DAY", "10")))
    cooldown_seconds: int = field(default_factory=lambda: int(os.getenv("DERIV_COOLDOWN_SECONDS", "30")))
    trade_log_path: str = field(default_factory=lambda: os.getenv("DERIV_TRADE_LOG_PATH", "trades.csv"))
    dry_run: bool = field(default_factory=lambda: _env_bool("DERIV_DRY_RUN", True))


def load_config() -> BotConfig:
    config = BotConfig()
    if not config.token:
        raise RuntimeError(
            "DERIV_TOKEN is not set. Add it to your .env file or export it in the shell."
        )
    return config
