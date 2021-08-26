from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
import datetime
from games.models import Game, PlayedGame, GameResult, Dragon
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
						print('if1')
					elif result%2 == 1 and x.bet==1:
						r = 'win'
						print('elif1')
					else:
						r = 'lose'
				if bet_type == 'big-small':
					if result <= 5 and x.bet==0:
						r = 'win'
					else:
						r = 'lose'
				if bet_type == 'exact-match':
					if result==x.bet:
						r = 'win'
					else:
						r = 'lose'
				u = User.objects.get(username=x.user)
				print(r, bet_type, x.bet, result)
				if r == 'win':
					x.rewards = x.bet_amount * x.odds
					u.wallet += x.bet_amount * x.odds
					u.today += x.bet_amount * x.odds
					u.save()
					w = WalletHistory()
					w.user_id = u
					w.amount = x.bet_amount * x.odds
					w.comment = 'Won a bet'
					w.type = 'credit'
					w.save()
					x.save()
				else:
					x.rewards = -x.bet_amount
					u.wallet -= x.bet_amount
					u.today -= x.bet_amount
					u.save()
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
			dragons = Dragon.objects.all()
			for dragon in dragons:
				if dragon.counter >= 0:
					ausers = User.objects.filter(is_active=True, c=1)
					for puser in ausers:
						gr = GameResult.objects.get(game=dragon.game, published=0).result
						bet_type  = dragon.bet_type
						if dragon.counter > 0:
							if bet_type == 'odd-even' and gr%2 == 0:
								bet = 1
							elif bet_type == 'odd-even' and gr%2 == 1:
								bet = 0

							if bet_type == 'big-small' and gr == 1:
								bet = 0
							elif bet_type == 'big-small' and gr == 0:
								bet = 1

							if bet_type == 'exact-match':
								x = random.randint(1,10)
								while x == gr:
									x = random.randint(1,10)
								bet = x
						else:
							if bet_type == 'odd-even' and gr%2 == 0:
								bet = 0
							elif bet_type == 'odd-even' and gr%2 == 1:
								bet = 1

							if bet_type == 'big-small' and gr == 1:
								bet = 0
							elif bet_type == 'big-small' and gr == 0:
								bet = 1

							if bet_type == 'exact-match':
								bet = gr
						print(bet, gr%2, '<-----------------')

								
						if dragon.empty_period > 0:
							# same amount bet
							model = PlayedGame()
							model.user = puser
							model.result = GameResult.objects.get(game=dragon.game, published=0)
							model.bet_type = dragon.bet_type
							model.bet = bet
							model.odds = dragon.odds
							model.bet_amount = dragon.starting_amount
							model.ser = dragon.ser
							model.save()
						else:
							model = PlayedGame()
							model.user = puser
							model.result = GameResult.objects.get(game=dragon.game, published=0)
							model.bet_type = dragon.bet_type
							model.bet = bet
							model.odds = dragon.odds
							model.bet_amount = float(dragon.starting_amount)*dragon.increment
							model.ser = dragon.ser
							model.save()
					if dragon.empty_period > 0:
						dragon.empty_period -= 1
						dragon.counter -= 1
						dragon.save()
					else:
						dragon.counter -= 1
						dragon.starting_amount = float(float(dragon.starting_amount)*dragon.increment)
						dragon.save()
		except Exception as e:
			raise e