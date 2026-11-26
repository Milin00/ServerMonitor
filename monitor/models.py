from django.db import models


class MonitoringSession(models.Model):
    """PCの監視セッションを管理するモデル"""

    class Status(models.TextChoices):
        RUNNING = "running", "監視中"
        STOPPED = "stopped", "停止"

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="監視開始日時"
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="監視終了日時"
    )

    last_heartbeat = models.DateTimeField(
    null=True,
    blank=True,
    verbose_name="最終生存通知日時"
    )
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.RUNNING,
        verbose_name="監視状態"
    )
    

    def __str__(self):
        return f"Session #{self.pk} ({self.status})"

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "監視セッション"
        verbose_name_plural = "監視セッション"


class SystemMetric(models.Model):

    session = models.ForeignKey(
        MonitoringSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="metrics",
        verbose_name="監視セッション"
    )

    cpu_usage = models.FloatField()

    memory_percent = models.FloatField()
    memory_used = models.FloatField()
    memory_total = models.FloatField()

    disk_percent = models.FloatField()
    disk_used = models.FloatField()
    disk_total = models.FloatField()

    bytes_sent = models.BigIntegerField()
    bytes_recv = models.BigIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'システム監視データ'
        verbose_name_plural = 'システム監視データ'

    def __str__(self):
        return f"SystemMetric {self.created_at}"