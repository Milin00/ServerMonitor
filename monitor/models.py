from django.db import models


class SystemMetric(models.Model):
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