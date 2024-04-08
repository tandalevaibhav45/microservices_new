from django.contrib import admin
from django.urls import path,include
from .views import login_view,verify_otp,send_otp
urlpatterns = [
    # path('send_otp/', send_otp, name='send_otp'),
    #     path('verify_user/', verify_user, name='verify_user'),
        path('', login_view, name='login'),
        path('send_otp', send_otp, name='send_otp'),
        path('verify_otp/<int:pk>', verify_otp, name='verify_otp'),

]