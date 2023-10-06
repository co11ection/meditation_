from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from wallet.views import WalletTokensView
from .models import UserProfile
from .serializers import UserProfileSerializer
from .tasks import end_meditation
from .models import Meditation
from .serializers import MeditationSerializer


class UserProfileMediation(APIView):
    def get(self, request):
        profile = UserProfile.objects.get(id=request.user.id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


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


class EndMeditationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meditation_id):
        """
        Прерывает или завершает сеанс медитации и показывает результаты.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        wallet_tokens_view = WalletTokensView()
        balance = wallet_tokens_view.calculate_individual_tokens_to_earn(
            request)
        return Response({"earned_tokens": balance},
                        status=status.HTTP_200_OK)
