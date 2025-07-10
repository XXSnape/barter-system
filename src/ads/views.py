from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ads.models import Ad
from ads.serializers import AdSerializer
from .permissions import IsAuthorOrReadOnly


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.select_related("user").all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = (
        "title",
        "description",
    )
    filterset_fields = (
        "category",
        "condition",
    )

    def perform_create(
        self,
        serializer: AdSerializer,
    ):
        serializer.save(user=self.request.user)
