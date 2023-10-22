from django.http import HttpResponse, HttpRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
import sqlite3
import logging
from flawedsite.models import Account

logger = logging.getLogger('django')

@login_required
def index(request):
	return render(request, 'pages/index.html')

def signup(request):
	identification_and_authentication_failure_fix = False # <-- Set this to True to fix the password validation
	if request.method == 'POST':
		new_user = User()
		new_user.username = request.POST["username"]
		new_user.email = request.POST["email"]
		new_user.set_password(request.POST["password"])
		if identification_and_authentication_failure_fix:
			try:
				validate_password(request.POST["password"], new_user)
				new_user.save()
				new_acc = Account()
				new_acc.user = new_user
				new_acc.save()
				return redirect('/')
			except ValidationError as ex:
				messages.add_message(request, messages.ERROR, "\n".join(ex.messages))
		else:
			new_user.save()
			new_acc = Account()
			new_acc.user = new_user
			new_acc.save()
			return redirect('/')
	return render(request, 'pages/signup.html')

# Csrf is exempt to make testing of BAC easier.
# This decorator would of course be removed when fixing the Broken Access Control issues.
@csrf_exempt
@login_required
def secret(request, uid):
	bac_fix = False
	injection_fix = False
	if bac_fix and uid != request.user.id:
		raise PermissionDenied("You're only allowed to view & edit your own secrets!")
	if request.method == 'POST':
		new_secret = request.POST["new_secret"]
		# You can test the injection for example with:
		# You´ve been hacked!'; --
		if injection_fix:
			user_acc = Account.objects.get(user_id=request.user.id)
			user_acc.super_secret = new_secret
			user_acc.save()
		else:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			cursor.execute("UPDATE flawedsite_account SET super_secret = '" + new_secret + "' WHERE user_id='" + str(uid) + "';")
			conn.commit()
		logger.info(msg=f"User {request.user.id} edited user's {uid} secret to '{new_secret}'")

	user_secret = Account.objects.get(user_id=uid).super_secret
	return render(request, "pages/secret.html", {'secret':user_secret})
