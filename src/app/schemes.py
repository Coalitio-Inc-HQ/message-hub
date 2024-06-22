from pydantic import BaseModel, Field
from datetime import datetime


class PlatformDTO(BaseModel):
    id: int
    name: str = Field(max_length=30)


class ClientServerDTO(BaseModel):
    id: int
    url: str = Field(max_length=256)
    platform_id: int


class UserDTO(BaseModel):
    id: int
    platform_id: int


class ManadgerDTO(BaseModel):
    user_id: int
    number_of_linked_bots: int


class ChatUsersDTO(BaseModel):
    user_id: int
    chat_id: int


class ChatDTO(BaseModel):
    id: int
    name: str = Field(max_length=256)
    creator: int


class MessageDTO(BaseModel):
    id: int | None = None
    chat_id: int
    creator: int
    created_at: datetime
    edit_at: datetime
    text_message: str | None
