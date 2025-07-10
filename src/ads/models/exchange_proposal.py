from django.db import models

from .ad import Ad


class ExchangeProposal(models.Model):
    ad_sender = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="ad_senders",
    )
    ad_receiver = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name="ad_receivers",
    )
    comment = models.TextField()
    status = models.CharField(
        choices={
            ("ожидает", "ожидает"),
            ("ожидает", "принято"),
            ("отклонено", "отклонено"),
        },
        default="ожидает",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ad_sender", "ad_receiver"],
                name="unique_sender_receiver",
            ),
            models.CheckConstraint(
                check=~models.Q(ad_sender=models.F("ad_receiver")),
                name="ad_sender_ne_ad_receiver",
            ),
        ]
