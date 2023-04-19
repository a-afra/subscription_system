from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    credit = models.FloatField(default=100.0)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.FloatField()