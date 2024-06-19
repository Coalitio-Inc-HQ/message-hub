from sqlalchemy import select,insert
from .models import UserORM,ChatUsersORM,ChatORM,MessageORM
from src.database import session_factory
from .schemes import ChatDTO,UserDTO,MessageDTO,ChatUsersDTO

async def create_user(from_table:str)->UserDTO:
    async with session_factory() as session:
        res = await session.execute(insert(UserORM).return_defaults(UserORM).values(from_table=from_table))
        await session.commit()
        return UserDTO(id=res.inserted_primary_key[0],from_table = from_table)
    
async def create_chat(name:str)->ChatDTO:
    async with session_factory() as session:
        res = await session.execute(insert(ChatORM).return_defaults(ChatORM).values(name=name))
        await session.commit()
        return ChatDTO(id=res.inserted_primary_key[0],name=name)

async def add_user_to_chat(user_id:int,chat_id:int)->None:
    async with session_factory() as session:
        session.add(ChatUsersORM(user_id=user_id,chat_id=chat_id))
        await session.commit()

# async def send_messge_to_chat()->MessageDTO:
#     async with session_factory() as session:
#         res = await session.execute(insert(MessageORM).return_defaults(MessageORM).values(from_table=from_table))
#         await session.commit()
#         return ChatUsersDTO(id=res.inserted_primary_key[0],from_table = from_table)
