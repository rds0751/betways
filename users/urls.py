from django.conf.urls import url

from . import views

app_name = "users"
urlpatterns = [
    url(r'^success/', views.success, name='success'),
    url(r'^failure/$', views.failure, name='failure'),
    url(r'^coming_soon/', views.coming_soon, name='coming_soon'),
    url(r'^cancel/$', views.cancel, name='cancel'),
    url(r"^shop-wallet/$", views.booking, name="booking"),
    url(r"^change-passcode/$", views.passcode, name="passcode"),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^lock/$', views.lockscreen, name='lockscreen'),
    url(r"^signup/(?P<use>\w{0,50})/$", views.referalsignup, name="refersignup"),
    url(regex=r"^$", view=views.UserDashboardView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    url(regex=r"^profile/$", view=views.profile.as_view(), name="profile"),
    url(regex=r"^recharge/$", view=views.recharge.as_view(), name=""),
    url(regex=r"^money-transfer/$", view=views.moneytransfer.as_view(), name=""),
    url(regex=r"^add-amount/$", view=views.addamount.as_view(), name=""),
    url(regex=r"^transfer-amount/$", view=views.transferamount.as_view(), name=""),
    url(regex=r"^direct-team/$", view=views.directteam.as_view(), name=""),
    url(regex=r"^zone-income/$", view=views.zoneincome.as_view(), name=""),
    url(regex=r"^my-network/$", view=views.mynetwork.as_view(), name=""),
    url(regex=r"^payment-options/$", view=views.paymentoptions.as_view(), name=""),
    url(regex=r"^activation-request/$", view=views.activationrequest.as_view(), name=""),
    url(regex=r"^withdrawal-history/$", view=views.withdrawalhistory.as_view(), name=""),
    url(regex=r"^income-history/$", view=views.incomehistory.as_view(), name=""),
    url(regex=r"^change-password/$", view=views.changepassword.as_view(), name=""),
    url(regex=r"^(?P<username>[\w.@+-]+)/$", view=views.UserDetailView.as_view(), name="detail"),
    url(r"^search/email/$", views.SearchListView.as_view(), name="other"),
]