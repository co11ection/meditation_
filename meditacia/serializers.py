from rest_framework import serializers
from .models import Meditation, UserProfile, GroupMeditation


class MeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class GroupMeditationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = GroupMeditation
        fields = "__all__"
