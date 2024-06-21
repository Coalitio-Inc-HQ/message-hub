from src.database import session_factory
from sqlalchemy import text, insert, delete, select, cte
from src.app.models import ChatORM, UserORM, MessageORM, PlatformORM, ChatUsersORM
from src.telegram_bot.models import TelegramUserORM

from src.telegram_bot.database_requests import put_to_database_telegramuser, get_telegramuser_by_user_id_from_database, get_telegramuser_by_telegram_id_from_database
from src.app.database_requests import platform_registration, create_user, create_chat, add_user_to_chat, create_user_from_bot

import asyncio

name = 'sad'
user_id = 1

cte_ = insert(ChatORM).returning(ChatORM.creator.label("user_id"),
                                 ChatORM.id.label("chat_id")).values(name=name, creator=user_id).cte()
select_cte = select(cte_)
stmt = insert(ChatUsersORM).from_select(select=select_cte, names=[
    "user_id", "chat_id"]).returning(ChatUsersORM.user_id, ChatUsersORM.chat_id)
