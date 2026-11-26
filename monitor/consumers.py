
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from monitor.services.live_monitor import (
    GROUP_NAME,
    start_monitoring,
    stop_monitoring,
    update_client_heartbeat,
)

class SystemMonitorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            GROUP_NAME,
            self.channel_name
        )

        await self.accept()

        self.session_id = await start_monitoring(
            self.channel_name
        )

    async def disconnect(self, close_code):
        print(
            f"[WS] disconnect: {self.channel_name}, "
            f"code={close_code}"
        )

        await self.channel_layer.group_discard(
            GROUP_NAME,
            self.channel_name
        )

        await stop_monitoring(self.channel_name)

        print("[WS] disconnect処理完了")

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
        except json.JSONDecodeError:
            return

        if message.get("type") == "heartbeat":
            await update_client_heartbeat(
                self.channel_name
            )

    async def system_update(self, event):
        await self.send(
            text_data=json.dumps(event["data"])
        )

    async def monitor_timeout(self, event):
        print(
            f"[WS] Heartbeatタイムアウトによる切断: "
            f"{self.channel_name}"
        )
        await self.close(code=4000)
