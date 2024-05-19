from django.urls import path
from .views import HomePageView, register, diets_page, training_page, recipies_page, get_bmi_recommendation, recipe_detail, workout_detail
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),  
    path("register/", register, name="register"),  
    path('diyet/', diets_page, name='diets_page'), 
    path('egzersiz/', training_page, name='training_page'), 
    path('tarifler/', recipies_page, name='recipies_page'), 
    path('bmi-recommendations/', get_bmi_recommendation, name='bmi_recommendations'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('workout/<int:pk>/', workout_detail, name='workout_detail'),
]
