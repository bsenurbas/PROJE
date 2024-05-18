from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    min_bmi = models.FloatField()
    max_bmi = models.FloatField()

    @classmethod
    def create_from_settings(cls):
        categories = {
            'Zayıf': (0, 18.5),
            'Normal': (18.5, 24.9),
            'Fazla Kilolu': (25, 29.9),
            'Obez': (30, 100),
        }
        for name, (min_bmi, max_bmi) in categories.items():
            cls.objects.create(name=name, min_bmi=min_bmi, max_bmi=max_bmi) 
    def __str__(self):
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
    goal = models.CharField(max_length=100)
    ingredients = models.TextField()
    list = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    note = models.TextField()
    exercise = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name