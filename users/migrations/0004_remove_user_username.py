# Generated by Django 3.2.3 on 2021-06-01 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]