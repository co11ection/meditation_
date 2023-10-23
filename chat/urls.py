from django.urls import path, re_path, include
from rest_framework import routers
from .views import RoomViewSet, MessageViewSet
from . import consumers

# Создаем router для DRF viewsets
router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet)

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# URL-паттерны для API
urlpatterns = [
    path('api/', include(router.urls)), 
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
