from django.urls import path,re_path
from . import consumers

websocket_urlpatterns= [
    path('ws/ac/<str:roomname>/', consumers.ChatConsumer.as_asgi()),
]