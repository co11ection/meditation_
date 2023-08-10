from rest_framework import serializers
from .models import ChatMessage, OnboardingText, Complaint
from .models import OnboardingStep
from .models import UserOnboarding


class OnboardingTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingText
        fields = '__all__'


class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingStep
        fields = '__all__'


class UserOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOnboarding
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'
