# Generated by Django 2.1.4 on 2019-01-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', unique=True),
        ),
    ]
