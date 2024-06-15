# from django.urls import path
# from apps.ws.consumers import  ChatConsumer

# websocket_urlpatterns = [
#     path('ws/chat/<user_name>/<room_name>', ChatConsumer.as_asgi()),
# ]

from django.urls import path

from apps.ws.consumers import  SystemConsumer

websocket_urlpatterns = [
    path('ws/system/', SystemConsumer.as_asgi()),
]
