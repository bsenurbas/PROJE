from django.contrib import admin
from django.urls import path, include
from pages.views import HomePageView, custom_login, register, user_page, contact_page,user_page,custom_login


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('user/', user_page, name='user_page'),
    path('', HomePageView.as_view(), name='home'),
    path('iletisim/', contact_page, name='contact_page'),
]
