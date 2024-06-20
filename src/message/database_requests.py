from sqlalchemy import select,insert,text
from .models import UserORM,ChatUsersORM,ChatORM,MessageORM,ClientServerORM
from src.database import session_factory
from .schemes import ChatDTO,UserDTO,MessageDTO,ChatUsersDTO,ClientServerDTO

async def client_server_registration(url:str)->ClientServerDTO:
    """
    Регестрирует новую платформу.
    Возаращяет: ClientServerDTO(id,url).
    """
    async with session_factory() as session:
        res = await session.execute(insert(ClientServerORM).return_defaults(ClientServerORM).values(url=url))
        await session.commit()
        return ClientServerDTO(id=res.inserted_primary_key[0],url = url)

async def create_user(client_server_id:int)->UserDTO:
    """
    Регестрирует нового пользователя с клиентсеого сервера, используется полноценными клиентами.
    Возаращяет: UserDTO(id,client_server).
    """
    async with session_factory() as session:
        res = await session.execute(insert(UserORM).return_defaults(UserORM).values(client_server_id=client_server_id))
        await session.commit()
        return UserDTO(id=res.inserted_primary_key[0],client_server_id = client_server_id)
    
async def create_chat(name:str)->ChatDTO:
    """
    Создаёт новый пустой чат.
    Возвращяет: ChatDTO(id,name).
    """
    async with session_factory() as session:
        res = await session.execute(insert(ChatORM).return_defaults(ChatORM).values(name=name))
        await session.commit()
        return ChatDTO(id=res.inserted_primary_key[0],name=name)

async def add_user_to_chat(user_id:int,chat_id:int)->None:
    """
    Добавлет ползователя к указаному чату.
    """
    async with session_factory() as session:
        session.add(ChatUsersORM(user_id=user_id,chat_id=chat_id))
        await session.commit()

async def create_user_from_bot(client_server_id:int,name_chat:str)->ChatUsersDTO:
    """
    !!!Следует переписаь!!!
    Регестрирует новго пользователя и саздаёт новый чат в который его добавляет.
    Возвращяет: ChatUsersDTO(user.id,chat.id).
    """
    async with session_factory() as session:
        res = await session.execute(text(
            """
            WITH user_id AS(INSERT INTO public.user (client_server_id) VALUES (:client_server_id) RETURNING public.user.id),chat_id AS(INSERT INTO public.chat (name) VALUES (:name_chat) RETURNING public.chat.id)
            INSERT INTO public.chatusers (user_id,chat_id) VALUES((SELECT * FROM user_id),(SELECT * FROM chat_id)) RETURNING user_id,chat_id
            """
        ),{"client_server_id":client_server_id,"name_chat":name_chat})
        result=res.all()
        await session.commit()
        return ChatUsersDTO(user_id=result[0][0],chat_id=result[0][1])



# async def send_messge_to_chat()->MessageDTO:
#     async with session_factory() as session:
#         res = await session.execute(insert(MessageORM).return_defaults(MessageORM).values(from_table=from_table))
#         await session.commit()
#         return ChatUsersDTO(id=res.inserted_primary_key[0],from_table = from_table)
