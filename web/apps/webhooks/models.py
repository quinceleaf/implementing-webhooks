from django.db import models


class WebhookMessage(models.Model):
    received_at = models.DateTimeField(help_text="When event was received")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]
