""" Model Payment """
from django.db import models
from customers.models import Customer
from loans.models import Loan
from django.core.validators import MinValueValidator


class Payment(models.Model):
    """ Model Payment """

    STATUS_PAYMENT_CHOICES = (
        (0, 'Completed'),
        (1, 'Rejected'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_id = models.CharField(max_length=60)
    total_amount = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(0)]

    )
    status = models.SmallIntegerField(
        choices=STATUS_PAYMENT_CHOICES,
        default=STATUS_PAYMENT_CHOICES[0][0]
    )
    paid_at = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

class PaymentLoanDetail(models.Model):
    """ Payment Loan Detail """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(0)]
    )

    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        """ Meta """
        unique_together = ('loan', 'payment')
