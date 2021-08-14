from django.conf.urls import url

from . import views

app_name = "users"
urlpatterns = [
    url(r"^transfer/$", views.transfer, name="transfer"),
    url(r"^fund-request/$", views.fundrequest, name="fundrequest"),
    url(r"^history/$", views.history, name="history"),
    url(r"^imps-transfer/$", views.imps, name="imps"),
    url(r"^send/$", views.send, name="send"),
    url(r"^account/$", views.paymentoptions, name="account"),
    url(r"^mt5-transfer/$", views.neft, name="neft"),
    url(r"^search-beneficiary/$", views.SearchListView.as_view(), name="search"),
]