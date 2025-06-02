import uuid

from django.db import models


class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=2, max_digits=20)
    currency = models.CharField(max_length=3, default='RUB')

    class Meta:
        db_table = 'finance_wallets'


class Payment(models.Model):
    operation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    payment_system_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finance_payments'


class BalanceLog(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finance_balance_logs'
