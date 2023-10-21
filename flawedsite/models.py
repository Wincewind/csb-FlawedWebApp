from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	super_secret = models.CharField(max_length=2000)
	password_recovery_answer = models.CharField(max_length=200)