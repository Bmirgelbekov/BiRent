# Generated by Django 4.2 on 2023-05-03 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faciliti', '0001_initial'),
        ('apartment', '0002_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'Апартаменты', 'verbose_name_plural': 'Апартаменты'},
        ),
        migrations.AddField(
            model_name='apartment',
            name='faciliti',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartments', to='faciliti.faciliti'),
        ),
    ]