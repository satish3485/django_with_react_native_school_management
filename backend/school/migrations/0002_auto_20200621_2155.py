# Generated by Django 2.2.7 on 2020-06-21 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='notificationToken',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='notificationToken',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
