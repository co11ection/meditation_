from rest_framework import serializers
from .models import Meditation


class MeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        fields = '__all__'
