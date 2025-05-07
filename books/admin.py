from django.contrib import admin
from .models import Book, City, CartItem

admin.site.register(Book)
admin.site.register(City)
admin.site.register(CartItem)