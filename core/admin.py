from django.contrib import admin
from .models import Customer, Reservation, Order, Item

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Reservation)
admin.site.register(Item)
