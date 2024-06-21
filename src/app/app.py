from enum import Enum
from fastapi import FastAPI, HTTPException
from .database_requests import *

app = FastAPI()


class PlatformsEnum(Enum):
    telegram = "telegram"


def check_platform(func):
    async def inner(platform_name: str):
        if platform_name in [platform.value for platform in PlatformsEnum]:
            return await func(platform_name)
        else:
            raise HTTPException(
                status_code=400, detail="Invalid platform name")
    return inner


@app.post("/platform_registration")
@check_platform
async def register_platform(platform_name: str):
    plaform = await platform_registration(f"{platform_name}")
    print(plaform.__dict__)
    return {"status": "ok"}


@app.post("/create_user_from_bot")
@check_platform
async def create_user_by_bot(platform_name: str):
    platform_id = await get_platform_id_by_platform_name(platform_name)
    user = await create_user_from_bot(platform_id)
    print(user.__dict__)
    return {"status": "ok"}
