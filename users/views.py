from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import requests
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, Http404
from django.contrib.auth import load_backend, login
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required 
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from games.models import PlayedGame
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url, urlsafe_base64_decode

from django.contrib.auth import get_user_model
User = get_user_model()

from wallets.models import AddFund
from wallets.models import WalletHistory
from games.models import Game

from uuid import uuid4
from random import randint
import logging

from allauth.account.views import SignupView
from django.contrib.auth import load_backend, login
from .models import User
from level.models import UserTotal
from .forms import SimpleSignupForm
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import random
from users.models import User
from level.models import UserTotal
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect, QueryDict

from django.http import JsonResponse
import datetime
from django.utils import timezone
from level.models import LevelIncomeSettings
import requests

logger = logging.getLogger('django')

@login_required
def coming_soon(request):
    return render(request, 'users/coming_soon.html')

def lockscreen(request):
    return render(request, 'account/lockscreen.html')


def customlogin(request):
    """
    Displays the login form and handles the login action.
    """
    print('hello')

    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print("auth",str(authenticate(username=username, password=password)))

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect('/games/parameters/')
            else:
                message = 'User Not Active'
                return render(request, 'account/login2.html', {'message': message})
        else:
            message = 'User Matching Query Does not Exists'
            return render(request, 'account/login2.html', {'message': message})
    else:
        return render(request, 'account/login2.html', {})

@login_required
def signuponboarding(request):
    user = request.user
    try:
        ruser = User.objects.get(username=user.referral)
    except Exception as e:
        ruser = 'blank'
    return render(request, 'users/onboarding.html', {'user': user, 'ruser': ruser})

@login_required
def records(request):
    user = request.user
    try:
        ruser = User.objects.get(username=user.referral)
    except Exception as e:
        ruser = 'blank'
    return render(request, 'users/dashboard.html', {'user': user, 'ruser': ruser})

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

class SearchListView(ListView):
    model = User
    template_name = "/users/password_reset_done.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["hide_search"] = True
        context["user"] = (
            get_user_model()
            .objects.get(Q(username__iexact=query) | Q(mobile__iexact=query))
        )
        
        return context

def referalsignup(request, use):
    logout(request)
    user = User.objects.get(username=use)
    user_name = user.name
    if request.method == 'POST':
        form = SimpleSignupForm()
        if form.is_valid():
            form.save()
            return redirect('/signup/onboarding/')
    else:
        form = SimpleSignupForm()
    return render(request, 'account/refersignup.html', {'form': form, 'user':user, 'name':user_name})

def vendorsignup(request):
    logout(request)
    if request.method == 'POST':
        form = SimpleSignupForm()
        if form.is_valid():
            form.save()
            return redirect('/panel/')
    else:
        form = SimpleSignupForm()
    return render(request, 'account/vendorsignup.html', {'form': form})


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name", "email", "mobile", "address", "city", "state"
    ]
    model = User
    
    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:update")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_context_data(self, *args, **kwargs):
        self.request.session['user_id'] = self.request.user.username
        context = super().get_context_data(*args, **kwargs)
        amount = 0
        try:
            levelp = UserTotal.objects.get(user=self.request.user)
        except Exception as e:
            levelp = 'None'

        user = User.objects.get(username=self.request.user)
        try:
            s = UserTotal.objects.get(user=user.username)
        except Exception as e:
            s = e
        
        context["s"] = s
        return context


class UserDashboardView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = 'users/user_dashboard.html'
    def get_context_data(self, *args, **kwargs):
        self.request.session['user_id'] = self.request.user.username
        context = super().get_context_data(*args, **kwargs)
        amount = 0
        try:
            levelp = UserTotal.objects.get(user=self.request.user)
        except Exception as e:
            levelp = 'None'

        user = User.objects.get(username=self.request.user)
        try:
            s = UserTotal.objects.get(user=user.username)
        except Exception as e:
            s = e
        directs = UserTotal.objects.filter(direct=user).count()

        
        context["games"] = Game.objects.all()
        return context


class profile(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/profile.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class recharge(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/recharge.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class moneytransfer(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/moneytransfer.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class addamount(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/addamount.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class transferamount(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/transferamount.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class binarytree(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/binarytree.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class directteam(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/directteam.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class zoneincome(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/zoneincome.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class mynetwork(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/mynetwork.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class paymentoptions(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/paymentoptions.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class activationrequest(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/activationrequest.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class withdrawalhistory(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/withdrawalhistory.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class incomehistory(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/incomehistory.html'
    slug_field = "username"
    slug_url_kwarg = "username"

class changepassword(LoginRequiredMixin, ListView):
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User
    template_name = 'users/changepassword.html'

@login_required
def loginbonus(request):
    user = request.user
    if user.login_bonus == True:
        return redirect('/users/')
    else:
        user.login_bonus = True
        user.income += 0.02

        benewallet = WalletHistory()
        benewallet.user_id = str(request.user)
        benewallet.amount = 0.02
        benewallet.type = "credit"
        benewallet.comment = "received for login bonus"

        benewallet.save()
        user.save()
    return render(request, 'index.html', {})

@login_required
def passcode(request):
    user = request.user
    if request.method == 'POST':
        passcode = request.POST.get('otp')
        user.otp = passcode
        user.save()
        return render(request, 'users/passcoded.html', {})
    return render(request, 'users/passcode.html', {})

@login_required
def booking(request):
    try:
        shopping = Shopping.objects.get(user=str(request.user))
    except Exception as e:
        shopping = 'blank'
    try:
        nuser = User.objects.get(username=request.user.referal)
    except Exception as e:
        nuser = 'blank'
    if nuser != 'blank':
        if nuser.username == 'JR1002':
            nuser = 'blank'
    message = ''
    if request.method=='POST':
        if request.POST.get('wallet_use') == 'on':
            if request.user.new_funds >= 1500:
                user = request.user
                user.new_funds -= 1500
                user.save()
                w = WalletHistory()
                w.user_id = user.username
                w.amount = 1500.00
                w.filter = "Add"
                w.comment = "Shopping Wallet Topup"
                w.type = "credit"
                w.save()
                w = WalletHistory()
                w.user_id = request.user.username
                w.amount = 1500.00
                w.filter = "Add"
                w.comment = "Shopping Topup, Wallet Debit".format(user.username)
                w.type = "debit"
                w.save()
                r = user
                r.cash_back += 1500.00
                r.save()
                model, created = Shopping.objects.get_or_create(user=user)
                model, created = Shopping.objects.get_or_create(user=user)
                if model.amount >= float(1000):
                    model.amount = 1500
                    model.expire_at += timezone.timedelta(days=70)
                    model.plan = 70
                else:
                    model.amount = 1500
                    model.expire_at = timezone.now() + timezone.timedelta(days=70)
                    model.plan = 70
                model.save()
                message = 'Your Shopping wallet updated!'
                p = 'Thankyou'
            else:
                message = 'Please add Money first!'
            return render(request, 'franchise/thankyou.html', {'message': message, 'p': p})
        else:
            if 'upline' in request.POST:
                upline = request.POST.get('upline')
                try:
                    upline = User.objects.get(username=upline)
                except Exception as e:
                    upline = 'blurrr'
                if upline == 'blurrr':
                    return render(request, 'users/shop_wallet.html', {'form': OrderForm(request.POST.copy()), 'message': message, 'shopping': shopping, 'nuser': nuser, })
                else:
                    Shopping.objects.get_or_create(user=request.user.username, direct=upline.username)
            r = request.POST.copy()
            r.update({'txnid': uuid4().hex,
                'productinfo': 'package'})
            order_form = OrderForm(r)
            print(order_form.errors)
            if order_form.is_valid():
                print('if2')
                amount = request.POST.get('amount')
                # if request.user.is_superuser:
                amount = 1500.00
                initial = order_form.cleaned_data
                initial.update({'key': settings.PAYU_INFO['merchant_key'],
                                'surl': 'https://www.jrindia.co.in'+reverse('users:success'),
                                'furl': 'https://www.jrindia.co.in'+reverse('users:failure'),
                                'service_provider': 'payu_paisa',
                                'firstname': request.user.username,
                                'email': request.user.email,
                                'phone': request.POST.get('mobile'),
                                'amount': request.POST.get('amount'),
                                'curl': 'https://www.jrindia.co.in'+reverse('users:cancel')})
                if 'upline' in request.POST:
                    initial.update({'lastname': request.POST.get('upline')})
                initial.update({'hash': generate_hash(initial)})
                payu_form = PayUForm(initial)
                print(payu_form.errors)
                if payu_form.is_valid():
                    context = {'form': payu_form,'action': "%s" % settings.PAYU_INFO['payment_url'], 'nuser': nuser, }
                    return render(request, 'payments/payu_form.html', context)
    initial = {'txnid': uuid4().hex,
            'productinfo': 'Shopping wallet'}
    order_form = OrderForm(initial=initial)
    context = {'form': order_form, 'message': message, 'shopping': shopping, 'nuser': nuser}
    return render(request, 'users/shop_wallet.html', context)

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
            added = int(float(data["net_amount_debit"]))
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
        AddMoney.objects.get(user=data.get('firstname'), txnid=txnid)
    except AddMoney.DoesNotExist:
        a = 'blank'
    except AddMoney.MultipleObjectsReturned:
        a = 'exists'
    if a == 'blank': 
        b = AddMoney()
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
        w = WalletHistory()
        w.user_id = data.get("firstname")
        w.amount = 1500.00
        w.filter = "Add"
        w.comment = "Shopping Wallet Topup"
        w.type = "credit"
        w.save()
        r = User.objects.get(username=data.get("firstname"))
        r.cash_back += 1500.00
        r.save()
        model, created = Shopping.objects.get_or_create(user=data.get("firstname"))
        model, created = Shopping.objects.get_or_create(user=data.get("firstname"))
        if model.amount >= 1500:
            model.amount = 1500
            model.expire_at  = model.expire_at + datetime.timedelta(70)
            model.plan = 70
        else:
            model.amount = 1500
            model.expire_at = datetime.datetime.now() + datetime.timedelta(70)
            model.plan = 70
        model.save()
        
    context = {"txnid":txnid,"status":status,"amount":amount, 'data':data, 'added':added}
    return render(request, 'tops.html', context)

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

def validate_username(request):
    username = request.GET.get('username', None)
    print(username)
    try:
        u = User.objects.get(username=username).name
    except Exception as e:
        u = 'Sorry Username Does not Exists or {}'.format(e)
    data = {
        'is_taken': u
    }
    return JsonResponse(data)


def bets(request):
    bets = PlayedGame.objects.filter(user=request.user.username).order_by('-id')
    print(bets)
    return render(request, 'users/bets.html', {'bets': bets})