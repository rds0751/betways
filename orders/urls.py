from django.conf.urls import include, url
from orders import views

urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^success/$', views.success, name='success'),
    url(r'^failure/$', views.failure, name='failure'),
    url(r'^cancel/$', views.cancel, name='cancel'),
]