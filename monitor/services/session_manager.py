
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

def stop_session(session_id):
    session = MonitoringSession.objects.filter(
        pk=session_id,
        status=MonitoringSession.Status.RUNNING
    ).first()

    if session is None:
        return None

    session.status = MonitoringSession.Status.STOPPED
    session.ended_at = timezone.now()

    session.save(update_fields=[
        "status",
        "ended_at",
    ])

    return session

def update_heartbeat(session_id):
    session = MonitoringSession.objects.filter(
        pk=session_id,
        status=MonitoringSession.Status.RUNNING
    ).first()

    if session is None:
        return False

    session.last_heartbeat = timezone.now()
    session.save(update_fields=["last_heartbeat"])

    return True

def recover_stale_sessions():
    """
    サーバー再起動後に残っている監視中セッションを終了扱いにする。
    """
    now = timezone.now()

    count = MonitoringSession.objects.filter(
        status=MonitoringSession.Status.RUNNING
    ).update(
        status=MonitoringSession.Status.STOPPED,
        ended_at=now
    )

    if count > 0:
        print(f"[MONITOR] 異常終了セッションを復旧: {count}件")

    return count