from django.db import models

# Create your models here.


class Orders(models.Model):
    id = models.CharField(max_length=64, verbose_name='Order ID', primary_key=True)
    last_edit = models.DateTimeField(verbose_name='Last Edit')
    date = models.DateField(verbose_name='Date')
    user = models.ForeignKey(to="users.User", verbose_name='User', on_delete=models.CASCADE)
    book = models.ManyToManyField(to="books.Books", through="Details", through_fields=('order', 'book'),
                                  verbose_name='Books')

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = '订单信息'


class Details(models.Model):
    book = models.ForeignKey(to='books.Books', on_delete=models.CASCADE)
    order = models.ForeignKey(to='orders.Orders', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Price')
    count = models.PositiveIntegerField(verbose_name='Count', default=0)
