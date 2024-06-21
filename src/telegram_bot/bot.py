import asyncio
from typing import Dict

import aiohttp
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters.command import Command
from aiogram.types import Message

from pydantic import BaseModel, Field, HttpUrl

from config_reader import config
from src.app.schemes import MessageDTO


class CommandUrlDTO(BaseModel):
    command: str = Field(..., description="Команда бота")
    url: HttpUrl = Field(..., description="Нужный endpoint для запроса")


# Определение команд и URL в виде списка Pydantic-моделей
COMMAND_URLS = [
    CommandUrlDTO(command='/register_server', url='http://127.0.0.1:8000/platform_registration'),
    CommandUrlDTO(command='/register_user', url='http://127.0.0.1:8000/create_user_from_bot')
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


@register_router.message(Command("register_server"))
async def register_server_command(message: Message):
    """
        Обрабатывает команду /register_server
    """
    print(message.text)
    command_url = next((cmd.url for cmd in COMMAND_URLS if cmd.command == '/register_server'), None)
    print(command_url)
    await forward_message_to_fastapi(message.text, command_url)
    await message.answer("registration")


@register_user_router.message(Command('register_user'))
async def register_user_command(message: Message):
    """
        Обрабатывает команду /register_user
    """
    print(message.text)
    command_url = next((cmd.url for cmd in COMMAND_URLS if cmd.command == '/register_user'), None)
    print(command_url)
    await forward_message_to_fastapi(message.text, command_url)
    await message.answer("register user")


@text_router.message(F)
async def message_with_text(message: Message):
    print(message.text)
    await message.answer("Это текстовое сообщение")


async def forward_message_to_fastapi(message: MessageDTO, command_url: HttpUrl) -> bool:
    """
        Функция, отправляющая запрос в FastAPI
        :params message: MessageDTO, command: CommandUrlDTO
        :returns: bool
    """
    params = {"platform_name": config.platform_name, "message": message}
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(command_url.__str__(), params=params, headers=headers) as response:
                response.raise_for_status()
                print(await response.text())
                return True
        except aiohttp.ClientResponseError as e:
            print(f"Error: {e}")
        except aiohttp.ClientError as e:
            print(f"Error: {e}")


async def start_bot(bot_instance: Bot):
    dp.include_routers(register_router, register_user_router, text_router)
    await dp.start_polling(bot_instance)


if __name__ == '__main__':
    asyncio.run(start_bot(bot))
