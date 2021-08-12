from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories, Withdrawals, Paymentoptions
from binary.models import BinaryTree
import datetime
from django.utils import timezone
from binary.models import Shopping
from pcard.models import ImageUploadModel
from django.db.models import F, Sum

class Command(BaseCommand):
    help = "Update Binary Data"

    def handle(self, *args, **options):
        all_shop = Shopping.objects.all()
        all_user = User.objects.all()
        all_user.update(imps_daily=0)
        all_shop.update(today_level_income=0, today_self_income=0)
        onhold_users = User.objects.all().annotate(on_hold=Sum(F('income') + F('binary_income') + F('added_amount') + F('received_amount'))).filter(on_hold__gte=10)
        for x in onhold_users:
            user_id = x
            y = x
            amount = 10
            if user_id.income <= amount:
                amount = amount - user_id.income
                user_id.income = 0
                if user_id.binary_income <= amount:
                    amount = amount - user_id.binary_income
                    user_id.binary_income = 0
                    if user_id.added_amount <= amount:
                        amount = amount - user_id.added_amount
                        user_id.added_amount = 0
                        if amount != 0:
                            user_id.received_amount = user_id.received_amount - amount
                            amount = 0
                    else:
                        user_id.added_amount = user_id.added_amount - amount
                        amount = 0
                else:
                    user_id.binary_income = user_id.binary_income - amount
                    amount = 0
            else:
                user_id.income = user_id.income - amount
                amount = 0
            user_id.save()
            y.new_funds += 10
            y.save()
        
        def sendshopping(user):
            s = user
            try:
                sx = Shopping.objects.get(user=s)
                userid = User.objects.get(username=s)
            except Exception as e:
                input('wrong {}'.format(e))
            

            def finduplines(puser):
                try:
                    user = Shopping.objects.get(user=str(puser))
                    upline = user.direct
                except Shopping.DoesNotExist:
                    upline = 'blank'
                return upline

            levels70 = {
            'level1': 5,
            'level2': 3,
            'level3': 2,
            'level4': 1,
            'level5': 1,
            'level6': 1,
            'level7': 1,
            }
            
            level = 0
            try:
                rect = Shopping.objects.get(user=s.direct)
            except Exception as e:
                rect = 'blank'
            upline_user = rect
            uplines = [upline_user, ]
            while level < 6 and upline_user != 'blank':
                upline_user = finduplines(str(upline_user))
                uplines.append(upline_user)
                level += 1

            level = 1
            for upline in uplines:
                try:
                    upline_user = User.objects.get(username=upline)
                    sp = Shopping.objects.get(user=str(upline_user))
                    directs = Shopping.objects.filter(amount__gt=1499, direct=str(upline_user)).count()
                except Exception as e:
                    upline_user = 'blank'
                    directs = 0
                if upline_user != 'blank' and directs >= level and sp.today_level_income <= 40000 and sp.amount >= 1500:
                    upline_amount = levels70['level{}'.format(level)]
                    upline_user.new_funds += upline_amount*0.9
                    upline_user.total_income  += upline_amount
                    upline_wallet = WalletHistories()
                    upline_wallet.user_id = upline
                    upline_wallet.amount = upline_amount
                    upline_wallet.balance_after = upline_user.new_funds + upline_user.added_amount + upline_user.received_amount + upline_user.shopping_wallet + upline_user.income + upline_user.binary_income
                    upline_wallet.type = "credit"
                    upline_wallet.comment = "Shopping Income from Level {}".format(level)
                    sp.today_level_income += upline_amount
                    sp.total_level_income += upline_amount
                    sp.save()
                    upline_user.save()
                    upline_wallet.save()
                level = level + 1
        
        start_date = datetime.datetime.now() + datetime.timedelta(-1000)
        end_date = datetime.datetime.now()
        oldids = Shopping.objects.filter(expire_at__range=(start_date, end_date))
        for odv in oldids:
            odv.amount = 0
            odv.save()

        newids = Shopping.objects.filter(amount__gte=1500)
        self.stdout.write('{} jobs to complete'.format(newids.count()))
        p = 0
        level = 0
        for idv in newids:
            p += 1
            level += 1
            amount = idv.amount
            expiry_date = idv.expire_at
            user = User.objects.get(username=idv.user)
            total_income = user.income + user.binary_income + user.added_amount + user.received_amount + user.new_funds + user.shopping_wallet
            if True: 
                sendshopping(idv)
                directs = Shopping.objects.filter(amount__gte=1499, direct=str(idv.user)).count()
                try:
                    sx = Shopping.objects.get(user=idv.user)
                    userid = User.objects.get(username=idv.user)
                except Exception as e:
                    input('wrong {}'.format(e))
                if True:
                    sx.today_self_income = 50
                    sx.total_self_income += 50
                    sx.save()
                    user.shopping_wallet += 50*0.9
                    user.balance_after = total_income + 50*0.9
                    user.total_income += 50
                    usewallet = WalletHistories()
                    usewallet.user_id = str(userid)
                    usewallet.amount = 50
                    usewallet.type = "credit"
                    usewallet.comment = "Shopping Self Earning"
                    user.save()
                    usewallet.save()
                try:
                    prime = BinaryTree.objects.get(user=user.username).active
                except Exception as e:
                    prime = False
                if directs > idv.extra:
                    if sx.total_self_income + sx.total_level_income < 8000 or prime:
                        count = directs - idv.extra
                        x = 0
                        while x <= count:
                            print(user, user.shopping_wallet)
                            if user.shopping_wallet > 500:
                                print('iffffffffff')
                                x = user.shopping_wallet
                                y = user.new_funds
                                v = user
                                v.new_funds += 500
                                v.save()
                                user.shopping_wallet = x - 500
                                user.save()
                                idv.extra += 1
                                idv.save()
                                x += 1
                            else:
                                print('eeeeeeeelse')
                                x += 1
                print(sx.total_level_income, sx.total_self_income, sx)
                if sx.total_self_income + sx.total_level_income > 8000 and user.new_funds > 1999 and not prime:
                    try:
                        prime_id = BinaryTree.objects.get(user=user.username)
                    except Exception as e:
                        print(e, user)
                        prime_id = BinaryTree.objects.get(user='JR1002')
                    prime_id.active = True
                    user_p = user
                    user_p.new_funds -= 1999
                    user_p.cash_back += 2000
                    user_p.save()
                    prime_id.save()
                print('{} job/s completed with directs {} and user {}'.format(level, directs, user))
        # neftusers = Users.objects.filter(new_funds__gte=1500)
        # for user in neftusers:
            withuser = user
            amount = withuser.new_funds
            amount = amount/100
            amount = int(amount)*100
            try:
                payment_o = Paymentoptions.objects.get(user=withuser)
                kyc = ImageUploadModel.objects.get(user=withuser)
                verify = True
            except Exception as e:
                verify = False
            if withuser.new_funds >= 500 and verify==True and withuser.auto_neft:
                if kyc.approved==True and payment_o.status == True:
                    withuser.new_funds -= amount
                    withuser.save()
                    usewalletp = WalletHistories()
                    usewalletp.user_id = str(userid)
                    usewalletp.amount = amount
                    usewalletp.type = "debit"
                    usewalletp.comment = "Auto NEFT"
                    usewalletp.save()
                    model = Withdrawals()
                    model.user = withuser
                    model.amount = amount
                    model.status = 'pending'
                    model.total_amount = 0.95*amount
                    model.admin_fees = 0
                    model.tax = 0.05*amount
                    model.comment = 'pending'
                    model.name = payment_o.name
                    model.account_number = payment_o.account_number
                    model.ifsc = payment_o.ifsc
                    model.save()
        self.stdout.write('job complete')