# Generated by Django 3.1.2 on 2020-10-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanManagement', '0015_auto_20201027_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
