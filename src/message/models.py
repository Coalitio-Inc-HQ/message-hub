from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,CheckConstraint,text,ForeignKey,JSON

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__="user"
    id: Mapped[int]=mapped_column(primary_key=True)
    from_table: Mapped[int]=mapped_column(len=10)

class ChatORM(Base):
    __tablename__="chat"
    id:Mapped[int]=mapped_column(primary_key=True)
    users: Mapped[JSON]

class MessageORM(Base):
    __tablename__="message"
    chat_id:Mapped[int]
    