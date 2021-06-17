from django.db import models

# Create your models here.


class Books(models.Model):
    title = models.CharField(max_length=32, verbose_name='书名')
    writers = models.ManyToManyField(to="writers.Writers", verbose_name='作者/译者')
    price = models.DecimalField(max_digits=4, decimal_places=2)
    price_vip = models.DecimalField(max_digits=4, decimal_places=2)
    publishers = models.ForeignKey(to="publishers.Publishers", verbose_name='出版社', on_delete=models.CASCADE)
    classification = models.ForeignKey(to="Classification", on_delete=models.CASCADE)
    sub_classification = models.ForeignKey(to="ClassificationSub", on_delete=models.CASCADE)
    publish_date = models.DateField(verbose_name='出版日期')
    edition = models.TextField(verbose_name='版本', null=True)
    storage = models.PositiveIntegerField(verbose_name='存量', default=0)

    class Meta:
        verbose_name = '书籍信息'
        verbose_name_plural = '书籍信息'

    def __str__(self):
        return self.title + '--相关图书信息'


class Classification(models.Model):
    class_name = models.CharField(max_length=20, verbose_name='主类名', default='blank')


class ClassificationSub(models.Model):
    class_name = models.CharField(max_length=20, verbose_name='子类名')
    ancestor_class_name = models.ForeignKey(to="Classification", on_delete=models.CASCADE, verbose_name='父分类')