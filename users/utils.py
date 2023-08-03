import re
import jwt
from time import time

from omtogether.settings import SECRET_KEY


def is_email(string: str):
    return re.fullmatch(r'[^@]+@[^@]+\.[^@]+', string)


def ru_phone(phone: str):
    try:
        return phone[-10:]
    except IndexError:
        return phone


def is_phone_number(string: str):
    return re.fullmatch(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', string)


def calculate_token(login: str):
    return jwt.encode({
        'login': login,
        'timestamp': str(time())
    }, key=SECRET_KEY)
