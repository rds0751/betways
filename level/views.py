import os

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.contrib.auth import get_user_model 
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView, CreateView
from django.shortcuts import render, redirect
from users.models import User
from .models import Activation, LevelIncomeSettings, UserTotal
from django.contrib.auth.decorators import login_required
from wallets.models import WalletHistory, FundRequest
from django.core.paginator import Paginator
from panel.views import activate
from django.utils.crypto import get_random_string

class OtherListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "level/search_results_other.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["hide_search"] = True
        context["users_list"] = (
            get_user_model()
            .objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
            .distinct()
        )     
        return context

@login_required
def leveltree(request, user, level):
    referrals = User.objects.filter(referral=user)
    return render(request, 'binary/tree.html', {'referrals': referrals})

@login_required
def leveljoin(request):
    packages = LevelIncomeSettings.objects.all().exclude(id=9).order_by('amount')
    message = "Please Proceed with upgrade"

    def userjoined(user, level):
        try:
            user = UserTotal.objects.get(user=str(user))
        except Exception as e:
            user = 'blank'
        print(user)
        if user != 'blank':
            return False
        else:
            return True


    global packamount
    if request.method == 'POST':
        user=request.user
        upline_user = user.referral
        packamount = float(request.POST["amount"])
        userbal = request.POST.get('FRN')
        try:
            userbal = FundRequest.objects.get(code=userbal, used=False, approved=True).amount
        except Exception as e:
            userbal = 0
        levelp = LevelIncomeSettings.objects.get(amount=packamount)
        user_id = User.objects.get(username=str(user))
        userjoined = userjoined(request.user, levelp.level)
        if userbal >= packamount:
            if userjoined:
                frn = FundRequest.objects.get(code=request.POST.get('FRN'))
                frn.used = True
                userwallet = WalletHistory()
                userwallet.user_id = user_id
                userwallet.amount = float(request.POST["amount"])
                userwallet.type = "debit"
                userwallet.comment = "Prime Upgradation"

                userid = request.user   

                def finduplines(user):  
                    try:    
                        user = User.objects.get(username__iexact=str(user)) 
                        upline = user.referral   
                    except User.DoesNotExist:   
                        upline = 'blank'    
                    return upline   

                levels = {  
                'level1': 20/100,  
                'level2': 10/100, 
                'level3': 8/100, 
                'level4': 6/100, 
                'level5': 4/100, 
                'level6': 2/100, 
                'level7': 2/100, 
                'level8': 8/100,  
                }   

                level = 0   
                upline_user = userid.referral    
                userid = request.user   
                amount = packamount 
                uplines = [upline_user, ]
                while level < 7 and upline_user != 'blank':
                    upline_user = finduplines(str(upline_user))
                    uplines.append(upline_user)
                    level += 1

                level = 0
                print(uplines)
                for upline in uplines:
                    try:
                        upline_user = User.objects.get(username=upline) 
                    except Exception as e:
                        upline_user = 'blank'
                    if upline_user != 'blank':  
                        directs = UserTotal.objects.filter(direct=upline_user)
                        if request.user.referral == upline_user.username:
                            direct = True
                        else:
                            direct = False
                        if directs.count() >= level and direct:   
                            upline_amount = levels['level{}'.format(level+1)]*amount 
                            upline_user.wallet += upline_amount
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = upline  
                            upline_wallet.amount = upline_amount    
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "New Upgrade by your level {} user".format(level+1)  
                            upline_user.save()
                            upline_wallet.save()
                        elif directs.count() > level and not direct:   
                            upline_amount = levels['level{}'.format(level+1)]*amount 
                            upline_user.wallet += upline_amount
                            upline_wallet = WalletHistory()   
                            upline_wallet.user_id = upline  
                            upline_wallet.amount = upline_amount    
                            upline_wallet.type = "credit"   
                            upline_wallet.comment = "New Upgrade by your level {} user".format(level+1)  
                            upline_user.save()
                            upline_wallet.save()
                    level = level + 1
                
                model = UserTotal()
                model.user = userid
                model.level = levelp.level
                model.active = True
                model.left_months = levelp.expiration_period
                model.direct = request.user.referral
                model.save()
                userwallet.save()
                user_id.save()
                frn.save()
                return redirect('/level/team/{}/'.format(user_id))
            else:
                message = "user already joined, please upgrade another ID"
        else:
            message = "not enough available balance in fund request"
    else:
        message = ""
    return render(request, 'level/level_join.html', {'packages': packages, "message": message})

def activation(request):
    packages = LevelIncomeSettings.objects.all().exclude(id=9).order_by('amount')
    actp = Activation.objects.filter(user=request.user.username, status='Pending').count()
    acta = Activation.objects.filter(user=request.user.username, status='Approved').count()
    if request.method == "POST":
        if request.POST.get('type') == 'cash':
            amount = request.POST.get("amount")
            user = request.user
            act = Activation()
            act.user = user.username
            act.amount = amount
            act.status = 'Pending'
            act.comment = ''
            act.save()
            title = 'Thankyou!'
            message = 'Your activation for ${} is in pending, please wait for 24-48 hrs for activation'.format(amount)
            return render(request,"level/thankyou.html", {'title': title, 'message': message})
        else:
            amount = int(request.POST.get("amount"))
            user = request.user
            if user.c >= amount:
                usec = user
                usec.c -= amount
                act = Activation()
                act.user = user.username
                act.amount = amount
                act.status = 'Approved'
                act.comment = 'auto approved service balance'
                message = activate(user, amount)
                act.save()
                usec.save()
            else:
                message = "You dont have enough service balance"
                title = 'Please check the error'
                return render(request,"level/sorry.html", {'title': title, 'message': message})
            title = 'Thankyou!'
            return render(request,"level/thankyou.html", {'title': title, 'message': message})
    return render(request,"level/level_join.html", {'packages': packages, 'acta': acta, 'actp': actp})

def payment(request):
    def generateid():
        txnid = get_random_string(8)
        try:
            txn = WalletHistory.objects.get(txnid = txnid)
        except WalletHistory.DoesNotExist:
            txn = 0
        if txn:
            generateid()
        else:
            return txnid

    amount = int(int(request.POST.get('amounta'))*75 + 0.02*int(request.POST.get('amounta'))*75)
    user = request.user
    txnid = generateid()
    w = WalletHistory()
    w.user_id = user.username
    w.amount = int(request.POST.get('amounta'))
    w.comment = 'Money added using razorpay'
    w.txnid = txnid
    w.save()
    context = {'user': user, 'oid': txnid, 'amount': amount}
    return render(request,"level/joined.html",context)

@csrf_exempt
def payment_success(request):
    if request.method =="POST":
        status = request.POST.get('status')
        oid = request.POST.get('order_id')
        txnid = request.POST.get('txnid')
        w = WalletHistory.objects.get(txnid=oid)
        if status == 'SUCCESS':
            w.type = 'credit'
            w.comment += 'success with {}'.format(txnid)
            w.save()
            u = User.objects.get(username=w.user_id)
            u.c += w.amount
            u.save()
        else:
            w.type = 'credit'
            w.comment += 'Failed'
            w.save()
    return redirect('/users/')
