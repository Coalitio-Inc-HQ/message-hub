from .database_requests import create_user_from_bot
from .schemes import ChatUsersDTO

"""
Логтка обработки вызовов.
"""


def create_user_from_bot_logic():
    """
    Логика регистрации пользователя бота.
    Возвращяет user.id, chat.id
    """
    bot_user_info = create_user_from_bot()
    return bot_user_info
