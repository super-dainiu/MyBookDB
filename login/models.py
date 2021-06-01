from django.db import models

# Create your models here.


class User(models.Model):
	username = models.CharField(max_length=40, verbose_name="Username")
	email = models.EmailField(max_length=40, verbose_name="E-mail")
	pwd = models.CharField(max_length=128, verbose_name="Password")

	def __str__(self):
		return self.username
