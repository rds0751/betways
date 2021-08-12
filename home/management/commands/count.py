from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories
from binary.models import BinaryTree
import datetime

class Command(BaseCommand):
    help = "Count Binary Data"

    def handle(self, *args, **options):
	    
	    def sendmatching(user, position, amount):
	        p = user
	        if user.upline_user_id != 'top':
	        	try:
	        		upline = BinaryTree.objects.get(user=str(user.upline_user_id))
	        		next_position = upline.position
	        		if upline.upline_user_id == user.upline_user_id:
	        			print('Max recursion se bacha le re baba'.format(upline, user))
	        			inpu = input("Enter y when done with resolution")
	        	except Exception as e:
	        		print("binary error {} at user {} and upline {}".format(e, str(user), str(user.upline_user_id)))
	        		upline = 'blank'


	        elif user.upline_user_id == 'top':
	            upline = 'blank'


	        if upline != 'blank':
	            p.rewarded = True
	            p.save()
	            try:
	                upline_user = User.objects.get(username=str(upline.user))
	                balance_before = upline_user.binary_income
	            except User.DoesNotExist:
	                print("user not found user is {}".format(str(upline.user)))
	                inputuser = input("Enter User:")
	                upline_user = User.objects.get(username=str(inputuser))
	                balance_before = upline_user.binary_income
	            
	            direct_left = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='left').count()
	            direct_right = BinaryTree.objects.filter(direct_user_id=str(upline_user), position='right').count()

	            
	            if upline_user.total_users_left == 0 or upline_user.total_users_left == 0:
	                if position == 'left':
	                    upline_user.total_users_left += 1
	                    upline_user.left_side_business += 885
	                    if upline_user.total_users_right >= upline_user.total_users_left:
	                        if direct_left >= 1 and direct_right >= 1:
	                            upline_user.total_income += 200
	                            print('if1')
	                        upline_user.rank = 'Ellite'
	                else:
	                    upline_user.total_users_right += 1
	                    upline_user.right_side_business += 885
	                    if upline_user.total_users_left >= upline_user.total_users_right:
	                        if direct_left >= 1 and direct_right >= 1:
	                            upline_user.total_income += 200
	                            print('if2')
	                        upline_user.rank = 'Ellite'
	            else:
	                if position == 'left':
	                    upline_user.total_users_left += 1
	                    upline_user.left_side_business += 885
	                    if upline_user.total_users_left == upline_user.total_users_right:
	                        upline_user.total_income += 200
	                        print('if3')
	                        upline_user.rank = 'Ellite'
	                else:
	                    upline_user.total_users_right += 1
	                    upline_user.right_side_business += 885
	                    if upline_user.total_users_left == upline_user.total_users_right:
	                        upline_user.total_income += 200
	                        print('if4')
	                        upline_user.rank = 'Ellite'
	            upline_user.save()
	            sendmatching(upline, next_position, amount)
	        else:
	            return 0
	            

	    newids = BinaryTree.objects.all()
	    self.stdout.write('{} jobs to complete'.format(newids.count()))
	    level = 0
	    for idv in newids:
	    	level += 1
	    	position = idv.position
	    	amount = idv.amount
	    	sendmatching(idv, position, amount)
	    	self.stdout.write('{} job/s completed'.format(level))


	    self.stdout.write( 'job complete' )