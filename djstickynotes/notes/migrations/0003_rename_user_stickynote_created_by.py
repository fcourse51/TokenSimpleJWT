# Generated by Django 5.0.4 on 2024-04-28 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_stickynote_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stickynote',
            old_name='user',
            new_name='created_by',
        ),
    ]
