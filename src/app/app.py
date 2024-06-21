from enum import Enum
from fastapi import FastAPI, HTTPException
from .database_requests import *

from pydantic import BaseModel

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


class PlatformsEnum(Enum):
    telegram = "telegram"


class PlatformRegistrationDTO(BaseModel):
    platform_name: str


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
async def register_platform(request: PlatformRegistrationDTO):
    platform = await platform_registration(f"{request.platform_name}")
    print(platform.__dict__)
    return {"status": "ok"}


@app.post("/create_user_from_bot")
@check_platform
async def create_user_by_bot(request: PlatformRegistrationDTO):  # пока что не работает
    platform_id = await get_platform_id_by_platform_name(request.platform_name)
    print(platform_id)
    user = await create_user_from_bot(platform_id)
    print(user.__dict__)
    return {"status": "ok"}
