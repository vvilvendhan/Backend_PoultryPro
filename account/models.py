from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
import os, base64
from django.conf import settings
# Create your models here.


class CustomUserManager(BaseUserManager):
    
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to "is_staff=Ture".')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must be assigned to "is_superuser=Ture".')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,**other_fields)
        user.set_password(password)
        user.save()
        return user
    

class Country(models.Model):
    iso = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    nicename = models.CharField(max_length=200)
    phonecode = models.CharField(max_length=10)
    numcode = models.CharField(max_length=10, null=True, blank=True)
    sort_order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.nicename



class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        (1,'Male'),
        (2,'Female'),
        (3,'Other'),
    )
    ROLE_CHOICES = (
        (1,'Admin'),
        (2,'Manager'),
        (3,'Staff'),
    )

    PLATFORM_CHOICE = (
        (None, '------'),
        (1, 'Android'),
        (2, 'iOS'),
        (3, 'Web')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    email = models.EmailField(unique=True, null=True, blank=True)
    proxy_mail = models.EmailField(unique=True, null=True, blank=True)
    phone_no = models.CharField(max_length=15, blank=True,null=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    phone_code = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200, blank=True,null=True)
    username =models.CharField(max_length=100,blank=True,null=True, unique=True)
    dob = models.DateField(blank=True,null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES,blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profile/', null=True, blank=True)
    contact_id = models.CharField(max_length=20, null=True, blank=True)
    date_joined =models.DateTimeField(auto_now_add=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_secret = models.CharField(max_length=200, null=True, blank=True)
    jwt_session_id = models.CharField(max_length=100, blank=True, null=True, editable=False)
    login_count = models.PositiveSmallIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    test_user = models.BooleanField(default=False)
    track_status = models.BooleanField(default=True)
    phone_language = models.CharField(max_length=100, blank=True, null=True)
    platform = models.PositiveSmallIntegerField(choices=PLATFORM_CHOICE, null=True, blank=True)
    feedback_mail_sent  = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
   
    def __str__(self):
        return self.email or self.proxy_mail or self.phone or 'Anonymous'