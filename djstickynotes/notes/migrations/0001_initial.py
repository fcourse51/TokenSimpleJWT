# Generated by Django 5.0.4 on 2024-04-28 09:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StickyNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
