from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OnboardingTextStartApp, \
    OnboardingTextStartMeditation
from .serializers import OnboardingTextStartSerializer, \
    OnboardingTextPreMeditationSerializer


class OnboardBaseView(ListAPIView):
    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.order_by('order')


class OnboardStartAppView(OnboardBaseView):
    model = OnboardingTextStartApp
    serializer_class = OnboardingTextStartSerializer


class OnboardStartMeditationView(OnboardBaseView):
    model = OnboardingTextStartMeditation
    serializer_class = OnboardingTextPreMeditationSerializer
