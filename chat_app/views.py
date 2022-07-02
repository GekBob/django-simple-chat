from django.shortcuts import redirect, render
from django import views
from django.contrib.auth import login, authenticate

from chat_app.models import User, Message
from chat_app.forms import LoginForm, RegistrationForm


class EnterView(views.View):
	def get(self, request):
		login_form = LoginForm(request.POST)
		reg_form = RegistrationForm(request.POST)
		context = {
			'login_form': login_form,
			'reg_form': reg_form
		}
		return render(request, 'enter.html', context)

	def post(self, request):
		login_form = LoginForm(request.POST)
		reg_form = RegistrationForm(request.POST)
		if request.POST.get('submit') == 'Вход':
			if login_form.is_valid():
				user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
				login(request, user)
				return redirect('chatroom')
		if request.POST.get('submit') == 'Регистрация':
			if reg_form.is_valid():
				user = reg_form.save(commit=False)
				user.username = reg_form.cleaned_data['username']
				user.set_password(reg_form.cleaned_data['password'])
				user.save()
				login(request, user)
				return redirect('chatroom')
		context = {
			'login_form': login_form,
			'reg_form': reg_form
		}
		return render(request, 'enter.html', context)

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('chatroom')
		return super().dispatch(request, *args, **kwargs)


class ChatroomView(views.View):
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('enter')
		messages = Message.objects.all().select_related('author')
		context = {
			'messages': messages
		}
		return render(request, 'chatroom.html', context)
