# Generated by Django 2.1.4 on 2019-01-02 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='skills',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='_skills',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
