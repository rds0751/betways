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
        # all_users = User.objects.all()
        # all_users.update(today_binary_income=0)

        def sendmatching(user, idv, position, amount):
            try:
                upline = BinaryTree.objects.get(user=str(user.upline_user_id))
                next_position = upline.position
            except BinaryTree.DoesNotExist:
                upline = 'blank'

            

            if upline != 'blank':
                
                upline_user = User.objects.get(username=str(upline.user))
                level = 0
                uplinen = 0
                while uplinen != upline:
                    uplinen = BinaryTree.objects.get(user=str(user.upline_user_id))
                    level+=1

                balance_before = User.objects.get(username=str(upline.user)).binary_income

                direct_left = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='left').count()
                direct_right = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='right').count()

                
                if True:
                    # send according to 1:1
                    if position == 'left':
                        upline_user.total_users_left += 1
                        if upline_user.total_users_right >= upline_user.total_users_left:
                            if upline_user.today_binary_income <= 180000:
                                upline_user.new_funds += 0.9*200
                                upline_user.total_income += 200
                                balance_after = upline_user.new_funds
                                upline_user.today_binary_income += 200

                                user_wallet = WalletHistories()
                                user_wallet.user_id = str(upline_user)
                                user_wallet.balance_before = balance_before
                                user_wallet.balance_after = balance_after
                                user_wallet.amount = 200
                                user_wallet.type = 'credit'
                                user_wallet.comment = 'Matching Income'.format('1:1')
                                user_wallet.save()
                                print("mathing generated in {} for {} in position left".format(str(upline_user), str(idv)))
                            

                    else:
                        upline_user.total_users_right += 1
                        if upline_user.total_users_left >= upline_user.total_users_right:
                            if upline_user.today_binary_income <= 180000:
                                upline_user.new_funds += 0.9*200
                                upline_user.total_income += 200
                                balance_after = upline_user.new_funds
                                upline_user.today_binary_income += 200

                                user_wallet = WalletHistories()
                                user_wallet.user_id = str(upline_user)
                                user_wallet.balance_before = balance_before
                                user_wallet.balance_after = balance_after
                                user_wallet.amount = 200
                                user_wallet.type = 'credit'
                                user_wallet.comment = 'Matching Income'.format('1:1')
                                user_wallet.save()
                                print("mathing generated in {} for {} in position right".format(str(upline_user), str(idv)))

                upline_user.save()
                print('upline user {} saved {} {}'.format(upline_user, upline_user.total_users_left, upline_user.total_users_right))
                try:
                	sendmatching(upline, idv, next_position, amount)
                except Exception as e:
	                input('upline{}, idv{}, next_position{}, amount{} exception{}'.format(upline, idv, next_position, amount, e))
            else:
                return 0
                
        start_date = datetime.datetime.now() + datetime.timedelta(-1)
        end_date = datetime.datetime.now()
        newids = BinaryTree.objects.filter(created_at__range=(start_date, end_date))
        self.stdout.write('{} jobs to complete'.format(newids.count()))
        level = 0
        for idv in newids:
            level += 1
            position = idv.position
            amount = idv.amount
            sendmatching(idv, idv, position, amount)
            self.stdout.write('{} job/s completed'.format(level))


        self.stdout.write( 'job complete' )