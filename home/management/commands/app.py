from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories
from task.models import CompletedTask, Postback
import datetime

class Command(BaseCommand):
    help = "Count App Data"

    def handle(self, *args, **options):
        def finduplines(user):
            try:
                user = User.objects.get(username__iexact=str(user))
                upline = user.referal
            except User.DoesNotExist:
                upline = 'blank'
            return upline

        new = CompletedTask.objects.filter(comment='pending' or "pending ")
        self.stdout.write('{} jobs to complete'.format(new.count()))
        leveln = 0
        for n in new:
            leveln += 1
            task = n.code
            try:
                postback = Postback.objects.get(unid=task)
            except Exception:
                postback = 'blank'
            if postback!='blank':
                userid = User.objects.get(username = str(n.user))

                levels = {
                'level1': 20/100,
                'level2': 10/100,
                'level3': 5/100,
                'level4': 3/100,
                'level5': 2/100,
                'level6': 2/100,
                'level7': 2/100,
                'level8': 2/100,
                'level9': 2/100,
                'level10': 2/100,
                }

                levelp = 0
                try:
                    upline_user = User.objects.get(username=userid.referal)
                except Exception as e:
                    upline_user = 'JR1000'
                amount = float(n.rewards)
                uplines = [upline_user,]
                while levelp < 9 and upline_user != 'blank':
                    upline_user = finduplines(str(upline_user))
                    uplines.append(upline_user)
                    levelp += 1

                level = 1
                for upline in uplines:
                    try:
                        upline_user = User.objects.get(username=upline)
                    except Exception as e:
                        upline_user = 'blank'
                    if upline_user != 'blank':
                        upline_amount = levels['level{}'.format(level)]*amount
                        upline_user.app_wallet += upline_amount*0.9
                        upline_user.total_app_income  += upline_amount
                        upline_wallet = CompletedTask()
                        upline_wallet.user_id = str(upline_user)
                        upline_wallet.amount = upline_amount
                        upline_wallet.type = "credit"
                        upline_wallet.comment = "{} task completed by your level{}".format(n.name, level)
                        upline_user.save()
                        upline_wallet.save()
                        self.stdout.write('payout {} level{}, {}'.format(upline_amount, level, str(upline_user)))
                    level = level + 1
                userid.app_wallet += 0.5*amount*0.9
                userid.total_app_income  += 0.5*amount
                n.type = "credit"
                n.comment = "{} task completed by you, payout generated!".format(n.name)
                n.save()
                userid.save()
                self.stdout.write('{} {}'.format(n.comment, 0.5*amount))
            else:
                n.comment = "Success"
                n.save()
                self.stdout.write('payout failed {} {}'.format(n.comment, leveln))


        self.stdout.write('job complete')