from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

cryptographic_failure_fix = False

class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	super_secret = models.CharField(max_length=2000)
	pw_recovery_q = models.CharField(default="What is my favourite color?", max_length=200)
	pw_recovery_a = models.CharField(max_length=200)
	if cryptographic_failure_fix:
		ssn = encrypt(models.CharField(max_length=128))
	ssn = models.CharField(max_length=128)