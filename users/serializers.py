from rest_framework import serializers
from .models import Users, CodePhone


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CodePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePhone
        fields = '__all__'






