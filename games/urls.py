from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r"^place/$", views.place, name="place"),
    url(r"^parameters/$", views.parameter, name="parameter"),
    url(r"^(?P<gameid>\w{0,50})/$", views.game, name="game"),
]