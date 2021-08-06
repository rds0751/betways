from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.html import mark_safe
 
# Create your models here.
class Beneficiary(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True)
    bene_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    vpa = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    ifsc = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

class WalletHistory(models.Model):
    user_id = models.CharField(max_length=20)
    amount = models.FloatField()
    balance = models.IntegerField(blank=True, default=0)
    type = models.CharField(max_length=12, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    filter = models.CharField(max_length=255)
    txnid = models.CharField(max_length=12, blank=True, null=True)

class AddFund(models.Model):
    postBackParamId  = models.CharField(max_length=200, null=True, blank=True)
    mihpayid  = models.CharField(max_length=200, null=True, blank=True)
    paymentId  = models.CharField(max_length=200, null=True, blank=True)
    mode  = models.CharField(max_length=200, null=True, blank=True)
    status  = models.CharField(max_length=200, null=True, blank=True)
    unmappedstatus  = models.CharField(max_length=200, null=True, blank=True)
    key  = models.CharField(max_length=200, null=True, blank=True)
    txnid  = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    addedon = models.CharField(max_length=200, null=True, blank=True)
    createdOn= models.CharField(max_length=200, null=True, blank=True)
    productinfo  = models.CharField(max_length=200, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname  = models.CharField(max_length=200, null=True, blank=True)
    address1  = models.CharField(max_length=200, null=True, blank=True)
    address2  = models.CharField(max_length=200, null=True, blank=True)
    city  = models.CharField(max_length=200, null=True, blank=True)
    state  = models.CharField(max_length=200, null=True, blank=True)
    country  = models.CharField(max_length=200, null=True, blank=True)
    zipcode  = models.CharField(max_length=200, null=True, blank=True)
    email  = models.CharField(max_length=200, null=True, blank=True)
    phone  = models.CharField(max_length=200, null=True, blank=True)
    hash  = models.CharField(max_length=200, null=True, blank=True)
    field1  = models.CharField(max_length=200, null=True, blank=True)
    field2= models.CharField(max_length=200, null=True, blank=True)
    field3  = models.CharField(max_length=200, null=True, blank=True)
    field4 = models.CharField(max_length=200, null=True, blank=True)
    field5= models.CharField(max_length=200, null=True, blank=True)
    field6= models.CharField(max_length=200, null=True, blank=True)
    field7 = models.CharField(max_length=200, null=True, blank=True)
    field8  = models.CharField(max_length=200, null=True, blank=True)
    field9   = models.CharField(max_length=200, null=True, blank=True)
    PG_TYPE  = models.CharField(max_length=200, null=True, blank=True)
    bank_ref_num  = models.CharField(max_length=200, null=True, blank=True)
    bankcode  = models.CharField(max_length=200, null=True, blank=True)
    error  = models.CharField(max_length=200, null=True, blank=True)
    error_Message = models.CharField(max_length=200, null=True, blank=True)
    cardToken  = models.CharField(max_length=200, null=True, blank=True)
    name_on_card  = models.CharField(max_length=200, null=True, blank=True)
    cardnum  = models.CharField(max_length=200, null=True, blank=True)
    postUrl= models.CharField(max_length=200, null=True, blank=True)
    calledStatus  = models.CharField(max_length=200, null=True, blank=True)
    additional_param  = models.CharField(max_length=200, null=True, blank=True)
    amount_split= models.CharField(max_length=200, null=True, blank=True)
    net_amount_debit  = models.CharField(max_length=200, null=True, blank=True)
    paisa_mecode  = models.CharField(max_length=200, null=True, blank=True)
    meCode = models.CharField(max_length=200, null=True, blank=True)
    payuMoneyId  = models.CharField(max_length=200, null=True, blank=True)
    encryptedPaymentId  = models.CharField(max_length=200, null=True, blank=True)
    baseUrl = models.CharField(max_length=200, null=True, blank=True)
    retryCount  = models.CharField(max_length=200, null=True, blank=True)
    isConsentPayment  = models.CharField(max_length=200, null=True, blank=True)
    S2SPbpFlag  = models.CharField(max_length=200, null=True, blank=True)
    giftCardIssued = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=30, null=True, blank=True)

class PaymentOption(models.Model):
    user = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    ifsc = models.CharField(max_length=255, blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    mt5_account = models.CharField(max_length=50, blank=True, null=True)
    verification = models.ImageField()
    status = models.NullBooleanField(null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.user

    def pan_image(self):
        return mark_safe('<img src="{}" width="400" />'.format(self.verification.url))


class Withdrawal(models.Model):
    user = models.CharField(max_length=20)
    amount = models.FloatField()
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    total_amount = models.FloatField()
    admin_fees = models.FloatField()
    tax = models.FloatField()
    comment = models.CharField(max_length=250)
    name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    ifsc = models.CharField(max_length=255, blank=True, null=True)


class FundRequest(models.Model):
    user = models.CharField(max_length=20)
    amount = models.FloatField()
    approved = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    code = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.code + ' for amount ' + str(self.amount) + ' on ' + str(self.created_at) + ' by ' + self.user