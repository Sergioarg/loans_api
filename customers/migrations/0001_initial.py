# Generated by Django 5.0.4 on 2024-05-09 00:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('external_id', models.CharField(max_length=60, unique=True)),
                ('status', models.SmallIntegerField()),
                ('score', models.DecimalField(decimal_places=2, max_digits=12)),
                ('preapproved_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
