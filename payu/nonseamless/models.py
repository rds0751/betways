from __future__ import unicode_literals
import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class NonSeamlessTransaction(models.Model):

    RESPONSE = [
        ('N', 'New'),
        ('W', 'Awaiting Confirmation'),
        ('S', 'Success'),
        ('F', 'Failure'),
        ('C', 'Cancelled'),
    ]

    txnid = models.CharField(max_length=32, db_index=True)
    productinfo = models.CharField(_('Product info'), max_length=1000)
    amount = models.DecimalField(_('Amount Paid'), max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(_('Currency'), max_length=8, null=True, blank=True)
    basket = models.CharField(_('Basket'), max_length=12, null=True, blank=True, db_index=True)
    credit_used = models.DecimalField(_('Credit Used'), max_digits=12, decimal_places=2, null=True, blank=True)

    firstname = models.CharField(_('First Name'), max_length=32, null=True, blank=True)
    lastname = models.CharField(_('Last Name'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=12, null=True, blank=True)
    address1 = models.CharField(_('Address 1'), max_length=48, null=True, blank=True)
    address2 = models.CharField(_('Address 2'), max_length=48, null=True, blank=True)
    city = models.CharField(_('City'), max_length=32, null=True, blank=True)
    state = models.CharField(_('State'), max_length=32, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=32, null=True, blank=True)
    zipcode = models.CharField(_('Zip Code'), max_length=8, null=True, blank=True)
    udf1 = models.CharField(max_length=255, null=True, blank=True)
    udf2 = models.CharField(max_length=255, null=True, blank=True)
    udf3 = models.CharField(max_length=255, null=True, blank=True)
    udf4 = models.CharField(max_length=255, null=True, blank=True)
    udf5 = models.CharField(max_length=255, null=True, blank=True)
    pg = models.CharField(max_length=8, null=True, blank=True)
    drop_category = models.CharField(_('Drop Category'), max_length=32, null=True, blank=True)
    custom_note = models.CharField(_('Custom Note'), max_length=128, null=True, blank=True)
    note_category = models.CharField(_('Note Category'), max_length=32, null=True, blank=True)
    offer_key = models.CharField(_('Offer Key'), max_length=32, null=True, blank=True)
    raw_response = models.TextField(_('Raw Response'), max_length=1024)
    raw_request = models.TextField(_('Raw Request'), max_length=1024)
    error_code = models.CharField(_('Error Code'), max_length=32, null=True, blank=True)
    error_message = models.CharField(_('Error Message'), max_length=128, null=True, blank=True)
    response = models.CharField(_('Response'), choices=RESPONSE, max_length=2, null=True, blank=True)
    orderid = models.CharField(_('Order ID'), max_length=32, null=True, blank=True)
    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('Date Updated'), auto_now=True)

    class Meta:
        ordering = ('-date_created',)
        app_label = 'payu'

    @property
    def is_successful(self):
        return self.response in ('S',)

    def status(self):
        return self.response

    def __str__(self):
        return '{}-{}'.format(self.txnid, self.orderid)
