from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistories
from binary.models import BinaryTree
from task.models import CompletedTask
import datetime

class Command(BaseCommand):
    help = "Update Binary Data"

    def handle(self, *args, **options):
        def sendmatching(main, taskname, user, level):
            level += 1
            try:
                upline_user = User.objects.get(username=str(user.referal))
            except User.DoesNotExist:
                upline_user = 'blank'

            if level <= 10 and upline_user != 'blank':
                direct_left = User.objects.filter(referal=str(upline_user)).count()
                direct_right = User.objects.filter(referal=str(upline_user)).count()

                if True:
                    try:
                        prime = BinaryTree.objects.get(user=str(upline_user))
                    except Exception as e:
                        prime = False
                    if level==1:
                        upline_user.app_temp += 1.0

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.1
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==2:
                        upline_user.app_temp += 0.9

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.09
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==3:
                        upline_user.app_temp += 0.8

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.08
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==4:
                        upline_user.app_temp += 0.7

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.07
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==5:
                        upline_user.app_temp += 0.6

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.06
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==6 and prime:
                        upline_user.app_temp += 0.5

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.05
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==7 and prime:
                        upline_user.app_temp += 0.4

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.04
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==8 and prime:
                        upline_user.app_temp += 0.3

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.03
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==9 and prime:
                        upline_user.app_temp += 0.2

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.02
                        model.comment = "Team commission from level {} and user {}".format(level, main)
                        model.save()

                    elif level==10 and prime:
                        upline_user.app_temp += 0.1

                        model = CompletedTask()
                        model.user = str(upline_user)
                        model.code = taskname
                        model.name = "Team Commission"
                        model.rewards = 0.01
                        model.comment = "From level {} and user {}".format(level, main)
                        model.save()

                upline_user.save()
                sendmatching(main, taskname, upline_user, level)
            else:
                level = 0
                return level
                
        start_date = datetime.datetime.now() + datetime.timedelta(-2)
        end_date = datetime.datetime.now()
        newtxns = CompletedTask.objects.filter(comment="pending")
        self.stdout.write('{} jobs to complete'.format(newtxns.count()))
        p = 0
        for idv in newtxns:
            p+=1
            main = idv.user
            code = idv.name
            try:
                pidv = User.objects.get(username=idv.user)
                nidv = User.objects.get(username=pidv.referal)
            except Exception as e:
                pidv = nidv = None
            if pidv != None and nidv != None:
                level = 0
                level  = sendmatching(main, code, nidv, level)
                idv.comment = "Rewarded"
                idv.save()
                self.stdout.write('{} job/s completed'.format(p))

        self.stdout.write( 'job complete' )