from django.db import IntegrityError

from finance.exceptions import PaymentAlreadyProcessedError
from finance.models import Payment
from .base import BasePaymentHandler


class BankPaymentHandler(BasePaymentHandler):
    payment_system_name = 'bank'

    def validate(self) -> None:
        operation_id = self.payload.get("operation_id")
        if Payment.objects.filter(operation_id=operation_id).exists():
            raise PaymentAlreadyProcessedError()

    def process_payment(self) -> Payment:
        try:
            payment = Payment.objects.create(
                operation_id=self.payload["operation_id"],
                wallet_id=self.wallet_id,
                amount=self.payload["amount"],
                payment_system_name=self.payment_system_name
            )
        except IntegrityError:
            raise PaymentAlreadyProcessedError()
        return payment
