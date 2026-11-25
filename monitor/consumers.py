
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SystemMonitorConsumer(AsyncWebsocketConsumer):
    """システム監視用WebSocket Consumer"""

    async def connect(self):
        """WebSocket接続時"""

        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "message": "WebSocket connection established"
        }))

    async def disconnect(self, close_code):
        """WebSocket切断時"""

        print(f"WebSocket disconnected: {close_code}")
