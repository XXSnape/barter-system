from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ads.models import Ad, ExchangeProposal
from ads.serializers import (
    AdSerializer,
    CreateExchangeProposalSerializer,
    ReadOrUpdateExchangeProposalSerializer,
)
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


class ExchangeProposalViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "create":
            return CreateExchangeProposalSerializer
        return ReadOrUpdateExchangeProposalSerializer

    def get_queryset(self):
        queryset = (
            ExchangeProposal.objects.prefetch_related(
                "ad_sender",
                "ad_receiver",
            )
            .select_related("ad_receiver__user")
            .filter(ad_receiver__user=self.request.user)
            .all()
        )
        return queryset
