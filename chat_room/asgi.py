
import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
# from main import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_room.settings")
django.setup()

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            __import__('main.routing').routing.websocket_urlpatterns
        )
    ),
})
