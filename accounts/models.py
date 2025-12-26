from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class DematAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit_balance = models.FloatField(default=0)
    wallet_balance = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class CarbonCreditType(models.Model):
    name = models.CharField(max_length=100)
    price_per_credit = models.FloatField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='buyer_tx', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller_tx', on_delete=models.CASCADE)
    credit_type = models.ForeignKey(CarbonCreditType, on_delete=models.CASCADE)
    credits = models.FloatField()
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
