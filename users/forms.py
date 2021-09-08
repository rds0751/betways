from allauth.account.forms import SignupForm
from django import forms
from .models import *
import random
import requests
from level.models import UserTotal, LevelIncomeSettings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError

class SimpleSignupForm(SignupForm):
	mobile = forms.CharField(max_length=250, label='mobile')
	name = forms.CharField(max_length=250, label='name')
	referal_code = forms.CharField(max_length=14, label="referal_code")

	def get_success_url(self):
		return '/signup/onboarding/'
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'mobile')

	def clean_name(self):
		name = self.cleaned_data['name']
		return name[0].upper() + name[1:].lower()

	def clean_username(self):
		try:
			user_exists1 = User.objects.get(username=self.cleaned_data['username'])
		except Exception as e:
			return self.cleaned_data['username']
		try:
			user_exists2 = User.objects.get(username=self.cleaned_data['mobile'])
		except Exception as e:
			return self.cleaned_data['mobile']
		if user_exists2:
			raise ValidationError("Mobile Number exists")
		if user_exists1:
			raise ValidationError("User exists")
		
			
	def save(self, request):
		user = super(SimpleSignupForm, self).save(request)
		referral = self.cleaned_data['referal_code']
		try:
			userr = User.objects.get(username=referral)
		except Exception as e:
			userr = 'blank'
		if userr == 'blank':
			referral = '999999'
		user.mobile = clean_mobile(self)
		user.name = self.cleaned_data['name']
		user.referral = referral
		user.save()
		return user