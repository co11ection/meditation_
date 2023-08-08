import hashlib
from loguru import logger
from users import utils
from .models import CustomUser
from .utils import ru_phone


def add_user(values: dict) -> tuple:
    """
    Добавление нового пользователя в базу данных.

    Параметры:
    - values (dict): Данные пользователя (имя пользователя, логин, пароль и т.д.).

    Возвращает:
    - token (str): Сгенерированный токен для нового пользователя.
    - user (Users): Вновь созданный экземпляр пользователя.
    """

    token = utils.calculate_token(values['login'])  # Используем вашу функцию для генерации токена
    login = values['login']
    email = login if utils.is_email(login) else None
    phone = None
    password = None
    if utils.is_phone_number(login):
        phone = login
        if CustomUser.objects.filter(phone_number__contains=ru_phone(phone)):
            raise Exception("UNIQUE constraint failed: user.phone_number")

    if email:
        if CustomUser.objects.filter(email__contains=email):
            raise Exception("UNIQUE constraint failed: users.email")
        password = hashlib.sha256(values['password'].encode("utf-8")).hexdigest()

    user = CustomUser.objects.create_user(
        login=login,
        token=token,
        nickname=values['nickname'],
        password=password,
        email=email,
        phone_number=phone,
        fcm_token=values['fcm_token']
    )
    logger.debug(f'Created new user with fcm token {values["fcm_token"]}')

    return token, user
