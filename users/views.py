from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import UsersSerializer
from .utils import is_phone_number, is_email, ru_phone, calculate_token


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
        if not (is_phone_number(login) or is_email(login)):
            return Response({"error": "Логин должен быть электронной почтой или номером телефона"},
                            status=status.HTTP_400_BAD_REQUEST)

        if is_phone_number(login):
            login = ru_phone(login)
            user = Users.objects.filter(phone_number=login).first()
        else:
            user = Users.objects.filter(email=login).first()

        if user:
            user.fcm_token = values.get('fcm_token')
            user.save()
            return Response({
                'authorized': True,
                'token': user.token,
                'id': user.id,
            })

        token, user = add_user(values, request.GET.get('ref'))
        return Response({
            "token": token,
            "id": user.id,
        }, status=status.HTTP_201_CREATED)

    except Exception as err:
        return Response({"error": f"Что-то пошло не так: {err}"},
                        status=status.HTTP_400_BAD_REQUEST)


def add_user(values, ref):
    """
    Добавление нового пользователя в базу данных.

    Параметры:
    - values (dict): Данные пользователя (имя пользователя, логин, пароль и т.д.).
    - ref (str): Код реферала (необязательно).

    Возвращает:
    - token (str): Сгенерированный токен для нового пользователя.
    - user (Users): Вновь созданный экземпляр пользователя.
    """
    # Ваша логика функции add_user здесь
    # Рассчитайте токен с помощью функции calculate_token
    # Создайте экземпляр пользователя и сохраните его
    # Верните токен и экземпляр пользователя
    pass


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
        user = Users.objects.get(pk=user_id)

        # Рассчитываем количество токенов
        n = base_value + booster + degradation
        result = n + n * k

        # Обновляем баланс пользователя
        user.balance += result
        user.save()

        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Users.DoesNotExist:
        return Response({"error": "Пользователь не найден."},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Что-то пошло не так: {e}"},
                        status=status.HTTP_400_BAD_REQUEST)
