from pydantic import BaseModel,Field
from datetime import datetime
# from typing import Optional

class ClientServerDTO(BaseModel):
    id: int
    url:str

class UserDTO(BaseModel):
    id: int
    client_server_id: int

class ChatUsersDTO(BaseModel):
    user_id:int
    chat_id:int

class ChatDTO(BaseModel):
    id:int
    name: str = Field (max_length=256)

class MessageDTO(BaseModel):
    message_id:int
    chat_id:int
    from_user:int
    created_at:datetime
    edit_at:datetime
    text_message:str|None