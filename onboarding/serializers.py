from rest_framework import serializers
from .models import OnboardingText


class OnboardingTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingText
        fields = '__all__'
