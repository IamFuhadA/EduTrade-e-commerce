from django.contrib import admin
from .models import Category, Book, Accessory
# Register your models her

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Accessory)