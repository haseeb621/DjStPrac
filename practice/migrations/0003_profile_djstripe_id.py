# Generated by Django 5.1 on 2024-10-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='djstripe_id',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]
