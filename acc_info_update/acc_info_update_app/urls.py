from django.contrib import admin
from django.urls import path,include
from .views import get_update_info,do_update

urlpatterns = [
    path('get_update_info/<int:pk>',get_update_info, name = 'get_update_info'),
    path('get_update_info/do_update/<int:pk>',do_update, name = 'do_update')
]