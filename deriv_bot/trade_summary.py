import csv
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def summarize_trades(file_path: str = "trades.csv", limit: int = 10) -> Dict[str, Any]:
    path = Path(file_path)
    summary: Dict[str, Any] = {
        "file": str(path),
        "total_trades": 0,
        "signals": {},
        "statuses": {},
        "recent": [],
    }

    if not path.exists():
        summary["message"] = "No trade log file found yet."
        return summary

    signals = Counter()
    statuses = Counter()
    recent: List[Dict[str, Any]] = []

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            summary["total_trades"] += 1
            signal = (row.get("signal") or "").strip()
            status = (row.get("status") or "").strip()
            if signal:
                signals[signal] += 1
            if status:
                statuses[status] += 1

            recent.append(
                {
                    "timestamp": row.get("timestamp", ""),
                    "signal": signal,
                    "status": status,
                    "price": row.get("price", ""),
                    "amount": row.get("amount", ""),
                    "duration": row.get("duration", ""),
                    "duration_unit": row.get("duration_unit", ""),
                    "notes": row.get("notes", ""),
                }
            )

    summary["signals"] = dict(sorted(signals.items()))
    summary["statuses"] = dict(sorted(statuses.items()))
    summary["recent"] = recent[-limit:]
    return summary


def print_trade_summary(file_path: str = "trades.csv", limit: int = 10) -> None:
    summary = summarize_trades(file_path=file_path, limit=limit)
    print(f"Trade summary for: {summary['file']}")
    print(f"Total entries: {summary['total_trades']}")
    print("Signals:")
    if summary["signals"]:
        for signal, count in summary["signals"].items():
            print(f"  - {signal}: {count}")
    else:
        print("  - none")

    print("Statuses:")
    if summary["statuses"]:
        for status, count in summary["statuses"].items():
            print(f"  - {status}: {count}")
    else:
        print("  - none")

    print(f"Recent trades (up to {len(summary['recent'])}):")
    if summary["recent"]:
        for item in summary["recent"]:
            print(
                f"  - {item['timestamp']} | signal={item['signal']} | status={item['status']} | "
                f"price={item['price']} | amount={item['amount']} | notes={item['notes']}"
            )
    else:
        print("  - no recent trades")
