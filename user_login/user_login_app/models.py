from django.db import models
from django.contrib.auth.models import AbstractUser
import pyotp

class Login(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)

