from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    title = models.CharField(
        max_length=128,
    )
    description = models.TextField()
    image_url = models.URLField(
        max_length=512,
        null=True,
    )
    category = models.CharField(
        max_length=128,
    )
    condition = models.CharField(
        max_length=128,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
