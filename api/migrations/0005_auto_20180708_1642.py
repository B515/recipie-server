# Generated by Django 2.0.7 on 2018-07-08 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_recipe_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='belong',
        ),
        migrations.AddField(
            model_name='recipe',
            name='Tag',
            field=models.ManyToManyField(to='api.Tag'),
        ),
    ]
