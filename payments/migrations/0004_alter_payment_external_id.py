# Generated by Django 5.0.4 on 2024-05-09 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_rename_loan_id_paymentloandetail_loan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='external_id',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]