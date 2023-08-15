from rest_framework import serializers
from .models import CustomUser, CodePhone


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login')


class CodePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePhone
        fields = '__all__'
