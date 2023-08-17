from rest_framework import serializers
from .models import OnboardingTextStartMeditation, OnboardingTextStartApp


class OnboardingTextStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTextStartMeditation
        fields = ('id', 'content', 'order')


class OnboardingTextPreMeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTextStartApp
        fields = ('id', 'content', 'order')
