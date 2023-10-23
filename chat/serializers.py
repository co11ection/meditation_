from rest_framework import serializers
from .models import Room, Message
from users.serializers import UsersSerializer

class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UsersSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")
        

class RoomSerializer(serializers.ModelSerializer):
    last_meessage = serializers.SerializerMethodField()
    message = MessageSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Room
        fields = ['pk', 'name', 'host', 'message', 'current_user', 'last_message']
        depth = 1
        read_only_fields = ['messages', 'last_message']
    
    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.messages.order_by('created_by').last()).data