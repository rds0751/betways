from django.shortcuts import render
from .models import Game, GameResult

def game(request, gameid):
    game = Game.objects.get(id=gameid)
    results = GameResult.objects.filter(game=game).order_by('-start_time')
    return render(request, 'games/game.html', {'game': game, 'results': results})