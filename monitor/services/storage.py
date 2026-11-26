
from monitor.models import SystemMetric


def save_system_metric(data, session_id):
    metric = SystemMetric.objects.create(
        session_id=session_id,
        cpu_usage=data["cpu"]["usage"],
        memory_percent=data["memory"]["percent"],
        memory_used=data["memory"]["used"],
        memory_total=data["memory"]["total"],
        disk_percent=data["disk"]["percent"],
        disk_used=data["disk"]["used"],
        disk_total=data["disk"]["total"],
        bytes_sent=data["network"]["bytes_sent"],
        bytes_recv=data["network"]["bytes_recv"],
    )

    return metric
