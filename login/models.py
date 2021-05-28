from django.db import models

# Create your models here.


class User(models.Model):
	name = models.CharField(max_length=10, verbose_name="姓名")
	sex = models.CharField(max_length=2, choices=((0, "男"), (1, "女"), (2, "保密")))
	phone = models.CharField(max_length=20, verbose_name="手机号")
	email = models.EmailField(max_length=30, verbose_name="E-mail")
	pwd = models.CharField(max_length=128, verbose_name="密码")
	vip = models.BooleanField(verbose_name="是否VIP？")

	def __str__(self):
		return self.name


class Address(models.Model):
	address = models.CharField(max_length=100, verbose_name="地址")
	user = models.ForeignKey(to="User", on_delete=models.CASCADE)