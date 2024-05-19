from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import UserProfile, Recipe, Workout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                birth_date=request.POST['birth_date']
            )
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_page')
        else:
            return redirect('register')  
    else:
        return render(request, 'login.html')

class HomePageView(TemplateView):
    template_name = 'home.html'

from django.contrib.auth.decorators import login_required

@login_required
def user_page(request):
    username = request.user.username
    return render(request, 'user.html', {'username': username})

def diets_page(request):
    return render(request, 'diyet.html')

def training_page(request):
    return render(request, 'training.html')

def recipies_page(request):
    return render(request, 'recipies.html')

def contact_page(request):
    return render(request, 'contact.html')

def get_bmi_recommendation(request):
    user_bmi = None
    recipes = []
    workouts = []

    if request.method == 'POST':
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        user_bmi = weight / (height ** 2)

        recipes = Recipe.objects.filter(min_bmi__lte=user_bmi, max_bmi__gte=user_bmi)
        workouts = Workout.objects.filter(min_bmi__lte=user_bmi, max_bmi__gte=user_bmi)

    context = {
        'user_bmi': user_bmi,
        'recipes': recipes,
        'workouts': workouts,
    }
    return render(request, 'bmi_recommendations.html', context)

def calculate_bmi(weight, height):
    height_meters = height / 100  # cm cinsinden gelen boyu metreye çeviriyoruz
    bmi = weight / (height_meters * height_meters)
    return bmi

