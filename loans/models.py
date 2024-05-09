""" Model Loans """
from django.db import models
from customers.models import Customer

class Loan(models.Model):
    """ Model Loans """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField()
    contract_version = models.CharField(max_length=30)
    maximun_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField()
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
