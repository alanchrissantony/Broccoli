# Generated by Django 5.0.2 on 2024-07-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(db_index=True, max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
