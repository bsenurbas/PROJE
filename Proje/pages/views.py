from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import UserProfile

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
