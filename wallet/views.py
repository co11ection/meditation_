from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import CustomUser
from .serializers import WalletSerializer
from rest_framework.permissions import AllowAny


class WalletTokensView(APIView):
    permission_classes = [AllowAny]

    @api_view(['GET'])
    def get(self, request):
        """
        Получение баланса накопленных токенов пользователя.
        """
        user = request.user  # Предполагается, что пользователь авторизован
        balance = self.calculate_balance(user)
        serializer = WalletSerializer(balance)
        return Response(serializer.data)

    @api_view(['POST'])
    def post(self, request):
        """
        Покупка и отправка токенов другому пользователю.
        """
        sender_id = request.data.get('sender_id')
        recipient_id = request.data.get('recipient_id')
        amount_to_send = request.data.get('amount')

        try:
            sender = CustomUser.objects.get(id=sender_id)
            recipient = CustomUser.objects.get(id=recipient_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        if sender.send_tokens_to_user(recipient, amount_to_send):
            return Response({'message': 'Токены успешны отправлены'},
                            status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Недостаточно токенов на балансе отправителя'},
                status=status.HTTP_400_BAD_REQUEST)

    def calculate_balance(self, user):
        """
        Расчет баланса накопленных токенов пользователя.
        """
        base_value = 10  # Значение токенов без коэффициентов
        b = self.calculate_booster(user)  # Ускоритель
        d = self.calculate_degradation(user)  # Понижающий коэффициент
        k = self.calculate_coefficient(user)  # Коэффициент
        n = base_value + b + d

        # Расчет начисления токенов за медитации
        result = n + n * k

        return result

    def calculate_booster(self, user):
        """
        Расчет ускорителя на основе непрерывной практики пользователя.
        """
        booster = 0.2
        return booster

    def calculate_degradation(self, user):
        """
        Расчет понижающего коэффициента для пользователя.
        """
        degradation = 0.05
        return degradation

    def calculate_coefficient(self, user):
        """
        Расчет коэффициента на основе различных факторов.
        """
        coefficient = 0.5
        return coefficient


#
# def send_tokens_to_app():
#     pass
#
#
# @api_view(['GET', 'POST'])
# def hello(request):
#     if request.method == 'POST':
#         return Response(
#             {'message': 'Полученные данные', 'data': 'request.data'})
#
#     return Response({'message': 'Это Get'})
#
#
# @api_view(['POST'])
# def send_tokens_to_user(request):
#     sender_id = request.data.get('sender_id')
#     recipient_id = request.data.get('recipient_id')
#     amount_to_send = request.data.get('amount')
#
#     try:
#         sender = CustomUser.objects.get(id=sender_id)
#         recipient = CustomUser.objects.get(id=recipient_id)
#     except CustomUser.DoesNotExist:
#         return Response({'error': 'User not found'},
#                         status=status.HTTP_404_NOT_FOUND)
#     if sender.send_tokens_to_user(recipient, amount_to_send):
#         return Response({'message': 'Токены успешны отправлены'},
#                         status=status.HTTP_200_OK)
#     else:
#         return Response(
#             {'error': 'Недостаточно токенов на балансе отправителя'},
#             status=status.HTTP_400_BAD_REQUEST)
#
#
# def buy_tokens_from_market():
#     pass
#
#
# def calculate_meditation_tokens_to_finish():
#     pass
#
#
# def booster_long():
#     pass


def buy_tokens_from_market():
    pass


def calculate_meditation_tokens_to_finish():
    pass


def booster_long():
    pass
