from django.contrib import admin

from .models import Customer, Subscription, Invoice

admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Invoice)