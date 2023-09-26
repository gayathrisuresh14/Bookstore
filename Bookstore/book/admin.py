from django.contrib import admin
from .models import Book, Genre, Order, Cart, CartItems, Contact

# Register your models here.

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Contact)
