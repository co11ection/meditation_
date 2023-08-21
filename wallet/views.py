from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import CustomUser
from rest_framework.permissions import AllowAny

from .models import WalletRatio
from .models import WalletTokens
# from .utils import calculate_group_meditation_tokens, get_balance
from . import utils


class WalletTokensView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Получение баланса накопленных токенов пользователя.
        """
        user = request.user
        balance = utils.get_balance(user)

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

    @staticmethod
    def calculate_booster(request):
        """
        Расчет ускорителя на основе непрерывной практики пользователя.
        """
        if request.user.consecutive_meditation_days > 21:
            return 1.2
        elif request.user.consecutive_meditation_days > 40:
            return 1.5
        elif request.user.consecutive_meditation_days > 90:
            return 2
        else:
            return 1

    @staticmethod
    def calculate_degradation():
        """
        Расчет понижающего коэффициента для пользователя.
        """
        degradation = 0.05
        return degradation

    @staticmethod
    def calculate_coefficient():
        """
        Расчет коэффициента на основе различных факторов.
        """
        coefficient = 0.5
        return coefficient

    def calculate_individual_tokens_to_earn(self, request):
        user = request.user
        balance = utils.get_balance(user)
        booster = self.calculate_booster(request)
        degradation = self.calculate_degradation()
        wallet_ratio_instance = WalletRatio.objects.first()
        group_size = int(request.data.get('group_size', 0))
        group_ratio = utils.calculate_group_meditation_tokens(group_size)

        earn_finish = ((wallet_ratio_instance.base_value + booster + degradation) +
                       (wallet_ratio_instance.base_value + booster + degradation) * group_ratio)
        individual_tokens = int(earn_finish)

        with transaction.atomic():
            if balance is not None:
                updated_balance = balance + individual_tokens
                self.update_balance(user, updated_balance)
            else:
                self.create_balance(user, individual_tokens)
        response_data = {
            'tokens_earned': individual_tokens,
            'total_balance': updated_balance if balance is not None else individual_tokens,
        }

        return response_data

    def update_balance(self, user, new_balance):
        try:
            wallet_tokens = WalletTokens.objects.get(user=user)
            wallet_tokens.balance = new_balance
            wallet_tokens.save()
        except WalletTokens.DoesNotExist:
            self.create_balance(user, new_balance)

    def create_balance(self, user, balance):
        WalletTokens.objects.create(user=user, balance=balance)


class GroupMediationTokensView(APIView):
    @staticmethod
    def post(self, request):
        group_size = int(request.data.get('group_size', 0))
        earned_tokens = utils.calculate_group_meditation_tokens(group_size)
        return Response({'earned_tokens': earned_tokens})
