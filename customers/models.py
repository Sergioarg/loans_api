""" Model Customer """
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    """ Model Customer """

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField()
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField()
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(default=timezone.now)
