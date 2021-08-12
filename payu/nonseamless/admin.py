from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from payu import models


class ExpressTransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Cart Order Information'), {
            'classes': ('collapse',),
            'fields': (
                'txnid',
                'productinfo',
                'amount',
                'currency',
                'basket',
                'credit_used',
            )
        }),
        (_('Shipping Information'), {
            'classes': ('collapse',),
            'fields': (
                'orderid',
                'date_created',
                'date_updated',
            )
        }),
        (_('Client Information'), {
            'classes': ('collapse',),
            'fields': (
                'firstname',
                'lastname',
                'email',
                'phone',
                'address1',
                'address2',
                'city',
                'state',
                'country',
                'zipcode'
            ),
        }),
        (_('Seller Information'), {
            'classes': ('collapse',),
            'fields': (
                'udf1',
                'udf2',
                'udf3',
                'udf4',
                'udf5',
                'pg',
                'drop_category',
                'custom_note',
                'note_category',
                'offer_key'
            )
        }),
        (_('Transaction'), {
            'classes': ('collapse',),
            'fields': (
                'response',
                'raw_response',
                'raw_request',
                'error_code',
                'error_message'
            ),
        })
    ]

    readonly_fields = [
        'amount',
        'currency',
        'error_code',
        'error_message',
        'raw_request',
        'raw_response',
        'date_created',
        'date_updated',
        'response'
    ]

    list_display = [
        'amount',
        'currency',
        'error_code',
        'error_message',
        'date_created'
    ]

    list_filter = [
        'city',
        'country',
        'state'
    ]

admin.site.register(models.NonSeamlessTransaction, ExpressTransactionAdmin)
