""" Model Customer """
from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    """ Model Customer """
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )

    score = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    preapproved_at = models.DateTimeField(null=True, blank=True)
