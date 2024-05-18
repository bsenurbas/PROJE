from django.contrib import admin
from .models import Recipe
from .models import Category
from .models import Workout

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Workout)
