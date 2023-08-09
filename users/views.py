from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UsersSerializer
from .db_communication import add_user, get_user
from users import utils


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_get_code(request):
    try:
        values = request.data
        if not (utils.is_phone_number(values['login'])):
            return Response("login must be phone number",
                            status=status.HTTP_400_BAD_REQUEST)
        phone = values['login']
        is_registered = False
        if CustomUser.objects.filter(phone_number__contains=utils.ru_phone(phone)):
            is_registered = True
        code, text = utils.send_phone_reset(phone)
        return Response({
            "code": code,
            "text": text,
            "is_registered": is_registered,
        })
    except Exception as err:
        return Response({"error": f"Something went wrong: {err}"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """
    Регистрация нового пользователя или аутентификация существующего.

    Параметры:
    - login (str): Логин пользователя (электронная почта или номер телефона).
    - fcm_token (str): Токен FCM для push-уведомлений.

    Возвращает:
    - Если пользователь существует, возвращает ответ с данными авторизации (токен и ID).
    - Если пользователь новый, возвращает ответ с данными регистрации (токен и ID).

    Если логин не является ни электронной почтой, ни номером телефона, возвращает ошибку неверного запроса.
    """
    try:
        values = request.data
        login = values.get('login')
        if not (utils.is_phone_number(login) or utils.is_email(login)):
            return Response({
                "error": "Login must be email or phone number"},
                status=status.HTTP_400_BAD_REQUEST)

        if utils.is_email(login) and 'password' in values:
            token, user = add_user(values)
            return Response({
                "token": token,
                "id": user.id,
            }, status=status.HTTP_201_CREATED)
        elif utils.is_phone_number(login):
            token, user = add_user(values)
            return Response({
                "token": token,
                "id": user.id,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error": "Invalid registration request"},
                status=status.HTTP_400_BAD_REQUEST)

    except Exception as err:
        return Response({"error": f"Something went wrong: {err}"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    try:
        values = request.data
        login = values.get('login')
        password = values.get('password')
        fcm_token = values.get('fcm_token')
        user = None
        if not (utils.is_phone_number(login) or utils.is_email(login)):
            return Response({
                "error": "Login must be email or phone number"},
                status=status.HTTP_400_BAD_REQUEST)
        if utils.is_phone_number(login):
            login = utils.ru_phone(login)
            user = get_user(
                login=login
            )
        if utils.is_email(login) and 'password' in values:
            user = get_user(
                login=login
            )
        if user is None:
            return Response({
                'authorized': False,
                'error': 'User with such login does not exists'
            })
        if utils.is_email(login) and check_password(utils.hash_password(password), user.password):
            user.fcm_token = fcm_token
            user.save()
            return Response({
                'authorized': True,
                'token': user.token,
                "id": user.id,
            })
        elif utils.is_phone_number(login):
            user.fcm_token = fcm_token
            user.save()
            return Response({
                'authorized': True,
                'token': user.token,
                "id": user.id,
            })
        else:
            return Response({
                'authorized': False,
                'error': 'Wrong credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        return Response({"error": f"Something went wrong: {err}"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def calculate_tokens(request):
    """
    Рассчитать и обновить баланс пользователя на основе коэффициентов медитации и бонусов.

    Параметры:
    - user_id (int): ID пользователя.
    - base_value (float): Базовое значение токенов.
    - booster (float): Коэффициент ускорения.
    - degradation (float): Коэффициент деградации.
    - k (float): Плавающий коэффициент.

    Возвращает:
    - Ответ с обновленными данными пользователя (баланс, ID и т.д.).

    Если пользователь не существует, возвращает ошибку "не найдено".
    """
    try:
        user_id = request.data.get('user_id')
        base_value = request.data.get('base_value', 0)
        booster = request.data.get('booster', 0)
        degradation = request.data.get('degradation', 0)
        k = request.data.get('k', 0)

        # Получаем пользователя по ID
        user = CustomUser.objects.get(pk=user_id)

        # Рассчитываем количество токенов
        n = base_value + booster + degradation
        result = n + n * k

        # Обновляем баланс пользователя
        user.balance += result
        user.save()

        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "Пользователь не найден."},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Что-то пошло не так: {e}"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_profile(request, pk):
    """
    Получить, обновить или удалить профиль пользователя.

    Параметры:
    - request: объект запроса Django REST framework.
    - pk (int): ID пользователя.

    Методы:
    - GET: Получить информацию о пользователе.
    - PUT: Обновить информацию о пользователе.
    - DELETE: Удалить пользователя.

    Возвращает:
    - Ответ с данными пользователя в случае GET и PUT.
    - Пустой ответ в случае успешного удаления пользователя.
    - Ответ с ошибкой "Пользователь не найден" в случае отсутствия пользователя с указанным ID.

    Пример запроса GET:
    GET /api/users/1/
    Возвращает данные пользователя с ID=1.

    Пример запроса PUT:
    PUT /api/users/1/
    {
        "username": "Новое имя пользователя",
        "email": "новаяпочта@example.com",
        ...
    }
    Обновляет информацию о пользователе с ID=1.

    Пример запроса DELETE:
    DELETE /api/users/1/
    Удаляет пользователя с ID=1.
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"error": "Пользователь не найден."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
