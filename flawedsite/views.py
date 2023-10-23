import sqlite3
import logging
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from flawedsite.models import Account

logger = logging.getLogger('django')

@login_required
def index(request):
	return render(request, 'pages/index.html')

def signup(request):
	identification_and_authentication_failure_fix = False # <-- Set this to True to fix the password validation
	if request.method == 'POST':
		empty_account_details = []
		for val in request.POST:
			if len(request.POST[val]) == 0:
				empty_account_details.append(val)
		if len(empty_account_details) > 0:
			messages.add_message(request, messages.ERROR, "Required information missing:\n"+"\n".join(empty_account_details))
		else:
			new_user = User()
			new_user.username = request.POST["username"]
			new_user.email = request.POST["email"]
			new_user.set_password(request.POST["password"])
			if identification_and_authentication_failure_fix:
				try:
					validate_password(request.POST["password"], new_user)
					new_user.save()
				except ValidationError as ex:
					messages.add_message(request, messages.ERROR, "\n".join(ex.messages))
					return render(request, 'pages/signup.html')
			else:
				new_user.save()
			new_acc = Account()
			new_acc.user = new_user
			new_acc.pw_recovery_q =request.POST["recovery_q"]
			new_acc.pw_recovery_a =request.POST["recovery_a"]
			new_acc.ssn = request.POST["ssn"]
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

	user_acc = Account.objects.get(user_id=uid)
	return render(request, "pages/secret.html", {'secret':user_acc.super_secret})

def recovery_init(request):
	recovery_q = None
	username = None
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.POST['username'])
		except Exception:
			return redirect('recovery_init')

		if user is not None:
			username = request.POST['username']
			user_acc = Account.objects.get(user_id=user.pk)
			recovery_q = user_acc.pw_recovery_q
	return render(request, "pages/recovery.html", {'username':username, 'recovery_q':recovery_q})

def recovery_attempt(request):
	if request.method == 'POST':
		user = User.objects.get(username=request.POST['username'])
		if user is not None:
			user_acc = Account.objects.get(user_id=user.pk)
			if request.POST['answer'].lower() == user_acc.pw_recovery_a.lower():
				request.session['uid'] = user.pk
				return render(request, "pages/recovery.html",{'correct_answer':True,'user_id':user.pk,'username':request.POST['username']})
			else:
				messages.add_message(request, messages.ERROR, "Wrong answer to the question!")
	return redirect('/')

def change_pw(request):
	uid = ''
	if 'uid' in request.session:
		uid = request.session['uid']
		del request.session['uid']
	if request.method == 'POST' and str(uid) == request.POST['user_id']:
		user = User.objects.get(pk=request.POST['user_id'])
		user.set_password(request.POST['new_pw'])
		user.save()
	return redirect('/')

def email_recovery(request):
	if request.method == 'POST':
		print(f'sending mail to {request.POST["recovery_email"]}')
		messages.add_message(request, messages.INFO, "If the email address you entered matches one we have recorded, we will send you a temporary password to access the account.")
		return redirect('/')
	return render(request, 'pages/recovery_email.html')
