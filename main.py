import asyncio

from deriv_bot.config import load_config
from deriv_bot.deriv_api import DerivClient
from deriv_bot.bot import DerivOptionsBot


def main():
    config = load_config()
    client = DerivClient(config)
    bot = DerivOptionsBot(config, client)
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
