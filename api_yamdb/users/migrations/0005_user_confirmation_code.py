# Generated by Django 2.2.16 on 2022-08-02 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220802_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]
