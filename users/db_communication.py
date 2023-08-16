import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from loguru import logger
from rest_framework.authtoken.models import Token
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
    login = values['login']
    nickname = values['nickname']
    email = login if utils.is_email(login) else None
    phone = None
    password = None
    if utils.is_phone_number(login):
        phone = login
        if CustomUser.objects.filter(phone_number__contains=utils.ru_phone(phone)).exists():
            raise Exception("UNIQUE constraint failed: user.phone_number")

    if email:
        if CustomUser.objects.filter(email__icontains=email).exists():
            raise Exception("UNIQUE constraint failed: users.email")
        password = utils.hash_password(values['password'])

    if CustomUser.objects.filter(nickname=nickname).exists():
        raise Exception("UNIQUE constraint failed: users.nickname")

    user = CustomUser.objects.create_user(
        login=login,
        nickname=nickname,
        password=password,
        email=email,
        phone_number=phone,
        fcm_token=values['fcm_token']
    )
    logger.debug(f'Created new user with fcm token {values["fcm_token"]}')

    token_obj, created = Token.objects.get_or_create(user=user)
    token = token_obj.key

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
        if not user.is_active:
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
        token_obj = Token.objects.get(user=user)
        token = token_obj.key
        return {
            "is_correct": True,
            "token": token
        }
    else:
        return {
            "is_correct": False
        }


def reset_password2(user, password):
    user.password = utils.hash_password(password)
    user.save()


def change_photo(user, photo: str):
    if photo:
        format, imgstr = photo.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{user.username}_ava.{ext}')
        user.photo = data
    else:
        user.photo = None
    user.save()
