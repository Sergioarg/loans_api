# pylint: disable=E1101
from django.db import models
from customers.models import Customer
from loans.models import Loan

def calculate_total_debt(customer: Customer) -> float:
    """Calculate the total debt of the customer

    Args:
        customer (Customer): instance of customer

    Returns:
        float: total debt of customer if the customer does not have return 0
    """
    total_debt = Loan.objects.filter(
        customer=customer,
        status__in=[0, 1]
    ).aggregate(total_debt=models.Sum('outstanding')).get('total_debt', 0)

    if not total_debt:
        total_debt = 0

    return total_debt
