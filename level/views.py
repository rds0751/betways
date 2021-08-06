import os
import razorpay

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
    lll = level
    user = User.objects.get(username=user)
    try:
        s = UserTotal.objects.get(user=user.username)
    except Exception as e:
        s = e
    directs = UserTotal.objects.filter(direct=user, active=True).count()
    level1 = UserTotal.objects.filter(direct=user.username).order_by('id')
    level1n = []
    for x in level1:
        level1n.append(x)
    level2n = []
    for y in level1n:
        level2 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level2:
            level2n.append(z)
    level3n = []
    for y in level2n:
        level3 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level3:
            level3n.append(z)
    level4n = []
    for y in level3n:
        level4 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level4:
            level4n.append(z)
    level5n = []
    for y in level4n:
        level5 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level5:
            level5n.append(z)
    level6n = []
    for y in level5n:
        level6 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level6:
            level6n.append(z)
    level7n = []
    for y in level6n:
        level7 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level7:
            level7n.append(z)
    level8n = []
    for y in level7n:
        level8 = UserTotal.objects.filter(direct=y).order_by('id')
        for z in level8:
            level8n.append(z)

    all_levels = [level1n, level2n, level3n, level4n, level5n, level6n, level7n, level8n]
    all_users = level1n
    counting = {}
    level = 0
    for a in all_levels:
        level += 1
        counting['{}'.format(level)] = len(a)

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

    business = {}
    level = 0
    for a in all_levels:
        level += 1
        b = 0
        for x in a:
            b += x.level.amount
        # business['{}'.format(level)] = b*levels['level{}'.format(level)]
        business['{}'.format(level)] = b

    l1 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 1', user_id=user.username)).exclude(comment__icontains='not')
    l2 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 2', user_id=user.username)).exclude(comment__icontains='not')
    l3 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 3', user_id=user.username)).exclude(comment__icontains='not')
    l4 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 4', user_id=user.username)).exclude(comment__icontains='not')
    l5 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 5', user_id=user.username)).exclude(comment__icontains='not')
    l6 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 6', user_id=user.username)).exclude(comment__icontains='not')
    l7 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 7', user_id=user.username)).exclude(comment__icontains='not')
    l8 = WalletHistory.objects.filter(Q(comment__icontains='Upgrade', user_id=user.username) and Q(comment__icontains='level 8', user_id=user.username)).exclude(comment__icontains='not')
    l1c = 0
    for x in l1:
        l1c += x.amount
    l2c = 0
    for x in l2:
        l2c += x.amount
    l3c = 0
    for x in l3:
        l3c += x.amount
    l4c = 0
    for x in l4:
        l4c += x.amount
    l5c = 0
    for x in l5:
        l5c += x.amount
    l6c = 0
    for x in l6:
        l6c += x.amount
    l7c = 0
    for x in l7:
        l7c += x.amount
    l8c = 0
    for x in l8:
        l8c += x.amount

    lc = [0, l1c, l2c, l3c, l4c, l5c, l6c, l7c, l8c]
    level1i = UserTotal.objects.filter(direct=user.username, active=True).order_by('id')
    level1ni = []
    for x in level1i:
        level1ni.append(x)
    level2ni = []
    for y in level1n:
        level2i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level2i:
            level2ni.append(z)
    level3ni = []
    for y in level2n:
        level3i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level3i:
            level3ni.append(z)
    level4ni = []
    for y in level3n:
        level4i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level4i:
            level4ni.append(z)
    level5ni = []
    for y in level4n:
        level5i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level5i:
            level5ni.append(z)
    level6ni = []
    for y in level5n:
        level6i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level6i:
            level6ni.append(z)
    level7ni = []
    for y in level6n:
        level7i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level7i:
            level7ni.append(z)
    level8ni = []
    for y in level7n:
        level8i = UserTotal.objects.filter(direct=y, active=True).order_by('id')
        for z in level8i:
            level8ni.append(z)

    all_levelsi = [level1ni, level2ni, level3ni, level4ni, level5ni, level6ni, level7ni, level8ni]
    all_usersi = level1ni
    countingi = {}
    leveli = 0
    for a in all_levelsi:
        leveli += 1
        countingi['{}'.format(leveli)] = len(a)

    user_list = []
    for u in all_users:
        try:
            user = User.objects.get(username=u.user)
            user_list.append(user)
        except Exception as e:
            pass

    level2n = level2n
    level2nu = []
    for u in level2n:
        try:
            user = User.objects.get(username=u.user)
            level2nu.append(user)
        except Exception as e:
            pass
    level3n = level3n
    level3nu = []
    for u in level3n:
        try:
            user = User.objects.get(username=u.user)
            level3nu.append(user)
        except Exception as e:
            pass
    level4n = level4n
    level4nu = []
    for u in level4n:
        try:
            user = User.objects.get(username=u.user)
            level4nu.append(user)
        except Exception as e:
            pass
    level5n = level5n
    level5nu = []
    for u in level5n:
        try:
            user = User.objects.get(username=u.user)
            level5nu.append(user)
        except Exception as e:
            pass
    level6n = level6n
    level6nu = []
    for u in level6n:
        try:
            user = User.objects.get(username=u.user)
            level6nu.append(user)
        except Exception as e:
            pass
    level7n = level7n
    level7nu = []
    for u in level7n:
        try:
            user = User.objects.get(username=u.user)
            level7nu.append(user)
        except Exception as e:
            pass
    level8n = level8n
    level8nu = []
    for u in level8n:
        try:
            user = User.objects.get(username=u.user)
            level8nu.append(user)
        except Exception as e:
            pass
    all_ = [zip(level2n, level2nu), zip(level3n, level3nu), zip(level4n, level4nu), zip(level5n, level5nu), zip(level6n, level6nu), zip(level7n, level7nu), zip(level8n, level8nu),]
    user_listi = []
    for u in all_usersi:
        try:
            user = User.objects.get(username=u.user)
            user_listi.append(user)
        except Exception as e:
            pass

    return render(request, 'level/tree.html', {'lll': lll, 'all': all_, 'lc': lc, 'counting': counting, 'directs': directs, 'business': business, 'countingi': countingi, 'user_':user, 'user_list': zip(user_list, all_users), 'user_listi':user_listi, 's': s,})

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
