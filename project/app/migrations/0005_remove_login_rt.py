# Generated by Django 5.0.1 on 2024-01-10 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_login_rt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='rt',
        ),
    ]
