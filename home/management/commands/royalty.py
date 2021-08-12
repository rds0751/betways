from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories, Withdrawals, Paymentoptions
from binary.models import BinaryTree
import datetime
from django.utils import timezone
from zone.models import ZoneUpgrades

class Command(BaseCommand):
    help = "Update Binary Data"

    def handle(self, *args, **options):
        achievers1 = User.objects.filter(binary_directs__gte=25) & User.objects.filter(binary_directs__lte=50)
        achievers2 = User.objects.filter(binary_directs__gte=50)
        z1 = ZoneUpgrades.objects.filter(zone='zone1', income__lte=300) or ZoneUpgrades.objects.filter(zone='zone2', income__lte=600) or ZoneUpgrades.objects.filter(zone='zone3', income__lte=5000)
        z2 = ZoneUpgrades.objects.filter(zone='zone4', income__lte=15000) or ZoneUpgrades.objects.filter(zone='zone5', income__lte=50000)
        za = []
        for p in z1:
            try:
                user = User.objects.get(username=p.user_id)
                za.append(user)
            except Exception as e:
                pass
        zb = []
        for q in z2:
            try:
                user = User.objects.get(username=q.user_id)
                zb.append(user)
            except Exception as e:
                pass
        zaa = 5000/len(za)
        zba = 9000/len(zb)

        jobs = 0
        print('{} Jobs to complete'.format(len(za)+len(zb)))
        for user in za:
            user.income += zaa
            usewallet = WalletHistories()
            usewallet.user_id = str(user)
            usewallet.amount = zaa
            usewallet.type = "credit"
            usewallet.comment = "Company Royalty Income"
            user.save()
            usewallet.save()
            print(jobs)
            jobs += 1

        for user in zb:
            user.income += zba
            usewallet = WalletHistories()
            usewallet.user_id = str(user)
            usewallet.amount = zba
            usewallet.type = "credit"
            usewallet.comment = "Company Royalty Income"
            user.save()
            usewallet.save()
            print(jobs)
            jobs += 1