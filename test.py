from src.database import session_factory
from sqlalchemy import text

from src.telegram_bot.database_requests import put_to_database_telegram_user, get_telegram_user_by_user_id_from_database, \
    get_telegram_user_by_telegram_id_from_database
from src.message.database_requests import create_user, create_chat, add_user_to_chat

import asyncio


async def test():
    print(await get_telegram_user_by_telegram_id_from_database(20))
    # print( (await create_user("tg")))


asyncio.run(test())
