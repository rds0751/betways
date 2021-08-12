from django.contrib import admin
from .models import Game, GameResult, PlayedGame
# Register your models here.

admin.site.register(Game)
admin.site.register(GameResult)
admin.site.register(PlayedGame)