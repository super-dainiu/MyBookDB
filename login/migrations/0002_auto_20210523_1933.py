# Generated by Django 3.2.3 on 2021-05-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('u_name', models.CharField(max_length=10)),
                ('u_sex', models.CharField(choices=[(0, '男'), (1, '女'), (2, '保密')], max_length=2)),
                ('u_phone', models.CharField(max_length=20)),
                ('u_email', models.CharField(max_length=30)),
                ('u_pwd', models.CharField(max_length=128)),
                ('u_vip', models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='ToDoList',
        ),
    ]
