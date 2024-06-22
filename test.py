from src.database import session_factory
from sqlalchemy import text, insert, delete
from src.app.models import ChatORM, UserORM, MessageORM, ChatUsersORM, PlatformORM, ManadgerORM
from src.telegram_bot.models import TelegramUserORM
from src.app.schemes import MessageDTO

from src.telegram_bot.database_requests import *
from src.app.database_requests import *

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
    print("platform_registration")
    platform = await platform_registration("telegram")
    print(platform)

    print("create_user")
    user = await create_user(platform_id=platform.id)
    print(user)

    print("create_chat")
    chat = await create_chat(user_id=user.id, name="chat")
    print(chat)

    print("create_user")
    user1 = await create_user(platform_id=platform.id)
    print(user1)

    print("add_user_to_chat")
    chatusers = await add_user_to_chat(user_id=user1.id, chat_id=chat.id)
    print(chatusers)

    print("save_messege")
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="Hello!"))
    print(seved_msg)

    print("get_chats_by_user")
    chats = await get_chats_by_user(user_id=user1.id)
    print(chats)

    print("get_messges_from_chat")
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="1!"))
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="2!"))
    seved_msg = await save_messege(MessageDTO(id=None, chat_id=chat.id, creator=user.id, created_at=datetime.now(), edit_at=datetime.now(), text_message="3!"))
    messges = await get_messges_from_chat(chat_id=chat.id, count=10)
    for msg in messges:
        print(msg)
    
    print("create_menedger_user")
    menedger = await create_menedger_user(platform_id=platform.id)
    print(menedger)

    print("create_user_from_bot")
    user_bot = await create_user_from_bot(platform_id=platform.id)
    print(user_bot)

    print("get_platform_by_platform_name")
    platform = await get_platform_by_platform_name(platform.name)
    print(platform)

    print("get_platform_by_platform_name")
    platform1 = await get_platform_by_platform_name("asdasd")
    print(platform1)

    print("get_all_platform")
    platforms = await get_all_platform()
    for row in platforms:
        print(row)
    
    print("get_users_by_chat_id")
    users_from_chat = await get_users_by_chat_id(chat_id=chat.id)
    for row in users_from_chat:
        print(row)


async def test():
    """
    Тестирование.
    """
    await clear_db()
    await test_database_requests_from_tele_bot()
    await test_database_requests_from_massage()

# asyncio.run(clear_db())
asyncio.run(test())
