""" Module with CustomerViewSet """
from decimal import Decimal
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import models
from customers.models import Customer
from .models import Loan
from .serializers import LoanSerializer

class LoansViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    # pylint: disable=E1101
    queryset = Loan.objects.all().order_by('id')
    serializer_class = LoanSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # Default validatiosn of serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer')
        customer = Customer.objects.get(pk=customer_id)

        # Check if customer has amount available to request loan
        total_amount = Loan.objects.filter(
            customer=customer,
            status__in=(0, 1)
        ).aggregate(total_amount=models.Sum('amount')
        ).get('total_amount', 0)

        if not total_amount:
            total_amount = 0

        amount = Decimal(request.data.get('amount'))

        if total_amount + amount > customer.score:
            response = {
                "detail": f"You cannot create a loan greater than {customer.score} your current debt is {total_amount}."
            }
            status_code = status.HTTP_400_BAD_REQUEST

            return Response(response, status_code)

        response = super().create(request, *args, **kwargs)
        return response
