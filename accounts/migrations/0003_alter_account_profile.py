# Generated by Django 5.0.2 on 2024-06-20 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile',
            field=models.CharField(default=False, max_length=255),
        ),
    ]