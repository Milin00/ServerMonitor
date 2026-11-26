
import asyncio
import time

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from monitor.services.collector import SystemCollector
from monitor.services.storage import save_system_metric
from monitor.services.session_manager import (
    start_session,
    stop_session,
    recover_stale_sessions,
)


# 接続管理: channel_name -> 最終Heartbeat受信時刻
_clients = {}

# 監視状態
_monitor_task = None
_monitor_lock = asyncio.Lock()
_session_id = None

GROUP_NAME = "system_monitor"

# Heartbeatのタイムアウト設定
HEARTBEAT_TIMEOUT = 30


async def start_monitoring(channel_name):
    global _monitor_task, _session_id

    async with _monitor_lock:
        # 接続を登録
        _clients[channel_name] = time.monotonic()

        # 監視タスクが存在しない場合だけ起動
        if _monitor_task is None or _monitor_task.done():

            # 前回のサーバー異常終了で残ったセッションを復旧
            recovered_count = await database_sync_to_async(
                recover_stale_sessions
            )()

            print(
                f"[MONITOR] セッション復旧確認: "
                f"{recovered_count}件"
            )

            # 新しい監視セッションを開始
            session = await database_sync_to_async(
                start_session
            )()

            _session_id = session.pk

            # 監視タスクを作成
            _monitor_task = asyncio.create_task(
                monitor_loop(_session_id)
            )

            print(
                f"[MONITOR] 監視開始: Session #{_session_id}"
            )

        print(f"[MONITOR] 接続数: {len(_clients)}")

        return _session_id

async def update_client_heartbeat(channel_name):
    async with _monitor_lock:
        if channel_name not in _clients:
            return False

        _clients[channel_name] = time.monotonic()
        print(f"[HEARTBEAT] {channel_name} 更新")

        return True


async def stop_monitoring(channel_name):
    global _monitor_task, _session_id

    async with _monitor_lock:
        if channel_name not in _clients:
            return

        _clients.pop(channel_name)

        print(f"[MONITOR] 接続解除: {channel_name}")
        print(f"[MONITOR] 残り接続数: {len(_clients)}")

        if _clients:
            return

        await _stop_monitoring_locked()


async def _stop_monitoring_locked():
    global _monitor_task, _session_id

    print("[MONITOR] 全接続切断。監視停止処理を開始")

    task = _monitor_task
    session_id = _session_id

    # 先に共有状態をクリア
    _monitor_task = None
    _session_id = None

    # 監視タスクを停止
    if task is not None and not task.done():
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            print("[MONITOR] 監視タスクをキャンセルしました")

    # 対象セッションを終了
    if session_id is not None:
        session = await database_sync_to_async(stop_session)(
            session_id
        )
        print(f"[MONITOR] セッション終了: {session}")


async def monitor_loop(session_id):
    global _monitor_task, _session_id

    collector = SystemCollector()
    channel_layer = get_channel_layer()

    save_counter = 0

    try:
        while True:
            async with _monitor_lock:
                now = time.monotonic()

                expired_clients = [
                    channel_name
                    for channel_name, last_seen in _clients.items()
                    if now - last_seen > HEARTBEAT_TIMEOUT
                ]

                for channel_name in expired_clients:
                    _clients.pop(channel_name, None)

                    print(
                        f"[MONITOR] Heartbeatタイムアウト: "
                        f"{channel_name}"
                    )

                    await channel_layer.send(
                        channel_name,
                        {
                            "type": "monitor.timeout",
                        }
                    )

                if not _clients:
                    print("[MONITOR] 全接続タイムアウト")

                    if _monitor_task is asyncio.current_task():
                        _monitor_task = None
                        _session_id = None

                    session = await database_sync_to_async(
                        stop_session
                    )(session_id)

                    print(f"[MONITOR] セッション終了: {session}")
                    return

            data = collector.collect()

            await channel_layer.group_send(
                GROUP_NAME,
                {
                    "type": "system.update",
                    "data": data,
                }
            )

            save_counter += 1

            if save_counter >= 5:
                await database_sync_to_async(
                    save_system_metric
                )(data, session_id)

                save_counter = 0

            await asyncio.sleep(1)

    except asyncio.CancelledError:
        raise