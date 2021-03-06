# Generated by Django 3.2.3 on 2021-06-20 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writers', '0004_auto_20210621_0054'),
        ('books', '0008_auto_20210621_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(db_index=True, max_length=64, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='books',
            name='writers',
            field=models.ManyToManyField(db_index=True, to='writers.Writers', verbose_name='Author/Translator'),
        ),
    ]
