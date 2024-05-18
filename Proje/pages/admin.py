from django.contrib import admin
from .models import Recipe
from .models import Category

admin.site.register(Category)
admin.site.register(Recipe)
