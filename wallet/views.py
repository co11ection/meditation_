from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import CustomUser
from .models import WalletTokens
from .serializers import WalletSerializer
from rest_framework.permissions import AllowAny


class WalletTokensView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Получение баланса накопленных токенов пользователя.
        """
        user = request.user
        balance = self.get_balance(user)

        response_data = {
            "balance": balance,
            "user": user.id
        }

        return Response(response_data, status.HTTP_200_OK)

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

    def get_balance(self, user):
        """
            Получение баланса пользователя из базы данных.
            """
        wallet_tokens = WalletTokens.objects.get(user=user)
        return wallet_tokens.balance

    def calculate_balance(self, user):
        """
        Расчет баланса накопленных токенов пользователя.
        """
        base_value = 10
        b = self.calculate_booster(user)
        d = self.calculate_degradation(user)
        k = self.calculate_coefficient(user)
        n = base_value + b + d

        result = n + n * k

        wallet_tokens, _ = WalletTokens.objects.get_or_create(user=user)
        wallet_tokens.balance = result
        wallet_tokens.save()

        return wallet_tokens

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
