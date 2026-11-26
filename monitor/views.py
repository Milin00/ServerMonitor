from django.shortcuts import render
from .services.system_info import get_system_info
from monitor.models import SystemMetric
from django.http import JsonResponse

def index(request):
    #システム情報を取得
    system_info=get_system_info()
    #データベースに保存
    SystemMetric.objects.create(
        cpu_usage=system_info['cpu'],
        memory_percent=system_info['memory']['percent'],
        memory_used=system_info['memory']['used'],
        memory_total=system_info['memory']['total'],
        disk_percent=system_info['disk']['percent'],
        disk_used=system_info['disk']['used'],
        disk_total=system_info['disk']['total'],
        bytes_sent=system_info['network']['bytes_sent'],
        bytes_recv=system_info['network']['bytes_recv']
    )
    history = list(SystemMetric.objects.order_by('-created_at')[:20])

    # グラフ用データは古い順に並べ替える
    chart_history = list(reversed(history))

    chart_data = {
        'labels': [item.created_at.strftime('%H:%M:%S') for item in chart_history],
        'cpu': [item.cpu_usage for item in chart_history],
        'memory': [item.memory_percent for item in chart_history],
        'disk': [item.disk_percent for item in chart_history]
    }
    params={
        'system_info': system_info,
        'history': history,
        'chart_data': chart_data
    }

    return render(request, 'monitor/index.html', params)

def websocket_test(request):
    return render(request, 'monitor/websocket_test.html')

def metric_history(request):
    metrics = SystemMetric.objects.order_by("-created_at")[:50]

    data = [
        {
            "id": metric.id,
            "cpu_usage": metric.cpu_usage,
            "memory_percent": metric.memory_percent,
            "disk_percent": metric.disk_percent,
            "created_at": metric.created_at.isoformat(),
        }
        for metric in reversed(metrics)
    ]

    return JsonResponse({"metrics": data})

def dashboard(request):
    return render(request, "monitor/dashboard.html")