from django.contrib import admin
from .models import Game, GameResult, PlayedGame, Parameter, Dragon
# Register your models here.

admin.site.register(Game)
admin.site.register(GameResult)
admin.site.register(PlayedGame)
admin.site.register(Parameter)
admin.site.register(Dragon)
