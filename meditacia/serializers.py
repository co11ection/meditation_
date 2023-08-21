from rest_framework import serializers
from .models import Meditation, UserProfile


class MeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
