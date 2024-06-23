import asyncio
from typing import Dict

import aiohttp
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters.command import Command
from aiogram.types import Message

from pydantic import BaseModel, Field, HttpUrl

from .config_reader import config
from src.app.schemes import *

from src.telegram_bot.database_requests import *

import datetime

class CommandUrlDTO(BaseModel):
    command: str = Field(..., description="Команда бота")
    url: HttpUrl = Field(..., description="Нужный endpoint для запроса")


# Определение команд и URL в виде списка Pydantic-моделей
COMMAND_URLS = [
    CommandUrlDTO(command='/register_user',
                  url='http://127.0.0.1:8000/bot/create_user_from_bot'),
    CommandUrlDTO(command='/send_messge',
                  url='http://127.0.0.1:8000/bot/send_messge')
]

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.telegram_bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher()

# Роутеры
register_router = Router()
register_user_router = Router()
text_router = Router()



@register_user_router.message(Command('start')) 
async def register_user_command(message: Message):
    """
        Обрабатывает команду /register_user
    """
    command_url = next(
        (cmd.url for cmd in COMMAND_URLS if cmd.command == '/register_user'), None)

    user = None

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(command_url.__str__(), params={"platform_name": "telegram"}, headers={"Content-Type": "application/json"}) as response:
                response.raise_for_status()
                user = ChatUsersDTO.model_validate_json(await response.text())
        except aiohttp.ClientResponseError as e:
            print(f"Error: {e}")
        except aiohttp.ClientError as e:
            print(f"Error: {e}")

    if user:
        await put_to_database_telegramuser(message.chat.id, user.user_id, user.chat_id)

    await message.answer("register user")


@text_router.message(F)
async def message_with_text(message: Message):
    command_url = next(
        (cmd.url for cmd in COMMAND_URLS if cmd.command == '/send_messge'), None)

    db_data = await get_telegramuser_by_telegram_id_from_database(telegram_user_id=message.chat.id)

    created_at = message.date.astimezone(
        datetime.timezone.utc)
    edit_at = message.date.astimezone(datetime.timezone.utc)

    print(created_at)
    print(date_time_convert(created_at))

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(command_url.__str__(), json={"chat_id": db_data.chat_id.__str__(), "creator": db_data.user_id.__str__(), "created_at": date_time_convert(created_at.replace(tzinfo=None)), "edit_at": date_time_convert( edit_at.replace(tzinfo=None)), "text_message": message.text}, headers={"Content-Type": "application/json"}) as response:
                response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            print(f"Error: {e}")
        except aiohttp.ClientError as e:
            print(f"Error: {e}")

def date_time_convert(t:datetime.datetime)->str:
    return f"{t.year:04}-{t.month:02}-{t.day:02}T{t.hour:02}:{t.minute:02}:{t.second:02}.{t.microsecond:03}Z"

async def start_bot(bot_instance: Bot):
    dp.include_routers(register_router, register_user_router, text_router)
    await dp.start_polling(bot_instance)

async def sent_message_to_user(user_id:int,message:MessageDTO):
    db_data = await get_telegramuser_by_user_id_from_database(user_id=user_id)
    await bot.send_message(db_data.telegram_user_id, message.text_message)
