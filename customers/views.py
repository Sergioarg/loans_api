""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer
from loans.models import Loan
from django.db import models

from .serializers import CustomerSerializer
from loans.serializers import LoanSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    # pylint: disable=E1101
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    @action(detail=True, methods=['GET'], url_path='/balance/(?P<customer_id>[^/.]+)/balance')
    def get_balance(self, request, customer) -> Response:

        customer = self.get_object()
        total_debt: float = Loan.objects.filter(
            customer=customer,
            status__in=[0, 1]
        ).aggregate(total_debt=models.Sum('outstanding')).get('total_debt', 0)
        score = customer.score
        available_amount: float = score - total_debt

        return Response(
            {
                "external_id": customer.external_id,
                "score": score,
                "available_amount": available_amount,
                "total_debt": total_debt
            },
            status=status.HTTP_200_OK
        )
