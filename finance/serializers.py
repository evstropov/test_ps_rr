from rest_framework import serializers

from organization.models import Organization


class BankPaymentWebhookSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    payer_inn = serializers.CharField(max_length=12)
    document_number = serializers.CharField(max_length=64)
    document_date = serializers.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        self._wallet_id = None
        super().__init__(*args, **kwargs)

    def validate_payer_inn(self, value):
        try:
            self._wallet_id = Organization.objects.filter(id=value).values_list('wallet_id', flat=True)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization does not exist")

    @property
    def wallet_id(self) -> int:
        if not self._wallet_id:
            raise AttributeError('Cannot access `.wallet_id` without validating serializer.')
        return self._wallet_id



