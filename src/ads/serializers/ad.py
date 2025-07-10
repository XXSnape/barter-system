from rest_framework import serializers

from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "image_url",
            "category",
            "condition",
            "created_at",
            "username",
        )
