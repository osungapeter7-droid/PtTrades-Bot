import argparse
import asyncio

from deriv_bot.config import load_config
from deriv_bot.bot import DerivOptionsBot
from deriv_bot.deriv_api import DerivClient
from deriv_bot.trade_summary import print_trade_summary


def parse_args():
    parser = argparse.ArgumentParser(description="Deriv options bot")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show the latest trade log summary instead of running the bot.",
    )
    parser.add_argument(
        "--log-file",
        default="trades.csv",
        help="CSV trade log file to read when using --summary.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.summary:
        print_trade_summary(args.log_file)
        return

    config = load_config()
    client = DerivClient(config)
    bot = DerivOptionsBot(config, client)
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
