# Telegram CRM Bot

**Telegram CRM Bot** that collects leads, writes them to **PostgreSQL**, and sends instant **Telegram notifications** to a manager. Built with **Python**, **Flask**, **SQLAlchemy**, and **aiogram**.

## What it does
- `/start` — greets the user
- `/lead` — step-by-step lead capture (name, phone, notes)
- Saves leads to PostgreSQL
- Notifies your manager chat on every new lead
- Simple Flask web UI to add a lead manually and view a basic list

## Stack
- Python, Flask
- SQLAlchemy (PostgreSQL)
- aiogram (Telegram Bot)
- Docker + docker-compose

## Quick start (Docker)
1. Copy env and edit:
   ```bash
   cp .env.example .env
   # put your TELEGRAM_BOT_TOKEN, MANAGER_CHAT_ID, etc.
   ```
2. Run:
   ```bash
   docker compose up --build
   ```
3. Services:
   - Flask API/UI: http://localhost:8000
   - Telegram Bot: runs in a separate container (polling)
   - PostgreSQL: localhost:5432

## Local dev (without Docker)
1. Python 3.11+ recommended.
2. Create and fill `.env` based on `.env.example`.
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize DB automatically on first run.
5. Run web:
   ```bash
   python run_web.py
   ```
6. Run bot:
   ```bash
   python run_bot.py
   ```

## Environment variables
- `DATABASE_URL` — e.g. `postgresql+psycopg2://user:pass@host:5432/dbname`
- `TELEGRAM_BOT_TOKEN` — your bot token
- `MANAGER_CHAT_ID` — Telegram chat ID for manager notifications
- `FLASK_SECRET_KEY` — secret for Flask session

## Minimal admin UI
Open `http://localhost:8000` to add a lead manually and to view the list (very basic).

## Project structure
```
telegram-crm-bot/
├─ app/
│  ├─ __init__.py        # Flask factory, routes registration
│  ├─ database.py        # SQLAlchemy engine/session
│  ├─ models.py          # Lead model
│  ├─ routes.py          # Web UI & JSON endpoints
│  └─ notify.py          # Manager notifications (Telegram)
├─ bot/
│  └─ bot.py             # aiogram bot (/lead flow)
├─ run_web.py            # start Flask app
├─ run_bot.py            # start Telegram bot (polling)
├─ requirements.txt
├─ .env.example
├─ docker-compose.yml
├─ Dockerfile
└─ LICENSE
```

## Security notes
- Do not commit your `.env`.
- Restrict who knows your `MANAGER_CHAT_ID`.
- Add auth to the web UI for production.

## License
MIT © 2025 Bogdan Yatsenko

📦 About the migration This repository was migrated as part of my Portfolio Refresh. Originally developed locally; during migration I added README, .env.example, Docker/CI, and minor improvements.
