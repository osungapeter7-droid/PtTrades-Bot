# Deriv Options Automated Bot

This repository contains a lightweight example of an automated Deriv options trading bot.

It is designed as a starting point for experimenting with:

- Deriv websocket connection
- Live tick subscription
- Momentum-based option signal generation
- Automatic trade execution for `CALL` or `PUT` contracts

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

4. Fill in your Deriv credentials:

   ```env
   DERIV_TOKEN=your_deriv_api_token
   DERIV_SYMBOL=R_100
   DERIV_AMOUNT=1
   DERIV_DURATION=5
   DERIV_DURATION_UNIT=m
   DERIV_LOOKBACK=20
   DERIV_THRESHOLD=0.8
   ```

5. Run the bot:

   ```bash
   python main.py
   ```

## Project structure

- `main.py` — entry point
- `deriv_bot/config.py` — environment configuration and validation
- `deriv_bot/deriv_api.py` — websocket client and simple momentum strategy
- `deriv_bot/bot.py` — bot runner

## Notes

The included strategy is intentionally small and easy to modify. You can replace the momentum logic with:

- RSI-based entries
- price action breakouts
- volatility filtering
- multiple-symbol scheduling

If you want, I can next turn this into a more production-ready bot with:

- signal logging to CSV / SQLite
- risk management and stop-loss controls
- custom command-line options
- backtesting support
- Telegram or email alerts
