from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import CustomUser


# Create your views here.

def send_tokens_to_app():
    pass


@api_view(['POST'])
def send_tokens_to_user(request):
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


def buy_tokens_from_market():
    pass


def calculate_meditation_tokens_to_finish():
    pass


def booster_long():
    pass
