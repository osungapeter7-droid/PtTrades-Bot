from dataclasses import dataclass, field
import os

from dotenv import load_dotenv

load_dotenv()


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


def load_config() -> BotConfig:
    config = BotConfig()
    if not config.token:
        raise RuntimeError(
            "DERIV_TOKEN is not set. Add it to your .env file or export it in the shell."
        )
    return config
