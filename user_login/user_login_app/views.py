from django.conf import settings
from twilio.rest import Client
from rest_framework.response import Response
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib import messages
from django.db import connection
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import math
import random
import json
config_file = open('config.json', 'r')
config = json.load(config_file)
HOST = config.get('HOST', 'default_host_value')
APP_CODE = config.get('APP_CODE', 'default_app_code')
SENDER_MAIL = config.get('SENDER_MAIL', 'default_sender_email@example.com')
SMTP_SERVER = config.get('SMTP_SERVER', 'default_smtp_server')
SMTP_PORT = config.get('SMTP_PORT', "default_smtp_server")  

config_file.close()
cursor=connection.cursor()

def login_view(request):
    if request.method == "POST":
        email_add = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = f"SELECT id ,first_name, email_add, password FROM user_registration.user_reg WHERE first_name = '{username}' AND email_add = '{email_add}' AND password = '{password}';"
        with connection.cursor() as cursor:
            cursor.execute(query)
            data=cursor.fetchone()
        if data:
            send_otp(request,email_add)
            return redirect(f'{HOST}:8000/verify_otp/{data[0]}')
        else:
            messages.error(request,"Invalid credentials")
    

    return render(request,"login.html")

def send_otp(request,mail):

    digits="0123456789"
    OTP=""
    for index in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    query_ = f"select email_add from user_registration.user_reg where email_add = '{mail}';"
    cursor.execute(query_)
    similar_mail = cursor.fetchone()
    if similar_mail!=None and similar_mail[0] == mail :
        sender_email = SENDER_MAIL
        receiver_email = mail
        subject = "OTP Verification"
        body = f"This is your OTP: {OTP}. Do not share it with anyone."

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        smtp_server = SMTP_SERVER
        smtp_port = SMTP_PORT

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, f"{APP_CODE}") 
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        request.session['otp'] = OTP
        return OTP
    else:
        messages.error(request,"OTP does not send")
            
            
def verify_otp(request,pk=0):
    if request.method == 'POST':
        otp = request.POST.get('otp')  
        x=otp
        if x == request.session['otp']:
            del request.session['otp']
            messages.info(request,"Log in successfully!")
            return render(request,"login_inside.html",{'pk':pk})
        else:
            messages.error(request,"Invalid OTP")
            return render(request,"login.html")
    return render(request,"login_verify_otp.html")