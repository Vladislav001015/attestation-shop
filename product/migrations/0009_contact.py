# Generated by Django 3.2.5 on 2021-08-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_like_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=30)),
            ],
        ),
    ]