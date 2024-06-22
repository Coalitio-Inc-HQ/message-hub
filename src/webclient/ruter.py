from fastapi import APIRouter
from src.app.database_requests import *
from pydantic import Field

router = APIRouter()

@router.post("/create_user")
async def create_user_by_web():
    user = await create_user()
    return user

@router.post("/create_menedger_user")
async def create_menedger_user_by_web():
    user = await create_menedger_user()
    return user

@router.post("/get_chats_by_user")
async def get_chats_by_user_by_web(user_id:int):
    """
    При введени аутнетификации изменить.
    """
    chats = await get_chats_by_user(user_id=user_id)
    return chats

# @router.post("/get_messges_from_chat")
# async def get_messges_from_chat_by_web():
#     chats = await get_messges_from_chat()
#     return chats

@router.post("/create_chat")
async def create_chat_by_web(user_id:int,name:str=Field(min_length=256)):
    """
    При введени аутнетификации изменить.
    """
    chat = await create_chat()
    return chat

@router.post("/add_user_to_chat")
async def add_user_to_chat_by_web(user_id:int,chat_id:int):
    """
    При введени аутнетификации изменить.
    """
    await add_user_to_chat(user_id=user_id,chat_id=chat_id)
    return  {"status": "ok"}

# @router.post("/send_messge")
# async def send_messge_by_web(message:MessageDTO):
#     """
#     При введени аутнетификации изменить.
#     """
#     chat = await save_messege(message=message)
#     return chat

