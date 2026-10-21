# Deriv Options Automated Bot

This repository contains a lightweight example of an automated Deriv options trading bot.

It is designed as a starting point for experimenting with:

- Deriv websocket connection
- Live tick subscription
- Momentum-based option signal generation
- Automatic trade execution for `CALL` or `PUT` contracts
- Risk controls and trade logging

Important:

- This project is for educational and research use only.
- Deriv trading involves real financial risk.
- Never run the bot with funds you cannot afford to lose.
- Make sure you understand the market and the Deriv API before using it in production.

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the sample environment file:

   ```bash
   cp .env.example .env
   ```

4. Fill in your Deriv credentials and risk settings:

   ```env
   DERIV_TOKEN=your_deriv_api_token
   DERIV_SYMBOL=R_100
   DERIV_AMOUNT=1
   DERIV_DURATION=5
   DERIV_DURATION_UNIT=m
   DERIV_LOOKBACK=20
   DERIV_THRESHOLD=0.8
   DERIV_MAX_TRADE_AMOUNT=1
   DERIV_MAX_DAILY_LOSS=50
   DERIV_MAX_TRADES_PER_DAY=10
   DERIV_COOLDOWN_SECONDS=30
   DERIV_TRADE_LOG_PATH=trades.csv
   ```

5. Run the bot:

   ```bash
   python main.py
   ```

## Project structure

- `main.py` — entry point
- `deriv_bot/config.py` — environment configuration and validation
- `deriv_bot/logger.py` — CSV trade logging utility
- `deriv_bot/deriv_api.py` — websocket client
- `deriv_bot/bot.py` — trading strategy, risk management, and bot loop

## Risk controls included

The starter bot now includes:

- `max_trade_amount` limit
- `max_daily_loss` limit
- `max_trades_per_day` cap
- `cooldown_seconds` between trades
- `trade_log_path` CSV logging

These are basic local controls and are not a substitute for proper account risk management.
