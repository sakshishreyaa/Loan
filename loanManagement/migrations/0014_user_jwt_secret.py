# Generated by Django 3.1.2 on 2020-10-25 18:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loanManagement', '0013_auto_20201025_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
