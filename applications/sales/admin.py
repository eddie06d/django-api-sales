from django.contrib import admin
from applications.sales.models import Currency, Client, Order

# Register your models here.

admin.site.register(Currency)
admin.site.register(Client)
admin.site.register(Order)