#!/bin/bash
alembic upgrade head 
python run_fastapi.py & python run_telegram_bot.py