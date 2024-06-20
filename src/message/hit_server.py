from .database_requests import client_server_registration,create_user_from_bot
from .schemes import ChatUsersDTO

"""
Логтка обработки вызовов сервера main.
"""

def client_server_registration_logic(url:str)->int:
    """
    Логика регистрации клиентского сервера.
    Возвращяет id сервера.
    """
    setver_info = client_server_registration(url=url)
    return setver_info.id

def create_user_from_bot_logic(client_server_id:int):
    """
    Логика регистрации пользователя бота.
    Возвращяет user.id, chat.id
    """
    bot_user_info = create_user_from_bot(client_server_id = client_server_id)
    return bot_user_info
