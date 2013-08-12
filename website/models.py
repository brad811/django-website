from django.db import models

class User(models.Model):
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=270)
	name = models.CharField(max_length=80)
	location = models.CharField(max_length=60)
	def __unicode__(self):
		return self.name
