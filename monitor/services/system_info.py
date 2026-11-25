
import os
import psutil


def get_cpu_info():
    """CPU使用率・コア数を取得する"""

    return {
        "usage": psutil.cpu_percent(interval=None),
        "core_count": psutil.cpu_count(logical=False),
        "logical_count": psutil.cpu_count(logical=True),
    }


def get_memory_info():
    """メモリ情報を取得する"""

    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent,
    }


def get_disk_info():
    """Windowsのシステムドライブ情報を取得する"""

    disk_path = os.environ.get("SystemDrive", "C:") + "\\"
    disk = psutil.disk_usage(disk_path)

    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }


def get_network_info():
    """ネットワークの累積送受信量を取得する"""

    network = psutil.net_io_counters()

    if network is None:
        return {
            "bytes_sent": 0,
            "bytes_recv": 0,
        }

    return {
        "bytes_sent": network.bytes_sent,
        "bytes_recv": network.bytes_recv,
    }


def get_process_info():
    """実行中のプロセス一覧を取得する"""

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info", "cpu_percent"]
    ):
        try:
            info = process.info
            memory = info["memory_info"]

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": info["cpu_percent"],
                "memory_used": memory.rss if memory else 0,
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    return processes


def get_system_info():
    """システム情報をまとめて取得する"""

    return {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
        "processes": get_process_info(),
    }
