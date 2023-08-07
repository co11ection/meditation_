from loguru import logger
from users import utils
from .models import CustomUser


def add_user(values: dict, token=None) -> tuple:
    """
    Добавление нового пользователя в базу данных.

    Параметры:
    - values (dict): Данные пользователя (имя пользователя, логин, пароль и т.д.).

    Возвращает:
    - token (str): Сгенерированный токен для нового пользователя.
    - user (Users): Вновь созданный экземпляр пользователя.
    """
    if not token:
        token = utils.calculate_token(values['login'])  # Используем вашу функцию для генерации токена
    login = values['login']
    email = values['email']
    phone = None
    if utils.is_phone_number(login):
        phone = login

    user = CustomUser(
        login=login,
        token=token,
        first_name=values['firstname'],
        email=email,
        phone_number=phone,
        fcm_token=values['fcm_token']
    )
    logger.debug(f'Created new user with fcm token {values["fcm_token"]}')
    user.save()

    return token, user
