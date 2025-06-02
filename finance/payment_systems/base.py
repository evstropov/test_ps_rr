from abc import ABC, abstractmethod
from typing import Any, Dict

from django.db import transaction, models

from finance.models import Payment, BalanceLog, Wallet


class BasePaymentHandler(ABC):
    payment_system_name = None

    def __init__(self, wallet_id: int, payload: Dict[str, Any]):
        self.wallet_id = wallet_id
        self.payload = payload

    @abstractmethod
    def validate(self) -> None:
        pass

    @abstractmethod
    def process_payment(self) -> Payment:
        pass

    def update_wallet_balance(self) -> None:
        wallet = Wallet.objects.select_for_update().get(id=self.wallet_id)
        wallet.balance = models.F("balance") + self.payload["amount"]
        wallet.save(update_fields=["balance"])

    def save_log(self, payment: Payment) -> None:
        BalanceLog.objects.create(
            payment_id=payment.pk,
            payload=self.payload,
        )

    def process(self):
        self.validate()
        with transaction.atomic():
            payment = self.process_payment()
            self.update_wallet_balance()
            self.save_log(payment)
