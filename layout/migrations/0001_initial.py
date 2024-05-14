# Generated by Django 5.0.2 on 2024-05-08 22:11

import core.models
import functools
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to=functools.partial(core.models.image_upload_path, *(), **{'folder': 'products'}))),
            ],
        ),
    ]
