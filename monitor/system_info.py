import psutil
import os

def get_system_info():

    # CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)

    # メモリ情報
    memory = psutil.virtual_memory()

    # ディスク情報
    disk_path= os.environ.get('SystemDirve','C:')+'\\'
    disk = psutil.disk_usage(disk_path)

    # ネットワーク情報
    network = psutil.net_io_counters()

    return {
        'cpu': cpu_usage,

        'memory': {
            'total': round(memory.total / (1024 ** 3), 2),
            'used': round(memory.used / (1024 ** 3), 2),
            'percent': memory.percent,
        },

        'disk': {
            'total': round(disk.total / (1024 ** 3), 2),
            'used': round(disk.used / (1024 ** 3), 2),
            'percent': disk.percent,
        },

        'network': {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
        }
    }