from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PrivateChat, Message


@login_required
def index(request):
	users = User.objects.exclude(username=request.user.username)
	context = {
		'users': users
	}

	return render(request, "chat/index.html", context)


@login_required
def room(request, username):
	if not User.objects.filter(username=username).exists():
		raise Http404()

	user1 = request.user
	user2 = User.objects.get(username=username)

	private_chat = PrivateChat.get_or_create_private_chat(user1, user2)
	messages = Message.objects.filter(room=private_chat)

	context = {
		'messages': messages,
		'username': username,
		'sender_username': user1.username,
	}

	return render(request, "chat/room.html", context)



def login_user(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		print("post method")
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			login(request, user)
			return redirect('/')
		else:
			return render(request, 'login.html', {
					'error': 'Invalid username or password!! fuck you'
				})

	return render(request, 'login.html')


def logout_user(request):
	logout(request)
	return redirect('/')


def home(request):
	return HttpResponse("""
		<p><a href="/login/">login</a></p>
		<p><a href="/logout/">logout</a></p>
		<p><a href="/chat/">chat</a></p>
		<style>
		body {
			padding: 50px;
		}
		</style>
	""")