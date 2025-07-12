from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, ExchangeProposal
from ads.serializers import (
    AdSerializer,
    CreateExchangeProposalSerializer,
    ReadExchangeProposalSerializer,
    UpdateExchangeProposalSerializer,
)

from .permissions import IsAuthorOrReadOnly, IsReceiverOrSender


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
    permission_classes = (IsAuthenticated, IsReceiverOrSender)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "ad_sender",
        "ad_receiver",
        "status",
    )

    def get_serializer_class(self):
        if self.action == "create":
            return CreateExchangeProposalSerializer
        if self.action in ("update", "partial_update"):
            return UpdateExchangeProposalSerializer
        return ReadExchangeProposalSerializer

    def get_queryset(self):
        queryset = (
            ExchangeProposal.objects.select_related(
                "ad_sender",
                "ad_receiver",
                "ad_receiver__user",
                "ad_sender__user",
            )
            .filter(
                Q(
                    ad_receiver__user=self.request.user,
                )
                | Q(ad_sender__user=self.request.user)
            )
            .all()
        )
        return queryset
