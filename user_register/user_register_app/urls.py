from django.contrib import admin
from django.urls import path,include
from .views import user_register

urlpatterns = [
    path('',user_register, name= 'user_register') # home page for user registration
]