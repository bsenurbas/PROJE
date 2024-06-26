from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

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
    name = models.CharField(max_length=255)
    sabah = models.TextField()
    ara_ogun_1 = models.TextField()
    ogle = models.TextField()
    ara_ogun_2 = models.TextField()
    aksam = models.TextField()
    gece = models.TextField()
    notlar = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    min_bmi = models.FloatField(default=0) 
    max_bmi = models.FloatField(default=50)

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    note = models.TextField()
    pazartesi = models.TextField()
    salı = models.TextField()
    çarşamba = models.TextField()
    perşembe = models.TextField()
    cuma = models.TextField()
    cumartesi = models.TextField()
    pazar = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    min_bmi = models.FloatField(default=0)  
    max_bmi = models.FloatField(default=50)

    def __str__(self):
        return self.name

from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
