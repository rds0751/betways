from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Game(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True, help_text="A short label, generally used to define a task.")
	imageURL = models.FileField(upload_to='documents/', default='x')
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class GameResult(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now=True)
	result = models.IntegerField(default=0)
	published = models.IntegerField(default=0)

	def end_time(self):
		activated_at = self.start_time
		return activated_at + timezone.timedelta(minutes=5)

	def __str__(self):
		return str(str(self.game)+' result '+str(self.result)) + str(self.published)


class PlayedGame(models.Model):
	user = models.CharField(max_length=50, null=True, blank=True)
	result = models.ForeignKey(GameResult, on_delete=models.CASCADE)
	bet_type = models.CharField(max_length=50, choices=(('odd-even','odd-even'), ('big-small','big-small'), ('exact-match','exact-match')))
	bet = models.FloatField(default=0)
	odds = models.FloatField(default=0, blank=True)
	bet_amount = models.FloatField(default=0, blank=True)
	rewards = models.FloatField(default=0, blank=True)
	ser = models.FloatField(default=0, blank=True)

	# big 1 small 0
	# odd 1 even 0
	# exact = exact
	
	def __str__(self):
		return str(self.user) + str(self.rewards)


class Parameter(models.Model):
	user = models.CharField(max_length=50, null=True, blank=True)
	status = models.IntegerField(default=0)
	selected_plan = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.user) + str(self.status)


class Dragon(models.Model):
	starting_amount = models.FloatField(default=3.3)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	bet_type = models.CharField(max_length=100, choices=(
		('odd-even', 'odd-even'),
		# ('exact-match', 'exact-match'), 
		# ('big-small', 'big-small')
		))
	ser = models.FloatField(default=18)
	counter = models.FloatField(default=0)
	empty_period = models.FloatField(default=30)
	odds = models.FloatField(default=0, blank=True)
	increment = models.FloatField(default=1.03)
