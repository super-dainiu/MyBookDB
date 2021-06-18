from django.db import models

# Create your models here.


class Publishers(models.Model):
    name = models.CharField(max_length=100, verbose_name='出版社名')
    phone_number = models.CharField(max_length=20, verbose_name='出版社电话')
    email = models.EmailField(verbose_name='出版社邮箱')
    contacts = models.CharField(max_length=40, verbose_name='联系人')
    address = models.CharField(max_length=60, verbose_name='出版社地址')

    class Meta:
        verbose_name = '出版社信息'
        verbose_name_plural = '出版社信息'

    def __str__(self):
        return self.name

