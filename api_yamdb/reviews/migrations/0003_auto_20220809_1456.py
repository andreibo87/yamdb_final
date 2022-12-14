# Generated by Django 2.2.16 on 2022-08-09 11:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220805_1548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('year',)},
        ),
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_name_year',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
