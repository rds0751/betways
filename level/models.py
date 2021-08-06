from django.db import models
from datetime import datetime
from django.utils import timezone


class Activation(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    amount = models.IntegerField()
    paid_by = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    utr_number = models.CharField(max_length=255, blank=True, null=True)
    reciept_number = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to='activation/', null=True)
    status = models.CharField(max_length=8)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class LevelIncomeSettings(models.Model):
    level = models.IntegerField()
    amount = models.IntegerField()
    name = models.CharField(max_length=125, null=True, blank=True)
    return_amount = models.IntegerField()
    expiration_period = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

class UserTotal(models.Model):
    user = models.CharField(max_length=25, blank=True, null=True)
    level = models.ForeignKey(LevelIncomeSettings, on_delete=models.CASCADE)
    active = models.BooleanField()
    left_months = models.IntegerField()
    direct = models.CharField(max_length=25, blank=True, null=True)
    business = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    def ccm_ends(self):
        activated_at = self.activated_at
        try:
            if activated_at + timezone.timedelta(days=7) <= timezone.now():
                return 'gone'
            return activated_at + timezone.timedelta(days=7)
        except Exception as e:
            return 'not active'

    def plan_ends(self):
        activated_at = self.activated_at
        try:
            if activated_at + timezone.timedelta(days=self.left_months*30) <= timezone.now():
                return 'gone'
            return activated_at + timezone.timedelta(days=self.left_months*30)
        except Exception as e:
            return 'not active'

    def __str__(self):
        return str(self.user) 