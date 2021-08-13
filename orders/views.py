from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, Http404
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import reverse
from payu.utils import generate_hash, verify_hash
from django.contrib.auth.decorators import login_required 

from django.contrib.auth import get_user_model
User = get_user_model()

from payu.forms import PayUForm
from orders.forms import OrderForm
from wallets.models import AddFund
from wallets.models import WalletHistory

from uuid import uuid4
from random import randint
import logging

logger = logging.getLogger('django')

@login_required
def checkout(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            user = request.user
            amount = request.POST.get('amount')
            initial = order_form.cleaned_data
            initial.update({'key': settings.PAYU_INFO['merchant_key'],
                            'surl': 'http://13.127.121.200'+reverse('orders:success'),
                            'furl': 'http://13.127.121.200'+reverse('orders:failure'),
                            'service_provider': 'payu_paisa',
                            'firstname': user.username,
                            'email': user.email,
                            'phone': user.mobile,
                            'amount': amount,
                            'curl': 'http://13.127.121.200'+reverse('orders:cancel')})
            # Once you have all the information that you need to submit to payu
            # create a payu_form, validate it and render response using
            # template provided by PayU.
            print(initial)
            initial.update({'hash': generate_hash(initial)})
            payu_form = PayUForm(initial)
            print(payu_form.errors)
            if payu_form.is_valid():
                context = {'form': payu_form,'action': "%s" % settings.PAYU_INFO['payment_url']}
                return render(request, 'payments/payu_form.html', context)
    else:
        initial = {'txnid': uuid4().hex,
                'productinfo': 'JR Add Money'}
        order_form = OrderForm(initial=initial)
    context = {'form': order_form}
    return render(request, 'payments/checkout.html', context)

import hashlib
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_protect
@csrf_exempt
def success(request):
    if request.method == 'POST':
        if 'status' in request.POST:
            c = {}
            c.update(csrf(request))
            status=request.POST["status"]
            firstname=request.POST["firstname"]
            amount=request.POST["amount"]
            txnid=request.POST["txnid"]
            posted_hash=request.POST["hash"]
            key=request.POST["key"]
            productinfo=request.POST["productinfo"]
            email=request.POST["email"]
            salt=settings.PAYU_INFO['merchant_salt']
            data = request.POST
            added = float(data.get("net_amount_debit"))
    try:
        additionalCharges=request.POST["additionalCharges"]
        retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    except Exception:
        retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
    hashh=hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    if(hashh !=posted_hash):
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ",txnid)
        print("We have received a payment of Rs. ", amount ,". Your order will soon be shipped.")
    a = 'None'
    try:
        AddFund.objects.get(user=data.get('firstname'), txnid=txnid)
    except AddFund.DoesNotExist:
        a = 'blank'
    except AddFund.MultipleObjectsReturned:
        a = 'exists'
    if a == 'blank': 
        b = AddFund()
        b.postBackParamId = data.get("postBackParamId")
        b.mihpayid = data.get("mihpayid")
        b.paymentId = data.get("paymentId")
        b.mode = data.get("mode")
        b.status = data.get("status")
        b.unmappedstatus = data.get("unmappedstatus")
        b.key = data.get("key")
        b.txnid = data.get("txnid")
        b.amount= data.get("amount")
        b.addedon= data.get("addedon")
        b.createdOn= data.get("createdOn")
        b.productinfo = data.get("productinfo")
        b.firstname= data.get("firstname")
        b.lastname = data.get("lastname")
        b.address1 = data.get("address1")
        b.address2 = data.get("address2")
        b.city = data.get("city")
        b.state = data.get("state")
        b.country = data.get("country")
        b.zipcode = data.get("zipcode")
        b.email = data.get("email")
        b.phone = data.get("phone")
        b.hash = data.get("hash")
        b.field1 = data.get("field1")
        b.field2 = data.get("field2")
        b.field3 = data.get("field3")
        b.field4 = data.get("field4")
        b.field5 = data.get("field5")
        b.field6 = data.get("field6") 
        b.field7 = data.get("field7")
        b.field8 = data.get("field8")
        b.field9  = data.get("field9")
        b.PG_TYPE = data.get("PG_TYPE")
        b.bank_ref_num = data.get("bank_ref_num")
        b.bankcode = data.get("bankcode")
        b.error = data.get("error")
        b.error_Message = data.get("error_Message")
        b.cardToken = data.get("cardToken")
        b.name_on_card = data.get("name_on_card")
        b.cardnum = data.get("cardnum")
        b.postUrl = data.get("postUrl")
        b.calledStatus = data.get("calledStatus")
        b.additional_param = data.get("additional_param")
        b.amount_split = data.get("amount_split")
        b.net_amount_debit = data.get("net_amount_debit")
        b.paisa_mecode = data.get("paisa_mecode")
        b.meCode = data.get("meCode")
        b.payuMoneyId = data.get("payuMoneyId")
        b.encryptedPaymentId = data.get("encryptedPaymentId")
        b.baseUrl = data.get("baseUrl")
        b.retryCount = data.get("retryCount")
        b.isConsentPayment = data.get("isConsentPayment")
        b.S2SPbpFlag = data.get("S2SPbpFlag")
        b.giftCardIssued = data.get("giftCardIssued")
        b.user = data.get("firstname")
        b.save()
        r = User.objects.get(username=data.get("firstname"))
        r.wallet += float(data.get("amount"))
        r.save()
        w = WalletHistories()
        w.user_id = data.get("firstname")
        w.amount = data.get("amount")
        w.filter = "added"
        w.comment = "fund added to wallet"
        w.type = "credit"
        w.save()
    context = {"txnid":txnid,"status":status,"amount":amount, 'data':data, 'added':added}
    return render(request, 'payments/sucess.html', context)

@csrf_protect
@csrf_exempt
def failure(request):
    if request.method == 'POST':
        return render(request, 'payments/failure.html')
    else:
        raise Http404

@csrf_protect
@csrf_exempt
def cancel(request):
    if request.method == 'POST':
        return render(request, 'payments/cancel.html')
    else:
        raise Http404