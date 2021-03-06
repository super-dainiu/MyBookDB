# Generated by Django 3.2.3 on 2021-06-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Writers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='作者名')),
                ('author_type', models.CharField(choices=[('1', 'original_author'), ('2', 'translator_author')], max_length=20)),
            ],
            options={
                'verbose_name': '作/译者信息',
                'verbose_name_plural': '作/译者信息',
            },
        ),
    ]
