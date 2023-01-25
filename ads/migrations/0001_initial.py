# Generated by Django 4.1.4 on 2023-01-25 06:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(10)])),
                ('slug', models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.CharField(max_length=1000)),
                ('is_published', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='image_ad/')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('items', models.ManyToManyField(to='ads.ad')),
            ],
        ),
    ]
