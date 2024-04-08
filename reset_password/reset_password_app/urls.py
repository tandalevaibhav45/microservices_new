from django.contrib import admin
from django.urls import path,include
from .views import reset_pass,otp_verify

urlpatterns = [
    path('',reset_pass, name = 'reset_pass'),
    path('otp_verify',otp_verify, name = 'otp_verify')
]