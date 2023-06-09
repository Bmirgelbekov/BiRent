# Generated by Django 4.2 on 2023-05-02 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0002_alter_apartmentreview_sub_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartmentreview',
            name='sub_comments',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_comment', models.TextField()),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_comments', to='review.apartmentreview')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
            },
        ),
    ]
