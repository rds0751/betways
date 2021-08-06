from django.conf.urls import url
from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    # url(r"^join/$", views.leveljoin, name="join"),
    url(r"^team/(?P<user>[\w.@+-]+)/(?P<level>[\w.@+-]+)", views.leveltree, name="tree"),
    path('payment/',views.payment,name="payment"),
    path('success/',views.payment_success,name="payment-success"),
    path('activation/',views.activation,name="activation"),
]