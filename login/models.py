from django.db import models

# Create your models here.


class User(models.Model):
	u_id = models.CharField(max_length=30, primary_key=True)
	u_name = models.CharField(max_length=10)
	u_sex = models.CharField(max_length=2, choices=((0, "男"), (1, "女"), (2, "保密")))
	u_phone = models.CharField(max_length=20)
	u_email = models.CharField(max_length=30)
	u_pwd = models.CharField(max_length=128)
	u_vip = models.BooleanField()

	def __str__(self):
		return self.u_name

