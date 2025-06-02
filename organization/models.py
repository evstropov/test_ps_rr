from django.db import models

from finance.models import Wallet


class Organization(models.Model):
    tin = models.CharField(max_length=12, db_index=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    class Meta:
        db_table = 'organizations'