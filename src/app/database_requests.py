from sqlalchemy import select, insert, text, func, bindparam, update
from .models import UserORM, ChatUsersORM, ChatORM, MessageORM, ManadgerORM, PlatformORM
from src.database import session_factory
from .schemes import ChatDTO, UserDTO, MessageDTO, ChatUsersDTO, ClientServerDTO, ManadgerDTO, PlatformDTO

import datetime


async def platform_registration(name: str) -> PlatformDTO:
    """
    Регестрирует новую платформу.
    Возаращяет: PlatformDTO(id,name).
    """
    async with session_factory() as session:
        res = await session.execute(insert(PlatformORM).returning(PlatformORM.id).values(name=name))
        await session.commit()
        return PlatformDTO(id=res.scalar(), name=name)


async def create_user(platform_id: int) -> UserDTO:
    """
    Регестрирует нового пользователя с клиентсеого сервера, используется полноценными клиентами.
    Возаращяет: UserDTO(id,platform_id).
    """
    async with session_factory() as session:
        res = await session.execute(insert(UserORM).returning(UserORM.id).values(platform_id=platform_id))
        await session.commit()
        return UserDTO(id=res.scalar(), platform_id=platform_id)


async def create_chat(user_id: int, name: str) -> ChatDTO:
    """
    Создаёт новый пустой чат и добавляет туда пользователя.
    Возвращяет: ChatDTO(id,name,creator).
    """
    async with session_factory() as session:
        cte_ = insert(ChatORM).returning(ChatORM.creator.label(
            "user_id"), ChatORM.id.label("chat_id")).values(name=name, creator=user_id).cte()
        select_cte = select(cte_)
        stmt = insert(ChatUsersORM).from_select(select=select_cte, names=[
            "user_id", "chat_id"]).returning(ChatUsersORM.chat_id)

        res = await session.execute(stmt)
        await session.commit()
        return ChatDTO(id=res.scalar(), name=name, creator=user_id)


async def add_user_to_chat(user_id: int, chat_id: int) -> ChatUsersDTO:
    """
    Добавлет ползователя к указаному чату.
    Возвращяет: ChatUsersDTO(user.id,chat.id).
    """
    async with session_factory() as session:
        session.add(ChatUsersORM(user_id=user_id, chat_id=chat_id))
        await session.commit()
        return ChatUsersDTO(user_id=user_id, chat_id=chat_id)


async def save_messege(message: MessageDTO) -> MessageDTO:
    """
    Сохраняет сообщение в БД.
    Возвращяет: MessageDTO(id,chat_id,creator,created_at,edit_at,text_message).
    """
    async with session_factory() as session:
        message.created_at = message.created_at.astimezone(
            datetime.timezone.utc)
        message.edit_at = message.edit_at.astimezone(datetime.timezone.utc)
        res = await session.execute(insert(MessageORM).returning(MessageORM.id).values(chat_id=message.chat_id, creator=message.creator, created_at=message.created_at.replace(tzinfo=None), edit_at=message.edit_at.replace(tzinfo=None), text_message=message.text_message))
        await session.commit()
        result = message.copy()
        result.id = res.scalar()
        return result


async def get_chats_by_user(user_id: int) -> list[ChatDTO]:
    """
    Находит все чаты в которых состоит пользователь.
    Возвращяет: list[ChatDTO(id,name,creator)].
    """
    async with session_factory() as session:
        cte = select(ChatUsersORM.chat_id).where(
            ChatUsersORM.user_id == user_id).subquery()
        sel = select(ChatORM).where(ChatORM.id.in_(cte))
        res_orm = (await session.execute(sel)).scalars().all()
        res_dto = [ChatDTO.model_validate(
            row, from_attributes=True) for row in res_orm]
        return res_dto


async def get_messges_from_chat(chat_id: int, count) -> list[MessageDTO]:
    """
    Возращяет count последних сообщений из чата, отсортированных по датте.
    Возвращяет: list[MessageDTO(id,chat_id,creator,created_at,edit_at,text_message)].
    """
    async with session_factory() as session:
        res = await session.execute(select(MessageORM).where(MessageORM.chat_id == chat_id).order_by(MessageORM.created_at.desc()).limit(count))
        res_orm = res.scalars().all()
        res_dto = [MessageDTO.model_validate(
            row, from_attributes=True) for row in res_orm[::-1]]
        return res_dto


async def get_platform_by_platform_name(platform_name: str) -> PlatformDTO:
    """
    Получает платформу по её названию.
    Возращяет PlatformDTO(id, name).
    """
    async with session_factory() as session:
        res = await session.execute(select(PlatformORM).where(PlatformORM.name == platform_name))
        sc_res = res.scalar_one_or_none()
        if sc_res:
            return PlatformDTO.model_validate(sc_res, from_attributes=True)
        else:
            return None


async def get_all_platform() -> list[PlatformDTO]:
    """
    Получает все платформы.
    Возращяет PlatformDTO(id, name).
    """
    async with session_factory() as session:
        res = await session.execute(select(PlatformORM))
        res_orm = res.scalars()
        res_dto = [PlatformDTO.model_validate(
            row, from_attributes=True) for row in res_orm]
        return res_dto


async def get_users_by_chat_id(chat_id: int) -> list[UserDTO]:
    """
    Получает всех пользователей чата.
    Возаращяет: [UserDTO(id,platform_id)].
    """
    async with session_factory() as session:
        res = await session.execute(select(UserORM).join(ChatUsersORM).where(ChatUsersORM.chat_id == chat_id))
        res_orm = res.scalars()
        res_dto = [UserDTO.model_validate(
            row, from_attributes=True) for row in res_orm]
        return res_dto

async def create_menedger_user(platform_id: int) -> UserDTO:
    """
    Регестрирует нового пользователя с клиентсеого сервера, и добавлет его в списк распределения ботов.
    Возаращяет: UserDTO(id,platform_id).
    """
    async with session_factory() as session:
        cte = insert(UserORM).returning(UserORM.id.label("user_id")).values(platform_id=platform_id).cte()
        cte_sel = select(cte,0)
        stmt = insert(ManadgerORM).from_select(select=cte_sel,names=["user_id","number_of_linked_bots"]).returning(ManadgerORM.user_id)
        res = await session.execute(stmt)
        await session.commit()
        return UserDTO(id=res.scalar(),  platform_id=platform_id)

"""
temp
"""

async def create_user_from_bot(platform_id: int) -> ChatUsersDTO:
    """
    Регестрирует новго пользователя и саздаёт новый чат в который его добавляет.
    Возвращяет: ChatUsersDTO(user.id,chat.id).
    """
    async with session_factory() as session:
        user_id = (await session.execute(insert(UserORM).returning(UserORM.id).values(platform_id=platform_id))).scalar()
        min_bots = select(
            func.min(ManadgerORM.number_of_linked_bots)).scalar_subquery()
        manadger = (await session.execute(select(ManadgerORM).where(ManadgerORM.number_of_linked_bots == min_bots))).scalar()
        chat_id = (await session.execute(insert(ChatORM).returning(ChatORM.id).values(name=str(user_id), creator=manadger.user_id))).scalar()
        manadger.number_of_linked_bots = manadger.number_of_linked_bots+1
        await session.execute(insert(ChatUsersORM), [{"user_id": user_id, "chat_id": chat_id}, {"user_id": manadger.user_id, "chat_id": chat_id}])

        await session.commit()
        return ChatUsersDTO(user_id=user_id, chat_id=chat_id)
