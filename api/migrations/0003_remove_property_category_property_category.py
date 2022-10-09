# Generated by Django 4.1 on 2022-10-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='category',
        ),
        migrations.AddField(
            model_name='property',
            name='category',
            field=models.ManyToManyField(to='api.category'),
        ),
    ]
