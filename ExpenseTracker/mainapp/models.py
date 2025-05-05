from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random

class UserManager(BaseUserManager):
    def create_user(self, email, name, username, number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, username=username, number=number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, username, email, name, number, password=None):
        user = self.create_user(username, email, name, number, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'number']

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()




class Feedback(models.Model):
    email = models.EmailField()
    message = models.TextField()
    is_user = models.BooleanField(default=False)  # To track if the user is a registered user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.email} - {self.created_at}"
    
