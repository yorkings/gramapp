# Generated by Django 4.2.1 on 2023-06-08 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
    ]
