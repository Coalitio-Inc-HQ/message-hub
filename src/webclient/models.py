from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Boolean,CheckConstraint,text,ForeignKey,JSON

class Base(DeclarativeBase):
    pass

class WebUserORM(Base):
    __tablename__="webuser"
    login: Mapped[str]=mapped_column(len=256)
    hash_password:Mapped[str]=mapped_column(len=1000)
    user_id: Mapped[int]=mapped_column(primary_key=True)