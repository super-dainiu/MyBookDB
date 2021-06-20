from django.db import models

# Create your models here.


class Books(models.Model):
    title = models.CharField(max_length=64, verbose_name='Title', db_index=True)
    writers = models.ManyToManyField(to="writers.Writers", verbose_name='Author/Translator', db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Price')
    price_vip = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='VIP Price')
    publishers = models.ForeignKey(to="publishers.Publishers", verbose_name='Publisher', on_delete=models.CASCADE)
    classification = models.ForeignKey(to="Classification", on_delete=models.CASCADE, verbose_name='Category')
    sub_classification = models.ForeignKey(to="ClassificationSub", on_delete=models.CASCADE, verbose_name='Sub-Category')
    publish_date = models.DateField(verbose_name='Publish Date')
    edition = models.TextField(verbose_name='Edition', null=True)
    storage = models.PositiveIntegerField(verbose_name='Storage', default=0)

    class Meta:
        verbose_name = '书籍信息'
        verbose_name_plural = '书籍信息'

        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publishers']),
            models.Index(fields=['classification']),
            models.Index(fields=['sub_classification']),
        ]

    def __str__(self):
        return self.title


class Classification(models.Model):
    class_name = models.CharField(max_length=20, verbose_name='主类名', default='blank')

    def __str__(self):
        return self.class_name


class ClassificationSub(models.Model):
    class_name = models.CharField(max_length=20, verbose_name='子类名')
    ancestor_class_name = models.ForeignKey(to="Classification", on_delete=models.CASCADE, verbose_name='父分类')

    def __str__(self):
        return str(self.ancestor_class_name)+'/'+self.class_name