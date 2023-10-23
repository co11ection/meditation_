import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
from .models import Room, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = await self.get_user_from_token(self.scope['query_string'])

        if self.user:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(message)
        

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': self.user.nickname  # Используйте поле пользователя, которое вы хотите
            }
        )
        
        await self.send_notification(message)

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    async def get_user_from_token(self, token_str):
        try:
            token_key = token_str.decode("utf-8").split('=')[1]
            token = Token.objects.get(key=token_key)
            user = User.objects.get(id=token.user_id)
            return user
        except Token.DoesNotExist:
            return None

    async def save_message(self, message_text):
        if self.user:
            room = Room.objects.get(name=self.room_name)
            message = Message(room=room, text=message_text, user=self.user)
            message.save()
    
    async def send_notification(self, message):
        notification_data = {
            'type': 'chat.notification',
            'message': 'У вас новое сообщение: ' + message,
            'user': self.user.nickname
        }

        
        await self.channel_layer.group_send(
            self.room_group_name,
            notification_data
        )   
