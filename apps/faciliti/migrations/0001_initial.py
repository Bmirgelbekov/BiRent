# Generated by Django 4.2 on 2023-05-03 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faciliti',
            fields=[
                ('slug', models.SlugField(blank=True, max_length=80, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'verbose_name': 'Удобства',
                'verbose_name_plural': 'Удобства',
            },
        ),
    ]
