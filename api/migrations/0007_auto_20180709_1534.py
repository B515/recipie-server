# Generated by Django 2.0.7 on 2018-07-09 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180708_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='descrption',
            new_name='description',
        ),
    ]
