# pylint: disable=E1101
from customers.models import Customer
from loans.models import Loan
from django.db import models



def calculate_total_debt(customer: Customer) -> float:
    """
    Calcula el total de la deuda para un cliente específico.
    """
    total_debt = Loan.objects.filter(
        customer=customer,
        status__in=[0, 1]
    ).aggregate(total_debt=models.Sum('outstanding')).get('total_debt', 0)

    if not total_debt:
        total_debt = 0

    return total_debt
