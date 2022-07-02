from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from chat_app.models import User, Message


class LoginForm(forms.ModelForm):
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

	class Meta:
		model = User
		fields = ['username', 'password']

	error_messages = {
		'invalid_login': _(
			"Пожалуйста, введите правильное имя пользователя и пароль. Обратите внимание, \
			что оба поля могут быть чувствительны к регистру."
		),
		'inactive': _("Аккаунт неактивен."),
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].label = 'Пароль'
		self.fields['username'].label = 'Имя пользователя'
		self.fields['username'].help_text = None

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username is not None and password:
			user = authenticate(username=username, password=password)
			if user is None:
				raise self.get_invalid_login_error()
			else:
				self.confirm_login_allowed(user)
		return self.cleaned_data

	def confirm_login_allowed(self, user):
		if not user.is_active:
			raise ValidationError(
				self.error_messages['inactive'],
				code='inactive',
			)

	def get_invalid_login_error(self):
		return ValidationError(
			self.error_messages['invalid_login'],
			code='invalid_login',
		)


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

	class Meta:
		model = User
		fields = ['username', 'password', 'confirm_password']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].label = 'Пароль'
		self.fields['confirm_password'].label = 'Подтверждение пароля'
		self.fields['username'].label = 'Имя пользователя'
		self.fields['username'].help_text = None

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password is not None and username:
			if User.objects.filter(username=username).exists():
				raise forms.ValidationError('Этот никнейм уже занят')
			if password != confirm_password:
				raise forms.ValidationError('Пароли не совпадают')
		return self.cleaned_data
