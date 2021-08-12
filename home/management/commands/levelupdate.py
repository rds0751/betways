from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories
from level.models import Activation
from users.models import User
from binary.models import BinaryTree
import datetime

class Command(BaseCommand):
    help = "Count Binary Data"

    def handle(self, *args, **options):

	    newids = User.objects.all()
	    self.stdout.write('{} jobs to complete'.format(newids.count()))
	    level = 0
	    for idv in newids:
	        level += 1
	        try:
	            binaryuser = BinaryTree.objects.get(user=idv.username)
	        except BinaryTree.DoesNotExist:
	            binaryuser = "blank"

	        if binaryuser == "blank":
	            try:
	                binary = User.objects.get(username=idv.username)
	            except User.DoesNotExist:
	                binary = "blank"
	            if binary != "blank":
	                direct_user = binary.referal
	                model = BinaryTree()
	                model.user = idv.username
	                model.direct_user_id = direct_user
	                model.amount = 0
	                model.binary_level = 0
	                model.save()
	                self.stdout.write('{} if job/s completed'.format(level))
	        else:
	            self.stdout.write('{} else job/s completed'.format(level))


	    self.stdout.write( 'job complete' )