from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,CheckConstraint,text,ForeignKey,JSON
from datetime import datetime

class Base(DeclarativeBase):
    pass

class ClientServerORM(Base):
    __tablename__="client_server"
    id: Mapped[int]=mapped_column(primary_key=True)
    url:Mapped[str]

class UserORM(Base):
    __tablename__="user"
    id: Mapped[int]=mapped_column(primary_key=True)
    client_server_id: Mapped[int]=mapped_column(ForeignKey("client_server.id"))

class ChatUsersORM(Base):
    __tablename__="chatusers"
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"),primary_key=True)
    chat_id:Mapped[int]=mapped_column(ForeignKey("chat.id"),primary_key=True)

class ChatORM(Base):
    __tablename__="chat"
    id:Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(256))

class MessageORM(Base):
    __tablename__="message"
    message_id:Mapped[int] = mapped_column(primary_key=True)
    chat_id:Mapped[int] = mapped_column(ForeignKey("chat.id"))
    from_user:Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime]
    edit_at: Mapped[datetime]
    text_message:Mapped[str|None]
