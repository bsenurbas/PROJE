from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import UserProfile, Recipe, Workout,Category

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
    category = None
    recipes = []
    workouts = []

    if request.method == 'POST':
        try:
            height = float(request.POST.get('height'))
            weight = float(request.POST.get('weight'))
            user_bmi = weight / (height ** 2)

            category = Category.objects.filter(min_bmi__lte=user_bmi, max_bmi__gte=user_bmi).first()
            if category:
                recipes = Recipe.objects.filter(category=category)
                workouts = Workout.objects.filter(category=category)
        except (ValueError, TypeError):
            user_bmi = None

    context = {
        'user_bmi': user_bmi,
        'category': category,
        'recipes': recipes,
        'workouts': workouts,
    }
    return render(request, 'bmi_recommendations.html', context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    return render(request, 'workout_detail.html', {'workout': workout})
