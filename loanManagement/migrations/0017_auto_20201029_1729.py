# Generated by Django 3.1.2 on 2020-10-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanManagement', '0016_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
