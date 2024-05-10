""" Model Loans """
from django.db import models
from django.core.validators import MinValueValidator
from rest_framework import serializers
from customers.models import Customer

class Loan(models.Model):
    """ Model Loans """
    STATUS_LOANS_CHOICES = (
        (1, 'Pending'),
        (2, 'Active'),
        (3, 'Rejected'),
        (4, 'Paid'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)]

    )
    status = models.SmallIntegerField(
        choices=STATUS_LOANS_CHOICES,
        default=STATUS_LOANS_CHOICES[0][0]
    )

    contract_version = models.CharField(max_length=30, null=True, blank=True)
    maximun_payment_date = models.DateTimeField(null=True, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)

    outstanding = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def clean(self):
        # pylint: disable=E1101
        credit_avaliable = self.customer.score
        amounts = Loan.objects.filter(
            customer=self.customer,
            status__in=(0, 1)
        ).aggregate(total_amount=models.Sum('amount')).get('total_amount', 0)

        total_amount = amounts + self.amount
        if total_amount > credit_avaliable:
            raise serializers.ValidationError({
                "detail": f"You cannot create a loan greater than this amount: {credit_avaliable}."
            })

    def save(self, *args, **kwargs):
        if not self.pk:
            self.outstanding = self.amount
        self.clean()
        super().save(*args, **kwargs)
