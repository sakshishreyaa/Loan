# Generated by Django 3.1.2 on 2020-10-25 12:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loanManagement', '0012_auto_20201023_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loan',
            name='modified_date',
            field=models.DateField(auto_now=True),
        ),
    ]
