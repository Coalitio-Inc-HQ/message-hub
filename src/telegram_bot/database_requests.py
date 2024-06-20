from sqlalchemy import select
from models import TelegramUserORM
from src.database import session_factory
from schemes import TelegramUserDTO


async def put_to_database_telegram_user(telegram_user_id: int, user_id: int, chat_id: int):
    async with session_factory() as session:
        session.add(TelegramUserORM(telegram_user_id=telegram_user_id, user_id=user_id, chat_id=chat_id))
        await session.commit()


async def get_telegram_user_by_user_id_from_database(user_id: int) -> TelegramUserDTO:
    async with session_factory() as session:
        res = await session.execute(select(TelegramUserORM).where(TelegramUserORM.user_id == user_id))
        # print(res.scalar_one().__dict__)
        return TelegramUserDTO.model_validate(res.scalar_one(), from_attributes=True)


async def get_telegram_user_by_telegram_id_from_database(telegram_user_id: int) -> TelegramUserORM:
    async with session_factory() as session:
        res = await session.execute(select(TelegramUserORM).where(TelegramUserORM.telegram_user_id == telegram_user_id))
        return TelegramUserDTO.model_validate(res.scalar_one(), from_attributes=True)
