from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
import datetime
from games.models import Game, PlayedGame, GameResult
import random

class Command(BaseCommand):
	help = "Count Binary Data"

	def handle(self, *args, **options):
		gameresults = GameResult.objects.all()
		gameresults.update(published=1)

		played = PlayedGame.objects.filter(rewards=0)
		for x in played:
			result = x.result.result
			if bet_type == 'odd-even':
				if result%2 == 0 and x.bet==0:
					r = 'win'
				else:
					r = 'lose'
			if bet_type == 'big-small':
				if result <= 5 and x.bet==0:
					r = 'win'
				else:
					r = 'lose'
			if bet_type == 'exact-match' and result==x.bet:
				r = 'win'
			else:
				r = 'lose'
			if r == 'win':
				x.rewards = x.bet_amount * x.odds
			else:
				x.rewards = -x.bet_amount
			x.save()
		games = Game.objects.all()
		for game in games:
			new = GameResult()
			new.game = game
			new.result = random.randint(1, 10)
			new.save()




