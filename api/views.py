from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import CreateUserSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import render
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.http import JsonResponse
from users.models import User
from level.models import UserTotal
from django.core import serializers
from django.core.cache import cache
# from .renderers import UserJSONRenderer
 
User = get_user_model()

class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        name = self.request.data ["name"]
        sponsor = self.request.data ["sponsor"]
        mobile = self.request.data ["mobile"]
        username = self.request.data ["username"]
        password = self.request.data ["password"]
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username Already exists"})
        else:
            if len(password) < 6:
                return Response({"error": "Password too short. Please add atleast 6 characters"})
            else:
                user = User.objects.create_user(username='JR{}'.format(username), password=password, name=name)
                user.mobile = mobile
                user.referal = sponsor
                user.save()
                return Response({"success": "User created Successfully"})
        

class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response({**serializer.data, **token_data}, status=status.HTTP_201_CREATED, headers=headers)


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = request.user
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'name': user_profile.name,
                    'username': user_profile.username,
                    'mobile': user_profile.mobile,
                    'address': user_profile.address,
                    'sponsor': user_profile.referal,
                    'email': user_profile.email,
                    'balance': '{}'.format(round(user_profile.app_wallet, 2)),
                    'temp_balance': '{}'.format(round(user_profile.app_temp, 2))
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)

class LevelTeamView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        username = request.user
        user_total = UserTotal.objects.filter(user_id=str(username)).order_by('level')
        leveldata = []
        for level in user_total:
            data = {
            'tags': ['levels'],
            'level': 'Level {}'.format(level.level),
            'active': level.active_users,
            'inactive': level.inactive_users
            }
            leveldata.append(data)
        level1 = User.objects.filter(referal=str(username)).only('username')
        level1n = []
        for x in level1:
            level1n.append(str(x))
        level2n = []
        for y in level1n:
            level2 = User.objects.filter(referal=y).only('username')
            for z in level2:
                level2n.append(str(z))

        all_users = level1n + level2n

        usersdata = []
        for user in all_users:
            try:
                user = User.objects.get(username=user)
                data = {
                'tags': ['users'],
                'name': user.name,
                'mobile': user.mobile,
                'userid': user.username,
                'by': user.referal
                }
                usersdata.append(data)
            except Exception as e:
                print(e)
            
        return Response({'users': usersdata, 'levels': leveldata})

from django.utils.crypto import get_random_string

class TaskView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        def generateid():
            txnid = get_random_string()
            try:
                txn = Postback.objects.get(unid = txnid)
            except Postback.DoesNotExist:
                txn = 0
            if txn:
                generateid()
            else:
                return '{}'.format(txnid)

        username = request.user
        tasks_all = Task.objects.filter(active=True)
        
        
        tasks = []
        for task in tasks_all:
            try:
                x = CompletedTask.objects.get(code=task.pk, user=str(username))
                x=1
            except CompletedTask.DoesNotExist:
                x=0
            if True:
                i = generateid()
                data = {
                'tags': ['task'],
                'name': '{}'.format(task.name),
                'id': i,
                'x':x,
                'amount': task.amount,
                'desc': task.description,
                'stars': task.stars,
                'url': task.url+'{}'.format(i),
                'first': 'https://www.jrindia.co.in{}'.format(task.imageURL.url),
                'second': 'https://www.jrindia.co.in{}'.format(task.mediumImageURL.url),
                'taskid': task.pk
                }
                tasks.append(data)
        return Response({ 'tasks': tasks})

class GameView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        username = request.user
        games_all = Game.objects.filter(active=True)
        
        
        games = []
        for game in games_all:
            try:
                x = PlayedGame.objects.get(name=game.name, user=str(username))
                x=1
            except PlayedGame.DoesNotExist:
                x=0
            if True:
                data = {
                'tags': ['game'],
                'name': '{}'.format(game.name),
                'code': game.code,
                'desc': game.description,
                'stars': game.stars,
                'url': game.url,
                'first': 'https://www.jrindia.co.in{}'.format(game.imageURL.url),
                }
                games.append(data)
        return Response({ 'games': games})

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

def postback(request, sub1, ip):
    model = Postback()
    model.task = 'Chingari'
    model.ip = ip
    model.unid = sub1

    model.save()
    message = "data sent succesfully sub1 {}, ip {}, ".format(sub1, ip)
    
    return render(request, 'ads/ads.html', {'message': message})

def newpostback(request, sub1, sub2, ip):
    model = Postback()
    model.task = sub1
    model.ip = ip
    model.unid = sub2

    model.save()
    message = "data sent succesfully sub1 {}, ip {}, {}".format(sub1, ip, sub2)
    
    return render(request, 'ads/ads.html', {'message': message})


from django.http import HttpResponse
class Completed(APIView):
    permission_classes = (permissions.AllowAny,)

    
    def post(self, request, format=None):
        taskid = self.request.data ["taskid"]
        user = self.request.data ["user"]
        rewards = self.request.data ["rewards"]
        ip = self.request.data ["ip"]
        comment = self.request.data ["comment"]
        name = self.request.data ["name"]

        try:
            x = CompletedTask.objects.get(code=taskid, user=user)
            x=1
        except CompletedTask.DoesNotExist:
            x=0
        if x:
            return HttpResponse(status=500)
        if True:
            model = CompletedTask()
            model.user = user
            model.code = taskid
            model.name = name
            model.rewards = 1
            model.ip = ip
            model.comment = "Task Done"
            model.save()
            try:
                task = Task.objects.get(id=str(taskid))
                task.todaydownload += 1
                task.totaldownload += 1
                task.save()
            except Exception as e:
                pass
            s = User.objects.get(username=user)
            p = s
            directs = User.objects.filter(referal=str(p))
            try:
                upline = User.objects.get(username=p.referal)
            except Exception as e:
                upline = 'blank'
            if upline != 'blank':
                upline.app_directs += 1
                p.tasks_done += 1
                p.save()
                done = p.tasks_done
                if upline.app_directs == 2 and done > 9:
                    s.app_temp += 10
                    s.save()

                def finduplines(user):
                    try:
                        user = User.objects.get(username__iexact=str(user))
                        upline = user.referal
                    except User.DoesNotExist:
                        upline = 'blank'
                    return upline

                levels = {
                'level1': 100/100,
                'level2': 90/100,
                'level3': 80/100,
                'level4': 70/100,
                'level5': 60/100,
                'level6': 50/100,
                'level7': 40/100,
                'level8': 30/100,
                'level9': 20/100,
                'level10': 10/100,
                }

                level = 0
                userid = upline
                upline_user = userid.referal
                amount = 1
                uplines = [upline_user, ]
                while level < 9 and upline_user != 'blank':
                    upline_user = finduplines(str(upline_user))
                    uplines.append(upline_user)
                    level += 1

                level = 1
                for upline in uplines:
                    directs = User.objects.filter(referal=str(upline))
                    try:
                        upline_user = User.objects.get(username=upline)
                    except Exception as e:
                        upline_user = 'blank'
                    try:
                        prime = BinaryTree.objects.get(user=str(upline_user))
                    except Exception as e:
                        prime = 'blank'
                    if upline_user != 'blank' and directs.count() > 1:
                        done = upline_user.task_done
                        if done > 9:
                            if level<=5:
                                upline_amount = levels['level{}'.format(level)]*amount
                                upline_user.app_temp += upline_amount
                                upline_user.total_income  += upline_amount
                                upline_wallet = WalletHistories()
                                upline_wallet.user_id = upline
                                upline_wallet.amount = upline_amount
                                upline_wallet.type = "credit"
                                upline_wallet.comment = "App Earning Team Commision".format(level)
                                upline_user.save()
                                upline_wallet.save()
                            if level > 5 and prime != 'blank':
                                upline_amount = levels['level{}'.format(level)]*amount
                                upline_user.app_temp += upline_amount
                                upline_user.total_income  += upline_amount
                                upline_wallet = WalletHistories()
                                upline_wallet.user_id = upline
                                upline_wallet.amount = upline_amount
                                upline_wallet.type = "credit"
                                upline_wallet.comment = "App Earning Team Commision".format(level)
                                upline_user.save()
                                upline_wallet.save()
                    level = level + 1

            return Response({"success": "Data Saved Successfully"})

from django.http import HttpResponse
class Played(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        code = self.request.data ["code"]
        user = self.request.data ["user"]
        ip = self.request.data ["ip"]
        comment = self.request.data ["comment"]
        name = self.request.data ["name"]



        try:
            x = PlayedGame.objects.get(code=code, user=user)
            x=1
        except CompletedTask.DoesNotExist:
            x=0
        if x:
            return HttpResponse(status=500)
        else:
            game = Game.objects.get(name=str(name))
            game.todaydownload += 1
            game.totaldownload += 1
            game.save()
            model = PlayedGame()
            model.user = user
            model.code = code
            model.name = name
            model.ip = ip
            model.comment = comment
            model.save()
            return Response({"success": "Data Saved Successfully"})
        

class TxnsView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        username = request.user
        txns = CompletedTask.objects.filter(user=str(username))
        txnsdata = []
        for txn in txns:
            data = {
            'tags': ['txns'],
            'name': txn.name,
            'reward': txn.rewards,
            'comment': txn.comment
            }
            txnsdata.append(data)
        return Response({ 'txns': txnsdata })