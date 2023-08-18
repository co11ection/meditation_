from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import MeditationSession
from .tasks import end_meditation
from .models import Meditation
from .serializers import MeditationSerializer


class MeditationsListView(ReadOnlyModelViewSet):
    queryset = Meditation.objects.order_by('-created_date')
    serializer_class = MeditationSerializer


class StartMeditationView(APIView):
    def post(self, request, meditation_id):
        """
        Начинает сеанс медитации для пользователя.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        meditation.scheduled_datetime = timezone.now()
        meditation.save()

        meditation_duration = meditation.duration
        end_time = meditation.scheduled_datetime + meditation_duration

        end_meditation.apply_async((meditation.id,), eta=end_time)

        end_meditation_url = reverse('meditacia:end-meditation',
                                     args=[meditation.id])

        return Response({'message': 'Начало медитации',
                         'end_meditation_url': end_meditation_url},
                        status=status.HTTP_200_OK)

# class StartMeditationView(APIView):
#     def post(self, request, meditation_id):
#         """
#         Начинает сеанс медитации для пользователя.
#         """
#         if request.user.is_authenticated:
#             meditation = get_object_or_404(Meditation, id=meditation_id)
#             session = MeditationSession.objects.create(
#                 user=request.user,
#                 meditation=meditation,
#                 start_time=timezone.now(),
#                 status="active",
#             )
#
#             meditation_duration = meditation.duration
#             end_time = session.start_time + meditation_duration
#
#             end_meditation.apply_async((session.id,), eta=end_time)
#
#             end_meditation_url = reverse('meditacia:end-meditation',
#                                          args=[session.id])
#
#             return Response({'message': 'Начало медитации',
#                              'end_meditation_url': end_meditation_url},
#                             status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Требуется аутентификация'},
#                             status=status.HTTP_401_UNAUTHORIZED)


class EndMeditationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meditation_id):
        """
        Прерывает или завершает сеанс медитации и показывает результаты.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)

        earned_tokens = 10

        return Response({"earned_tokens": earned_tokens},
                        status=status.HTTP_200_OK)


class PauseMeditationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meditation_id):
        """
        Приостанавливает сеанс медитации и останавливает таймер.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)

        session = MeditationSession.objects.get(user=request.user,
                                                meditation=meditation,
                                                status="active")

        session.status = "paused"
        session.save()

        return Response({'message': 'Медитация приостонвлена'},
                        status=status.HTTP_200_OK)
