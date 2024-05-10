""" Model Payment """
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from customers.models import Customer
from loans.models import Loan


class Payment(models.Model):
    """ Model Payment """

    STATUS_PAYMENT_CHOICES = (
        (1, 'Completed'),
        (2, 'Rejected'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(Decimal('0.00'))]

    )
    status = models.SmallIntegerField(
        choices=STATUS_PAYMENT_CHOICES,
        default=STATUS_PAYMENT_CHOICES[0][0]
    )
    paid_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class PaymentLoanDetail(models.Model):
    """ Payment Loan Detail """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount = models.DecimalField(
        max_digits=20, decimal_places=10,
        validators=[MinValueValidator(0)]
    )

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    class Meta:
        """ Meta """
        unique_together = ('loan', 'payment')
