from django.urls import path
from .views import HomePageView, register,diets_page,training_page,recipies_page
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),  
    path("register/", register, name="register"),  
    path('diyet/', diets_page, name='diets_page'), 
    path('egzersiz/', training_page, name='training_page'), 
    path('tarifler/', recipies_page, name='recipies_page'),
       
]
