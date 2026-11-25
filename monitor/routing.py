from django.urls import path

from monitor.consumers import SystemMonitorConsumer

websocket_urlpatterns = [
    path(
        "ws/monitor/",
        SystemMonitorConsumer.as_asgi()
    ),
]