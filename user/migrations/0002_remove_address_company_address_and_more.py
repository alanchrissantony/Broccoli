# Generated by Django 5.0.2 on 2024-05-12 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='company_address',
        ),
        migrations.RemoveField(
            model_name='address',
            name='company_name',
        ),
    ]
