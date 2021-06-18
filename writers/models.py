from django.db import models

# Create your models here.


class Writers(models.Model):
    AUTHOR_TYPE_CHOICE = (
        ('1', 'Author'),
        ('2', 'Translator')
    )
    name = models.CharField(max_length=40, verbose_name='Name')

    author_type = models.CharField(max_length=20, choices=AUTHOR_TYPE_CHOICE, verbose_name='Author type')

    class Meta:
        verbose_name = '作/译者信息'
        verbose_name_plural = '作/译者信息'

    def __str__(self):
        if self.author_type == 'Author':
            return '[作]'+self.name
        if self.author_type == 'Translator':
            return '[译]'+self.name