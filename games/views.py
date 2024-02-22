from django.shortcuts import render
from .models import Game, GameResult, PlayedGame
import random

def game(request, gameid):
    game = Game.objects.get(id=gameid)
    results = GameResult.objects.filter(game=game).order_by('-start_time')
    return render(request, 'games/game.html', {'game': game, 'results': results})

def parameter(request):
	played_games = PlayedGame.objects.filter(user=request.user)
	return render(request, 'games/parameter.html', {'played_games': played_games})

def place(request):
	if request.method == 'POST':
		amount = request.POST.get('amount')
		if request.user.wallet|floatformat:2 >= int(amount):
			if 'evenodd' in request.POST:
				bet = request.POST.get('bet')
				amount = request.POST.get('amount')
				btype = 'odd-even'

			if 'bigsmall' in request.POST:
				bet = request.POST.get('bet')
				amount = request.POST.get('amount')
				btype = 'big-small'

			if 'exact' in request.POST:
				bet = request.POST.get('bet')
				amount = request.POST.get('amount')
				btype = 'exact-match'

			game = Game.objects.get(id=request.POST.get('gid'))
			gameresult = GameResult.objects.get(game=game, published=0)
			model = PlayedGame()
			model.user = request.user
			model.result = gameresult
			model.bet_type = btype
			model.bet = bet
			model.odds = 2
			model.bet_amount = amount
			model.ser = random.randint(11,99)
			model.save()
			message = 'Bet Placed'
		else:
			message = 'Not enough Available Balance!'
	return render(request, 'games/placed.html', {'message': message})
