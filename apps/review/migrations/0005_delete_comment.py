# Generated by Django 4.2 on 2023-05-04 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_comment_review_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
