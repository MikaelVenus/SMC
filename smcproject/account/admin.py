from django.contrib import admin

# Register your models here.
from .models import Menu, Booking, Customer, Item, Supplier, Location

admin.site.register(Menu)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(Supplier)
admin.site.register(Location)