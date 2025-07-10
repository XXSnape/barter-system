from rest_framework import viewsets

from ads.models import Ad
from ads.serializers import AdSerializer
from .permissions import IsAuthorOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.select_related("user").all()
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(
        self,
        serializer: AdSerializer,
    ):
        serializer.save(user=self.request.user)
