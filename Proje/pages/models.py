from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name 
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    height = models.FloatField(default=1.75)  # Boy metre cinsinden
    weight = models.FloatField(default=70)  # Kilo kilogram cinsinden

    @property
    def bmi(self):
        if self.height > 0:
            return self.weight / (self.height ** 2)
        return None

    def str(self):
        return self.user.username
    
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    min_bmi = models.FloatField()
    max_bmi = models.FloatField()

    def str(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    recipes = models.ManyToManyField(Recipe)
    min_bmi = models.FloatField()
    max_bmi = models.FloatField()

    def str(self):
        return self.name