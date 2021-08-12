from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories
from binary.models import BinaryTree
import datetime

class Command(BaseCommand):
    help = "Update Binary Data"

    def handle(self, *args, **options):
        def sendmatching(user, level, amount):
            level += 1
            try:
                upline = BinaryTree.objects.get(user=str(user.upline_user_id))
                next_position = upline.position
            except BinaryTree.DoesNotExist:
                upline = 'blank'

            if level <= 10 and upline != 'blank':
                uplinen = '123'
                try:
                    upline_user = User.objects.get(username=str(upline.user))
                    balance_before = User.objects.get(username=str(upline.user)).binary_income
                    direct_left = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='left').count()
                    direct_right = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='right').count()
                    u = False
                except Exception as e:
                    u = True
                    upline_user = User.objects.get(username='JR1002')


                if upline_user.today_binary_income <= 180000 and u != True:
                    rank = upline_user.total_users_left + upline_user.total_users_right
                    if level==1 and rank >= 0:
                        upline_user.new_funds += 0.2*float(amount)
                        upline_user.total_income += 0.2*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.2*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.2*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 1'.format(level)
                        

                    elif level==2 and rank >= 2:
                        upline_user.new_funds += 0.1*float(amount)
                        upline_user.total_income += 0.1*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.1*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.1*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 2'.format(level)
                        
                        

                    elif level==3 and rank >= 3:
                        upline_user.new_funds += 0.05*float(amount)
                        upline_user.total_income += 0.05*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.05*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.05*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 3'.format(level)
                        
                        

                    elif level==4 and rank >= 4:
                        upline_user.new_funds += 0.03*float(amount)
                        upline_user.total_income += 0.03*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.03*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.03*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 4'.format(level)
                        
                        

                    elif level==5 and rank >= 5:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 5'.format(level)
                        
                        

                    elif level==6 and rank >= 6:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 6'.format(level)
                        
                        

                    elif level==7 and rank >= 7:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 7'.format(level)
                        
                        

                    elif level==8 and rank >= 8:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 8'.format(level)
                        
                        

                    elif level==9 and rank >= 9:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 9'.format(level)
                        
                        

                    elif level==10 and rank >= 10:
                        upline_user.new_funds += 0.02*float(amount)
                        upline_user.total_income += 0.02*float(amount)
                        balance_after = upline_user.new_funds
                        upline_user.today_binary_income += 0.02*float(amount)
                        

                        user_wallet = WalletHistories()
                        user_wallet.user_id = str(upline_user)
                        user_wallet.balance_before = balance_before
                        user_wallet.balance_after = balance_after
                        user_wallet.amount = 0.02*float(amount)
                        user_wallet.type = 'credit'
                        user_wallet.comment = 'Income from Level 10'.format(level)

                    upline_user.save()
                    user_wallet.save()
                sendmatching(upline, level, amount)
            else:
                level = 0
                return level
                
        start_date = datetime.datetime.now() + datetime.timedelta(-1)
        end_date = datetime.datetime.now()
        newtxns = WalletHistories.objects.filter(created_at__range=(start_date, end_date), comment="Matching Income")
        self.stdout.write('{} jobs to complete'.format(newtxns.count()))
        p = 0
        for idv in newtxns:
            p+=1
            nidv = BinaryTree.objects.get(user=idv.user_id)
            amount = idv.amount
            level = 0
            level  = sendmatching(nidv, level, amount)
            self.stdout.write('{} job/s completed'.format(p))


        self.stdout.write( 'job complete' )