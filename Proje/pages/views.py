from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import UserProfile, Recipe, Workout,Category, BlogPost ,UploadedFile
from django.contrib import messages
import pandas as pd
from .forms import UploadFileForm,BlogPostForm ,FileUploadForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
import csv

def export_workout(request, workout_id):
    # Veritabanından workout çekme
    workout = Workout.objects.get(id=workout_id)
    
    # HttpResponse nesnesi oluşturma
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{workout.name}.csv"'
    
    # CSV yazarı oluşturma
    writer = csv.writer(response)
    
    # CSV dosyasına veri yazma
    writer.writerow(['Açıklama:'])
    writer.writerow([workout.description])
    writer.writerow([''])
    writer.writerow(['Not:'])
    writer.writerow([workout.note])
    writer.writerow([''])
    writer.writerow(['Egzersiz:'])
    writer.writerow([workout.exercise])
    
    return response

def export_recipe(request, recipe_id):
    # Veritabanından tarifi çekme
    recipe = Recipe.objects.get(id=recipe_id)
    
    # HttpResponse nesnesi oluşturma
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{recipe.name}.csv"'
    
    # CSV yazarı oluşturma
    writer = csv.writer(response)
    
    # CSV dosyasına veri yazma
    writer.writerow(['Hedef:'])
    writer.writerow([recipe.goal])
    writer.writerow([''])
    writer.writerow(['Malzemeler:'])
    writer.writerow([recipe.ingredients])
    writer.writerow([''])
    writer.writerow(['Liste:'])
    writer.writerow([recipe.list])
    
    return response

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                birth_date=request.POST.get('birth_date')
            )
            login(request, user)  # Kullanıcıyı otomatik olarak giriş yaptırma
            return redirect('home')
    else:
        form = CustomUserCreationForm()
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

def ipucu_page(request):
    return render(request, 'ipucları.html')

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

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                data = pd.read_excel(file)  # Excel dosyasını yükleyin
                for index, row in data.iterrows():
                    BlogPost.objects.create(
                        title=row['Title'],  # Sütun adlarını değiştirin
                        content=row['Content'],  # Sütun adlarını değiştirin
                        created_at=row['Created_At']  # Sütun adlarını değiştirin
                    )
                messages.success(request, 'Veriler başarıyla yüklendi!')
            except Exception as e:
                messages.error(request, f'Hata oluştu: {e}')
            return redirect('import_data')
    else:
        form = UploadFileForm()
    return render(request, 'import_data.html', {'form': form})

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_create.html', {'form': form})

def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            UploadedFile.objects.create(file=request.FILES['file'])
            return redirect('file_list')  # Dosya yüklendikten sonra yönlendirme
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

def file_list(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        if file_id:
            try:
                file = UploadedFile.objects.get(id=file_id)
                file.file.delete()  # Dosya sisteminden sil
                file.delete()  # Veritabanından kaydı sil
                messages.success(request, 'Dosya başarıyla silindi.')
            except UploadedFile.DoesNotExist:
                messages.error(request, 'Dosya bulunamadı.')
        return redirect('file_list')

    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})