"""FoodBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='receipies'),
    path('recipe-single/', views.recipe_single, name='recipe-single'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('forget_password_user/', views.forget_password_user, name='forget_password_user'),
    path('forget_password_otp/', views.forget_password_otp, name='forget_password_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),

    path('update_profile_user/', views.update_profile_user, name='update_profile_user'),
    path('change_password_user/', views.change_password_user, name='change_password_user'),

    path('logout/', views.logout, name='logout'),
]
