from src.database import session_factory
from sqlalchemy import text,insert,delete
from src.message.models import ChatORM, UserORM,MessageORM,ClientServerORM,ChatUsersORM
from src.telegram_bot.models import TelegramUserORM

from src.telegram_bot.database_requests import put_to_database_telegramuser,get_telegramuser_by_user_id_from_database,get_telegramuser_by_telegram_id_from_database
from src.message.database_requests import client_server_registration,create_user,create_chat,add_user_to_chat,create_user_from_bot

import asyncio

async def clear_db():
    """
    Отчистка бд перед тестированием.
    """
    async with session_factory()as session:
        await session.execute(delete(TelegramUserORM))

        await session.execute(delete(MessageORM))
        await session.execute(delete(ChatUsersORM))
        await session.execute(delete(ChatORM))
        await session.execute(delete(UserORM))
        await session.execute(delete(ClientServerORM))
        
        await session.commit()

async def test_database_requests_from_tele_bot():
    """
    Тестирование БД telegram_bbot.
    """
    print(await put_to_database_telegramuser(1,1,1))
    print(await get_telegramuser_by_user_id_from_database(1))
    print(await get_telegramuser_by_telegram_id_from_database(1))

async def test_database_requests_from_massage():
    """
    Тестирование БД main.
    """
    client_server = await client_server_registration(url="http://127.0.0.1:8000")
    print(client_server)
    user=await create_user(client_server_id=client_server.id)
    print(user)
    chat=await create_chat(name="chat")
    print(chat)
    await add_user_to_chat(user_id=user.id,chat_id=chat.id)
    user_bot = await create_user_from_bot(client_server_id=client_server.id,name_chat="aaaaaaaaa...")
    print(user_bot)

async def test():
    """
    Тестирование.
    """
    await clear_db()
    await test_database_requests_from_tele_bot()
    await test_database_requests_from_massage()

asyncio.run(test())

