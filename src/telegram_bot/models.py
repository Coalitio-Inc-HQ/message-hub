from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BIGINT


class Base(DeclarativeBase):
    pass


class TelegramUserORM(Base):
    __tablename__ = "telegram_user"
    telegram_user_id: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
