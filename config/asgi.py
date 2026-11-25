
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.asgi import get_asgi_application

# Djangoの初期化
django_asgi_app = get_asgi_application()

# Channels
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import monitor.routing

application = ProtocolTypeRouter({
    # HTTP通信
    "http": django_asgi_app,

    # WebSocket通信
    "websocket": AuthMiddlewareStack(
        URLRouter(
            monitor.routing.websocket_urlpatterns
        )
    ),
})
