# Generated by Django 2.2.16 on 2022-08-02 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=16, verbose_name='confirmation_code'),
        ),
    ]
