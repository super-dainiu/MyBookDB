from django.db import models

# Create your models here.


class Writers(models.Model):
    AUTHOR_TYPE_CHOICE = (
        ('1', 'Author'),
        ('2', 'Translator')
    )
    name = models.CharField(max_length=40, verbose_name='作者名')

    author_type = models.CharField(max_length=20, choices=AUTHOR_TYPE_CHOICE)

    class Meta:
        verbose_name = '作/译者信息'
        verbose_name_plural = '作/译者信息'