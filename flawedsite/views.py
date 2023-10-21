from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from flawedsite.models import Account


@login_required
def index(request):
	return render(request, 'pages/index.html')

def signup(request:HttpRequest):
	if request.method == 'POST':
		new_user = User()
		new_user.username = request.POST["username"]
		new_user.email = request.POST["email"]
		new_user.set_password(request.POST["password"])
		new_user.save()
		new_acc = Account()
		new_acc.user = new_user
		new_acc.save()
		return redirect('/')
	return render(request, 'pages/signup.html')