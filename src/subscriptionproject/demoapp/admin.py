from django.contrib import admin

from .models import Customer, Subscription, SubscriptionPlan, Invoice

admin.site.register(Customer)
admin.site.register(SubscriptionPlan)
admin.site.register(Subscription)
admin.site.register(Invoice)