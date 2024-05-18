from django.contrib import admin
from django.urls import path, include
from pages.views import HomePageView, custom_login, register, user_page, contact_page,user_page,custom_login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('user/', user_page, name='user_page'),
    path('', HomePageView.as_view(), name='home'),
    path('iletisim/', contact_page, name='contact_page'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]