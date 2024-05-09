# Generated by Django 5.0.4 on 2024-05-09 18:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0003_alter_customer_created_at_alter_customer_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('external_id', models.CharField(max_length=60)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.SmallIntegerField(choices=[(1, 'Pending'), (2, 'Active'), (3, 'Rejected'), (4, 'Paid')], default=1)),
                ('contract_version', models.CharField(blank=True, max_length=30, null=True)),
                ('maximun_payment_date', models.DateTimeField(blank=True, null=True)),
                ('taken_at', models.DateTimeField(blank=True, null=True)),
                ('outstanding', models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]
