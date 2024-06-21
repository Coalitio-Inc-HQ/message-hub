from pydantic import BaseModel


class TelegramUserDTO(BaseModel):
    telegram_user_id: int
    user_id: int
    chat_id: int
