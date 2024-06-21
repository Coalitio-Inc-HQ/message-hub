from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, CheckConstraint, text, ForeignKey, JSON


class Base(DeclarativeBase):
    pass


class TelegramUserORM(Base):
    __tablename__ = "telegram_user"
    telegram_user_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
