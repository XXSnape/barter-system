from rest_framework import serializers
from ads.models import ExchangeProposal


class CreateExchangeProposalSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = ExchangeProposal
        fields = (
            "id",
            "ad_sender",
            "ad_receiver",
            "comment",
        )


class ReadOrUpdateExchangeProposalSerializer(
    CreateExchangeProposalSerializer,
):
    class Meta:
        model = ExchangeProposal
        fields = (
            "id",
            "ad_sender",
            "ad_receiver",
            "comment",
            "status",
        )
