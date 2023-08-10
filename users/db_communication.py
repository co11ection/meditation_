from django.core.exceptions import ObjectDoesNotExist, ValidationError
from loguru import logger
from .models import CustomUser, CodePhone
from users import utils


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
        if CustomUser.objects.filter(phone_number__contains=utils.ru_phone(phone)).exists():
            raise Exception("UNIQUE constraint failed: user.phone_number")

    if email:
        if CustomUser.objects.filter(email__contains=email).exists():
            raise Exception("UNIQUE constraint failed: users.email")
        password = utils.hash_password(values['password'])

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


def get_user(**kwargs) -> CustomUser:
    login = kwargs.get("login")
    phone_number = None
    email = None
    if login:
        phone_number = utils.ru_phone(login) if utils.is_phone_number(login) else None
        email = login if utils.is_email(login) else None

    if phone_number:
        user = CustomUser.objects.filter(phone_number__contains=phone_number).first()
    elif email:
        user = CustomUser.objects.filter(email__contains=email).first()
    else:
        user = CustomUser.objects.filter(
            **kwargs
        ).first()
    if user:
        if 'token' in kwargs and not user.is_active:
            raise Exception("Your account has been blocked. Please, contact support")
    return user


def reset_password1(values):
    login = values["login"]
    if utils.is_email(login):
        user = get_user(login=login)
        if not user:
            raise ObjectDoesNotExist
        code = utils.send_mail_reset(login)

        user.code = code
        user.save()
        return {
            "login": login
        }

    elif utils.is_phone_number(login):
        raise Exception("Login must be email to change password")
    else:
        raise ValidationError("Invalid login format")


def check_code(values):
    login = values["login"]
    code = values["code"]
    if utils.is_email(login):
        user = get_user(login=login)
    else:
        raise ValidationError("Invalid login format")
    if not user:
        raise ObjectDoesNotExist

    if not user.code:
        raise Exception("No need a code")
    if user.code == code:
        user.code = 0
        user.save()
        return {
            "is_correct": True,
            "token": user.token
        }
    else:
        return {
            "is_correct": False
        }


def reset_password2(token, password):
    user = get_user(token=token)
    if not user:
        raise ObjectDoesNotExist
    user.password = utils.hash_password(password)
    user.save()
