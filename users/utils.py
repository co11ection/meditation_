import re
import jwt
import requests
import json
import random
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


def send_phone_reset(phone):
    code = random.randint(100000, 999999)
    body = json.dumps(
        {
            "messages": [
                {
                    "phone": phone,
                    "sender": "BiBipTrip",
                    "clientId": "1",
                    "text": "Ваш код подтверждения приложения BiBipTrip: " + str(code) + ". Не говорите код!"
                }
            ],
            "statusQueueName": "myQueue",
            "showBillingDetails": True,
            "login": "rkaydarzinn88",
            "password": "YaGIQ27Kt"
        }
    )
    r = requests.post('https://api.iqsms.ru/messages/v2/send.json', data=body)
    # print(r.text)
    # print(phone)
    return code, r.text
