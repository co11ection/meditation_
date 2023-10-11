from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
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
from .models import UserProfile, GroupMeditation
from .serializers import UserProfileSerializer
from .tasks import end_meditation
from .models import Meditation
from .serializers import MeditationSerializer, GroupMeditationSerializer


class UserProfileMediation(APIView):
    def get(self, request):
        profile = UserProfile.objects.get(id=request.user.id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class MeditationsListView(ReadOnlyModelViewSet):
    queryset = Meditation.objects.order_by("-created_date")
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

        end_meditation_url = reverse("meditacia:end-meditation", args=[meditation.id])

        return Response(
            {"message": "Начало медитации", "end_meditation_url": end_meditation_url},
            status=status.HTTP_200_OK,
        )


class EndMeditationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, meditation_id):
        """
        Прерывает или завершает сеанс медитации и показывает результаты.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        wallet_tokens_view = WalletTokensView()
        balance = wallet_tokens_view.calculate_individual_tokens_to_earn(request)
        return Response({"earned_tokens": balance}, status=status.HTTP_200_OK)


class GroupMeditationViewSet(viewsets.ModelViewSet):
    queryset = GroupMeditation.objects.all()
    serializer_class = GroupMeditationSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["POST"])
    def join(self, request, pk=None):
        meditation = self.get_object()
        user = request.user

        if user not in meditation.participants.all():
            meditation.participants.add(user)
            meditation.save()
            return Response({"message": "Вы успешно присоединились к медитации."})
        else:
            return Response(
                {"message": "Вы уже присоединены к этой медитации."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["GET"])
    def upcoming_meditations(self, request):
        now = timezone.now()
        upcoming_meditations = GroupMeditation.objects.filter(start_datetime__gt=now)
        serializer = GroupMeditationSerializer(upcoming_meditations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def past_meditations(self, request):
        now = timezone.now()
        past_meditations = GroupMeditation.objects.filter(start_datetime__lt=now)
        serializer = GroupMeditationSerializer(past_meditations, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
