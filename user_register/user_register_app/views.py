from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages
cursor=connection.cursor()

import json
config_file = open('config.json', 'r')
config = json.load(config_file)
HOST = config.get('HOST', 'default_host_value')

@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_add = request.POST.get('email_add')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        query = "INSERT INTO user_reg (first_name, last_name, email_add, contact, password) VALUES (%s, %s, %s, %s, %s)"
        
        with connection.cursor() as cursor:
            cursor.execute(query, [first_name, last_name, email_add, contact, password])
        
        messages.success(request, "Registration successful.")
        return redirect(f'{HOST}:8000/')
    return render(request, "user_reg.html")
