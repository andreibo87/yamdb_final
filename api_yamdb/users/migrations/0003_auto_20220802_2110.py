# Generated by Django 2.2.16 on 2022-08-02 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220802_0715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]