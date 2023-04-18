from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField()

class Subscription(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)