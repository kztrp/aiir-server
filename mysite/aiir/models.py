from django.db import models
from django.contrib.auth.models import User
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
# Create your models here.


class Calculation(models.Model):
	number = models.IntegerField(default=0)
	title = models.CharField(max_length=100, default='')
	progress = models.FloatField(default=0)
	result = models.BooleanField(default=False)
	is_fermat = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	user = CurrentUserField()
	text = models.TextField()

	class Meta:
		ordering = ['created']