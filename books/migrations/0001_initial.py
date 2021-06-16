# Generated by Django 3.2.3 on 2021-06-16 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('writers', '0001_initial'),
        ('publishers', '0002_auto_20210608_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(default='blank', max_length=20, verbose_name='主类名')),
            ],
        ),
        migrations.CreateModel(
            name='ClassificationSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20, verbose_name='子类名')),
                ('ancestor_class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.classification', verbose_name='父分类')),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='书名')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('price_vip', models.DecimalField(decimal_places=2, max_digits=4)),
                ('publish_date', models.DateField(verbose_name='出版日期')),
                ('edition', models.TextField(null=True, verbose_name='版本')),
                ('storage', models.PositiveIntegerField(default=0, verbose_name='存量')),
                ('classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.classification')),
                ('publishers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publishers.publishers', verbose_name='出版社')),
                ('sub_classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.classificationsub')),
                ('writers', models.ManyToManyField(to='writers.Writers', verbose_name='作者/译者')),
            ],
            options={
                'verbose_name': '书籍信息',
                'verbose_name_plural': '书籍信息',
            },
        ),
    ]