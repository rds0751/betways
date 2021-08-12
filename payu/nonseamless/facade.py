from __future__ import unicode_literals

from hashlib import sha512 
from uuid import uuid4

from django.conf import settings
from .models import NonSeamlessTransaction

KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
        'udf9', 'udf10')

PAYU_INFO = settings.PAYU_INFO


def generate_hash(data, salt):
    keys = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
            'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
            'udf9',  'udf10')
    sash=''
    for key in keys:
        sash+="%s%s" % (str(data.get(key, '')), '|')
    sash+=settings.PAYU_INFO.get('merchant_salt')
    hash = sha512(sash.encode('utf-8'))
    return hash.hexdigest().lower()


def verify_hash(data, salt):
    """
    Generates sha512 of received data fields in following format.
    sha512(SALT|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)
    """
    # KEYS_REVERSED = KEYS[::-1]
    # hash_sum = sha512('')
    # hash_sum.update(salt)
    # hash_sum.update("%s%s" % ('|', str(data.get('status', ''))))
    # for key in KEYS_REVERSED:
    #     hash_sum.update("%s%s" % ('|', str(data.get(key, ''))))
    # return hash_sum.hexdigest().lower() == str(data.get('hash', ''))
    HashSeq = salt+'|'+data.get('status')+'|||||||||||'+data.get('email')+'|'+data.get('firstname')+'|'+data.get('productinfo')+'|'+data.get('amount')+'|'+data.get('txnid')+'|'+data.get('key')
    hash = sha512(HashSeq.encode('utf-8'))
    # for key in keys:
    #     sash+="%s%s" % (str(data.get(key, '')), '|')
    # sash+=settings.PAYU_INFO.get('merchant_salt')
    # hash = sha512(sash.encode('utf-8'))
    return (hash.hexdigest().lower() == data.get('hash'))


def get_payu_url():
    """
    Return the URL for a PayPal Express transaction.

    This involves registering the txn with PayPal to get a one-time
    URL.  If a shipping method and shipping address are passed, then these are
    given to PayPal directly - this is used within when using PayPal as a
    payment method.
    """
    return 'https://secure.payu.in/_payment'


def set_txn(request, basket, currency, email,  order_total_with_credit, order_total_without_credit, user_want_credit, user_address=None):
    if user_want_credit:
        user = basket.owner
        user_SCL = user.cash_back + user.secondary_cashback
        usable_credit = order_total_without_credit.excl_tax - order_total_with_credit.excl_tax
        if user_SCL >= usable_credit:
            SCL = usable_credit
        else:
            SCL = user_SCL
        payu_amount = order_total_without_credit.excl_tax - int(SCL)
    else:
        payu_amount = order_total_without_credit.excl_tax
        SCL = 0

    txn = NonSeamlessTransaction()
    txn.txnid = uuid4().hex[:28]
    txn.productinfo = basket.all_lines()[0].product.get_title()
    txn.amount = payu_amount
    txn.currency = currency
    txn.firstname = user_address.first_name
    txn.lastname = user_address.last_name
    txn.email = email
    txn.phone = '7000934949'
    txn.address1 = user_address.line1[:46]
    txn.address2 = user_address.line2[:46]
    txn.city = user_address.line4
    txn.state = user_address.state
    txn.country = user_address.country
    txn.zipcode = user_address.postcode
    txn.response = 'N'
    txn.basket = basket.id
    txn.credit_used = SCL
    txn.save()
    return txn 