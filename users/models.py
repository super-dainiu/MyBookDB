from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=40, verbose_name="Username")
    name = models.CharField(max_length=40, verbose_name="Name")
    sex = models.CharField(max_length=6, choices=((0, "Male"), (1, "Female"), (2, "None")))
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    email = models.EmailField(max_length=40, verbose_name="E-mail")
    vip = models.BooleanField(verbose_name="VIP")

    def __str__(self):
        return self.name