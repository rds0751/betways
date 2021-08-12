from django.shortcuts import render
from .models import Game, GameResult

def game(request, gameid):
    game = Game.objects.get(id=gameid)
    results = GameResult.objects.filter(game=game)
    return render(request, 'games/game.html', {'game': game, 'results': results})