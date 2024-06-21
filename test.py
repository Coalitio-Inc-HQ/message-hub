from src.database import session_factory
from sqlalchemy import text, insert, delete
from src.message.models import ChatORM, UserORM, MessageORM, ChatUsersORM, PlatformORM, ManadgerORM
from src.telegram_bot.models import TelegramUserORM
from src.message.schemes import MessageDTO

from src.telegram_bot.database_requests import put_to_database_telegramuser, get_telegramuser_by_user_id_from_database, get_telegramuser_by_telegram_id_from_database
from src.message.database_requests import platform_registration, create_user, create_chat, add_user_to_chat, save_messege, get_chats_by_user, get_messges_from_chat, create_menedger_user, create_user_from_bot

import asyncio

from datetime import datetime


async def clear_db():
    """
    Отчистка бд перед тестированием.
    """
    async with session_factory()as session:
        await session.execute(delete(TelegramUserORM))

        await session.execute(delete(MessageORM))
        await session.execute(delete(ChatUsersORM))
        await session.execute(delete(ChatORM))
        await session.execute(delete(ManadgerORM))
        await session.execute(delete(UserORM))
        await session.execute(delete(PlatformORM))

        await session.commit()


async def test_database_requests_from_tele_bot():
    """
    Тестирование БД telegram_bbot.
    """
    print(await put_to_database_telegramuser(1, 1, 1))
    print(await get_telegramuser_by_user_id_from_database(1))
    print(await get_telegramuser_by_telegram_id_from_database(1))


async def test_database_requests_from_massage():
    """
    Тестирование БД main.
    """
    platform = await platform_registration("telegram")
    print(platform)
    user = await create_user(platform_id=platform.id)
    print(user)
    chat = await create_chat(user_id=user.id, name="chat")
    print(chat)
    user1 = await create_user(platform_id=platform.id)
    print(user1)
    chatusers = await add_user_to_chat(user_id=user1.id, chat_id=chat.id)
    print(chatusers)
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="Hello!"))
    print(seved_msg)
    chats = await get_chats_by_user(user_id=user1.id)
    print(chats)
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="1!"))
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="2!"))
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="3!"))
    messges = await get_messges_from_chat(chat_id=chat.id, count=10)
    for msg in messges:
        print(msg)
    menedger = await create_menedger_user(platform_id=platform.id)
    print(menedger)
    user_bot = await create_user_from_bot(platform_id=platform.id)
    print(user_bot)


async def test():
    """
    Тестирование.
    """
    await clear_db()
    await test_database_requests_from_tele_bot()
    await test_database_requests_from_massage()

asyncio.run(test())
