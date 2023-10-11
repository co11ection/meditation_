import re
import requests
import json
import phonenumbers
# import vonage
import random
from django.core.mail import send_mail

from omtogether.settings import EMAIL_HOST_USER, SMS_PASSWORD, SMS_LOGIN, SMS_KEY, SMS_SECRET_KEY


def is_email(string: str):
    return re.fullmatch(r'[^@]+@[^@]+\.[^@]+', string)


def ru_phone(phone: str):
    try:
        return phone[-10:]
    except IndexError:
        return phone


# def is_phone_number(string: str):
#     return re.fullmatch(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', string)


def is_phone_number(string: str):
    parsed_number = phonenumbers.parse(string, None)
    return phonenumbers.is_possible_number(parsed_number)


# def is_phone_number_test(phone_number: str):
#     parsed_number = phonenumbers.parse(phone_number, None)
#     is_valid = phonenumbers.is_valid_number(parsed_number)
#     formatted_number = phonenumbers.format_number(parsed_number,
#                                                   phonenumbers.PhoneNumberFormat.INTERNATIONAL)
#     print(parsed_number)
#     print(is_valid)
#     print(formatted_number)


# def calculate_token(login: str):
#     return jwt.encode({
#         'login': login,
#         'timestamp': str(time())
#     }, key=SECRET_KEY)


def send_phone_reset(phone):
    code = random.randint(100000, 999999)
    body = json.dumps(
        {
            "messages": [
                {
                    "phone": phone,
                    "sender": "MediaGramma",
                    "clientId": "1",
                    "text": "Ваш код подтверждения приложения Omtogether: " + str(code) + ". Не говорите код!"
                }
            ],
            "statusQueueName": "myQueue",
            "showBillingDetails": True,
            "login": SMS_LOGIN,
            "password": SMS_PASSWORD
        }
    )
    requests.post('https://api.iqsms.ru/messages/v2/send.json', data=body)
    return code


# def send_phone_code(phone):
#     code = random.randint(100000, 999999)
#     client = vonage.Client(key="c8437bab", secret="Ba5u1ftxvSetEREZ")
#     response_data = client.sms.send_message(
#         {
#             "from": "Vonage APIs",
#             "to": "79005320888",
#             "text": "Ваш код подтверждения приложения Test: " + str(code) + ". Не говорите код!",
#         }
#     )
#
#     if response_data["messages"][0]["status"] == "0":
#         return code, response_data
#     else:
#         return 0, response_data['messages'][0]['error-text']


def send_mail_reset(email):
    code = random.SystemRandom().randint(100000, 999999)
    try:
        send_mail('Your code',
                  f'Введите этот код для подтверждения личности на сервисе Test:'
                  f' {code}',
                  EMAIL_HOST_USER,
                  [email],
                  fail_silently=False, )
        return code
    except Exception as ex:
        return ex
