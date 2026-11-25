
import time
from datetime import datetime

import psutil

from monitor.services.system_info import get_system_info


class SystemCollector:
    """システム情報を定期的に取得するクラス"""

    def __init__(self):
        # ネットワーク速度計算用の初期値
        network = psutil.net_io_counters()

        self.previous_sent = network.bytes_sent
        self.previous_recv = network.bytes_recv
        self.previous_time = time.monotonic()

        # CPU使用率の初回測定を初期化
        psutil.cpu_percent(interval=None)

        # プロセスごとのCPU測定も初期化
        for process in psutil.process_iter():
            try:
                process.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

    def collect(self):
        """システム情報を1回取得する"""

        # システム情報を取得
        data = get_system_info()

        # ネットワーク累積通信量
        current_sent = data["network"]["bytes_sent"]
        current_recv = data["network"]["bytes_recv"]

        # 経過時間
        current_time = time.monotonic()
        elapsed = current_time - self.previous_time

        # 通信速度を計算
        if elapsed > 0:
            upload_speed = max(
                0, current_sent - self.previous_sent
            ) / elapsed

            download_speed = max(
                0, current_recv - self.previous_recv
            ) / elapsed
        else:
            upload_speed = 0
            download_speed = 0

        # 次回測定用に更新
        self.previous_sent = current_sent
        self.previous_recv = current_recv
        self.previous_time = current_time

        # ネットワーク情報に速度を追加
        data["network"]["upload_speed"] = upload_speed
        data["network"]["download_speed"] = download_speed

        # 取得日時を追加
        data["timestamp"] = datetime.now().astimezone().isoformat()

        return data