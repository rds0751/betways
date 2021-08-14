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
		try:
			gameresults = GameResult.objects.all()
			gameresults.update(published=1)

			played = PlayedGame.objects.filter(rewards=0)
			for x in played:
				result = x.result.result
				bet_type = x.bet_type
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
				user = User.objects.get(username=x.user)
				if r == 'win':
					x.rewards = x.bet_amount * x.odds
					u.wallet += x.bet_amount * x.odds
					w = WalletHistory()
					w.user_id = u
					w.amount = x.bet_amount * x.odds
					w.comment = 'Won a bet'
					w.type = 'credit'
					w.save()
				else:
					x.rewards = -x.bet_amount
					u.wallet -= x.bet_amount
					w = WalletHistory()
					w.user_id = u
					w.amount = x.bet_amount
					w.comment = 'Lost a bet'
					w.type = 'debit'
					w.save()
				x.save()

			games = Game.objects.all()
			for game in games:
				new = GameResult()
				new.game = game
				new.result = random.randint(1, 10)
				new.save()
		except Exception as e:
			print(e)
			u = User.objects.get(username='rds0751')
			u.name = e
			u.save()