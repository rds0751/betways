from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.utils.html import mark_safe


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=25, blank=True, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    is_superuser = models.BooleanField(blank=True, default=False)
    rank = models.CharField(max_length=44, null=True, blank=True)
    nominee = models.CharField(max_length=155, default='blank', blank=False)
    nominee_relation = models.CharField(max_length=155, default='blank', blank=False)
    profile_pic = models.FileField(upload_to='profile_pics/', null=True)
    otp = models.IntegerField(default='1234', null=True)
    referral = models.CharField(max_length=25, blank=True, null=True)
    wallet = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['name', 'referal', 'mobile']
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.name:
            return self.name