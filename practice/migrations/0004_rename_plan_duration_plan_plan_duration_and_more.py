# Generated by Django 5.1 on 2024-10-31 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_profile_djstripe_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='Plan_duration',
            new_name='plan_duration',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='Plan_Type',
            new_name='plan_type',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='Customer',
            new_name='customer',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='price_id',
        ),
        migrations.AddField(
            model_name='plan',
            name='features',
            field=models.TextField(default='Enter plan features separated by commas.'),
        ),
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(default='Add plan name here', max_length=100),
        ),
        migrations.AddField(
            model_name='plan',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]