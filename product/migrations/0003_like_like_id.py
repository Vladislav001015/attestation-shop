# Generated by Django 3.2.5 on 2021-08-16 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210816_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='like_id',
            field=models.IntegerField(default=0),
        ),
    ]
