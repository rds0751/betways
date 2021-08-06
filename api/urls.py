from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.cache import cache_page
from .views import CreateUserAPIView, LogoutUserAPIView, SignupView, UserDetailView, LevelTeamView, TaskView, postback, Completed, TxnsView, newpostback, GameView, Played


urlpatterns = [
    url(r'^auth/login/$',
        obtain_auth_token,
        name='auth_user_login'),
    url(r'^auth/signup/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    url(r"^auth/register/$", SignupView.as_view(), name='auth_user_create'),
    url(r"^completed/$", Completed.as_view(), name='completed'),
    url(r"^played/$", Played.as_view(), name='played'),
    url(r'^auth/logout/$',
        LogoutUserAPIView.as_view(),
        name='auth_user_logout'),
    url(r"^user/data/$", UserDetailView.as_view(), name='user-data'),
    url(r"^user/network/$", LevelTeamView.as_view(), name='my-network'),
    url(r"^user/wallet/$", TxnsView.as_view(), name='txns'),
    url(r"^user/tasks/$", TaskView.as_view(), name='my-task'),
    url(r"^user/games/$", GameView.as_view(), name='my-game'),
    url(r"^ads/postback/ip=(?P<ip>[\w.@+-]+)/sub1=(?P<sub1>[\w.@+-]+)/$", postback, name="ads-postback"),
    url(r"^ads/postback/ip=(?P<ip>[\w.@+-]+)/sub1=(?P<sub1>[\w.@+-]+)/sub2=(?P<sub2>[\w.@+-]+)/$", newpostback, name="new-ads-postback"),
    # url(r'^users/login/?$', LoginAPIView.as_view()),
]
