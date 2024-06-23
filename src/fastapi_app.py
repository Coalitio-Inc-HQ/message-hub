from src.telegram_bot.bot import bot
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends,APIRouter
from src.app.database_requests import *
from pydantic import BaseModel

from .settings import settings

from contextlib import asynccontextmanager

from src.telegram_bot.bot import sent_message_to_user as telegram_sent_message_to_user
"""
Обслуживаемые платформы.
"""
PLATFORMS_CONF = [{"name": "telegram", "send_func": telegram_sent_message_to_user}
                  , {"name": "sdhf", "send_func": lambda user_id,message: print(user_id)}]



async def initplatforms(platforms: list) -> None:
    """
    Инициализация платформ.
    Если её нету то добавление в бд.
    """
    db_platforms = await get_all_platform()
    for platform in platforms:
        fundplatform = [
            obj for obj in db_platforms if obj.name == platform["name"]]
        if len(fundplatform) > 0:
            platform["id"] = fundplatform[0].id
        else:
            pl = await platform_registration(platform["name"])
            platform["id"] = pl.id


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Позволяет выпольнить код до запуска серваера и после его остановки.
    """
    await initplatforms(PLATFORMS_CONF)
    yield

app = FastAPI(lifespan=lifespan)

async def check_platform(platform_name: str) -> PlatformDTO:
    """
    Проверяем существование платформы.
    """
    p_dto = await get_platform_by_platform_name(platform_name=platform_name)
    if p_dto:
        return p_dto
    else:
        raise HTTPException(status_code=400, detail="Platform not fund")


@app.post("/bot/create_user_from_bot")
async def create_user_by_bot(platform: PlatformDTO = Depends(check_platform)):
    """
    Создаёт нового пользователя для бота.
    """
    user = await create_user_from_bot(platform_id=platform.id)
    return user


@app.post("/bot/send_messge")
async def send_messge_from_bot(message: MessageDTO):
    """
    Принемает сообщение отправленное с бота.
    """
    message = await save_messege(message=message)
    await sending_messages(message=message)
    return {"status": "ok"}


async def sending_messages(message: MessageDTO):
    users = await get_users_by_chat_id(message.chat_id)
    for user in users:
        if (not user.id == message.creator) or settings.CHAT_ECHO:
            for plat in PLATFORMS_CONF:
                if plat["id"] == user.platform_id:
                    await plat["send_func"](user.id,message)


