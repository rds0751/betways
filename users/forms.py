from allauth.account.forms import SignupForm
from django import forms
from .models import *
import random
import requests
from level.models import UserTotal, LevelIncomeSettings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SimpleSignupForm(SignupForm):
	mobile = forms.CharField(max_length=250, label='mobile')
	name = forms.CharField(max_length=250, label='name')
	referal_code = forms.CharField(max_length=14, label="refer")

	def get_success_url(self):
		return '/signup/onboarding/'
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'mobile')

	def clean_name(self):
		name = self.cleaned_data['name']
		return name[0].upper() + name[1:].lower()

	def clean_username(self):
		def generateuser():
			r = random.randint(100001,999999)
			u = User.objects.filter(username='IPAY{}'.format(r)).count()
			if u > 0:
				generateuser()
			else:
				return 'IPAY{}'.format(r)
		u = generateuser()
		username = u
		return username

	def save(self, request):
		user = super(SimpleSignupForm, self).save(request)
		referral = self.cleaned_data['referal_code'].upper()
		try:
			userr = User.objects.get(username=referral)
		except Exception as e:
			userr = 'blank'
		if userr == 'blank':
			referral = 'IPAY999999'
		plan = UserTotal()
		plan.user = user
		plan.level = LevelIncomeSettings.objects.get(id=9)
		plan.active = False
		plan.left_months = 0
		plan.direct = referral
		plan.save()
		# subject = 'Welcome to IPAYMATICS Inc.'
		# html_message = render_to_string('account/email/welcome.html', {'context': self.cleaned_data['name']})
		# plain_message = strip_tags(html_message)
		# from_email = 'support@ipaymatics.com'
		# to = user.email

		# mail.send_mail(subject=subject, message=plain_message, from_email=from_email, recipient_list=[to], html_message=html_message)
		# url = "http://2factor.in/API/V1/99254625-e54d-11eb-8089-0200cd936042/ADDON_SERVICES/SEND/PSMS"
		# payload = "{'From': 'TFCTOR', 'Msg': 'Hello World', 'To': '7000934949,'}"
		# response = requests.request("GET", url, data=payload)
		# print(response.text)
		user.mobile = self.cleaned_data['mobile']
		user.name = self.cleaned_data['name']
		user.referral = referral
		user.save()
		return user