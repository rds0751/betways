from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import re_path

from . import views

app_name = "panel"
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.guestlogin, name='guestlogin'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<id>[\w.@+-]+)/$', views.user, name='users'),
    url(r'^~withdrawals/$', views.neft, name='neft'),
    url(r'^withdrawals/$', views.withdrawals, name='withdrawals'),
    url(r'^ids/$', views.ids, name='ids'),
    url(r'^bankdetails/$', views.bankdetails, name='bankdetails'),
    url(r'^kycs/$', views.kycs, name='kycs'),
    url(r'^activations/$', views.activations, name='activations'),
    url(r'^activations/(?P<id>[\w.@+-]+)/$', views.activation, name='activation'),
    url(r'^withdrawals/(?P<id>[\w.@+-]+)/$', views.withdrawal, name='withdrawal'),
    url(regex=r"^~profile/$", view=views.UserProfileView.as_view(), name="profile"),
    url(r'^franchise/$', views.franchise, name='franchise'),
]