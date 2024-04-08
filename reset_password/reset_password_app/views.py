from django.shortcuts import render,redirect
import math
import random
import smtplib 
from .encrypt_folder import password_security
from email.mime.text import MIMEText
from django.db import connection
cursor = connection.cursor()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages
import json
config_file = open('config.json', 'r')
config = json.load(config_file)
HOST = config.get('HOST', 'default_host_value')
APP_CODE = config.get('APP_CODE', 'default_app_code')
SENDER_MAIL = config.get('SENDER_MAIL', 'default_sender_email@example.com')
SMTP_SERVER = config.get('SMTP_SERVER', 'default_smtp_server')
SMTP_PORT = config.get('SMTP_PORT', "default_smtp_server")  

def reset_pass(request):
    if request.method == "POST":
        digits="0123456789"
        OTP=""
        for index in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        
        mail = request.POST.get('email')
        query_ = f"select email_add from user_registration.user_reg where email_add = '{mail}';"
        cursor.execute(query_)
        similar_mail = cursor.fetchone()
        if similar_mail!=None and similar_mail[0] == mail :
            sender_email = SENDER_MAIL
            receiver_email = mail
            subject = "Reset Password"
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
            server.login(sender_email, APP_CODE) 
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            request.session['otp']=OTP
            request.session['mail']=mail
            return redirect(f"{HOST}:8002/otp_verify")
        else:
            messages.error(request,"OTP does not send")

    return render(request, 'reset_password.html')
            
            
def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')    
        new_password = request.POST.get('newpass')
        repeat_password = request.POST.get('confirmpass')
        mail__= request.session['mail']
        x=otp
        if x == request.session['otp']:
            if new_password == repeat_password:
                query_for_update_pass = "update user_registration.user_reg set password=%s where email_add=%s"
                query=(new_password,mail__)
                cursor.execute(query_for_update_pass,query)
                connection.commit()
                del request.session['otp']
                return redirect(f'{HOST}:8000/')
            else:
                return render(request,"reset_password.html")
        else:
            return render(request,"reset_password.html")
    return render(request,"reset_otp_verify.html")