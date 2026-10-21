import csv
from datetime import datetime, timezone
from pathlib import Path


class TradeLogger:
    def __init__(self, file_path: str = "trades.csv"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text(
                "timestamp,signal,symbol,price,amount,duration,duration_unit,status,notes\n",
                encoding="utf-8",
            )

    def log_trade(
        self,
        signal: str,
        symbol: str,
        price: float,
        amount: float,
        duration: int,
        duration_unit: str,
        status: str,
        notes: str = "",
    ) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with self.file_path.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    timestamp,
                    signal,
                    symbol,
                    price,
                    amount,
                    duration,
                    duration_unit,
                    status,
                    notes,
                ]
            )
