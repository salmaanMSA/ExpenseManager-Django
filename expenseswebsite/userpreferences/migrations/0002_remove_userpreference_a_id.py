# Generated by Django 3.1.4 on 2021-01-28 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='a_id',
        ),
    ]
