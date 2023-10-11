from rest_framework import serializers
from .models import OnboardText, OnboardType


class OnboardingTextSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = OnboardText
        fields = "__all__"


class OnboardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        models = OnboardType
        fields = "type"
