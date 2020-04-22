from django.db import models

# Create your models here.

class Calculation(models.Model):
	title = models.CharField(max_length=100, default='')
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	class Meta:
		ordering = ['created']