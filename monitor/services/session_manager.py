
from django.utils import timezone

from monitor.models import MonitoringSession


def get_active_session():
    """現在実行中の監視セッションを取得する"""
    return MonitoringSession.objects.filter(
        status=MonitoringSession.Status.RUNNING
    ).order_by("-started_at").first()


def start_session():
    """監視セッションを開始する"""
    session = get_active_session()

    # すでに監視中なら既存のセッションを返す
    if session is not None:
        return session

    return MonitoringSession.objects.create(
        status=MonitoringSession.Status.RUNNING
    )


def stop_session():
    """監視セッションを停止する"""
    session = get_active_session()

    if session is None:
        return None

    session.status = MonitoringSession.Status.STOPPED
    session.ended_at = timezone.now()
    session.save(update_fields=["status", "ended_at"])

    return session
