from django.urls import path
from .views import HomePageView, register, diets_page, training_page, recipies_page, get_bmi_recommendation, recipe_detail, workout_detail, ipucu_page
from . import views
from .views import export_recipe
from .views import export_workout

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),  
    path("home", HomePageView.as_view(), name="home"), 
    path("register/", register, name="register"),  
    path('diyet/', diets_page, name='diets_page'), 
    path('egzersiz/', training_page, name='training_page'), 
    path('tarifler/', recipies_page, name='recipies_page'), 
    path('bmi-recommendations/', get_bmi_recommendation, name='bmi_recommendations'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('workout/<int:pk>/', workout_detail, name='workout_detail'),
    path('import/', views.import_data, name='import_data'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('export_recipe/<int:recipe_id>/', export_recipe, name='export_recipe'),
    path('export_workout/<int:workout_id>/', export_workout, name='export_workout'),
    path('ipucları/', ipucu_page, name='ipucu_page'),
]
