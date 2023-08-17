from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import datetime
from celery import shared_task
from .tasks import end_meditation
from .models import Meditation
from .serializers import MeditationSerializer


class MeditationsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Получает список всех существующих медитаций.
        """
        meditations = Meditation.objects.all()
        serializer = MeditationSerializer(meditations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartMeditationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meditation_id):
        """
        Начинает сеанс медитации для пользователя.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        meditation.scheduled_datetime = timezone.now()
        meditation.save()

        meditation_duration = meditation.duration
        end_time = meditation.scheduled_datetime + meditation_duration

        # Schedule the end_meditation Celery task
        end_meditation.apply_async((meditation.id,), eta=end_time)

        return Response(status=status.HTTP_200_OK)


class EndMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        """
        Прерывает или завершает сеанс медитации и показывает результаты.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        # Рассчитать заработанные токены на основе продолжительности сеанса, пользователя и т. д.
        # Показать результаты с заработанными токенами
        return Response({"earned_tokens": earned_tokens},
                        status=status.HTTP_200_OK)


class PauseMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        """
        Приостанавливает сеанс медитации и останавливает таймер.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        # Логика приостановки сеанса медитации здесь
        return Response(status=status.HTTP_200_OK)


class CreateMeditationView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Создает новую медитацию.
        """
        serializer = MeditationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
