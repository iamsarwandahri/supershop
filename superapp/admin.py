from django.contrib import admin
from .models import Product, OrderItem, Order, Countries, Customer, Contact, Checkout


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Countries)
admin.site.register(Contact)
admin.site.register(Checkout)
