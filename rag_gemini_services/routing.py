from django.urls import re_path
from .consumers import GeminiChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\d+)/$', GeminiChatConsumer.as_asgi()),
]