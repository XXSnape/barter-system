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

    def validate(self, data: dict) -> dict:
        if data["ad_sender"] == data["ad_receiver"]:
            raise serializers.ValidationError(
                "Объявления не могут обмениваться сами с собой", code=400
            )
        user = self.context["request"].user
        if data["ad_sender"].user != user:
            raise serializers.ValidationError(
                "Вы не можете отправить "
                "предложение обмена не на свое объявление",
                code=403,
            )
        if data["ad_receiver"].user == user:
            raise serializers.ValidationError(
                "Вы не можете отправить предложение обмена на свое объявление",
                code=403,
            )
        return data


class ReadExchangeProposalSerializer(
    serializers.ModelSerializer,
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


class UpdateExchangeProposalSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = ExchangeProposal
        fields = ("status",)
