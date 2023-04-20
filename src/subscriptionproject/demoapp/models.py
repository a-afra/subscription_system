from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Customer(AbstractUser):
    credit = models.FloatField(default=100.0)

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'customer {self.customer.username} {self.plan.name} plan'


class Invoice(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.FloatField()

    def __str__(self):
        return f'invoice {self.id} for {self.subscription.customer.username}'

    """def save(self, *args, **kwargs):
        # update start and end date before saving
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(minutes=10)
        # calculate amount based on subscription price
        self.amount = self.subscription.plan.price
        super().save(*args, **kwargs)"""