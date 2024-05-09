""" Model Payment """
from django.db import models
from customers.models import Customer
from loans.models import Loan

class Payment(models.Model):
    """ Model Payment """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField()
    paid_at = models.DateTimeField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

class PaymentLoanDetail(models.Model):
    """ Payment Loan Detail """
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        """ Meta """
        unique_together = ('loan', 'payment')
