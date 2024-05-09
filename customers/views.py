""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer
from loans.models import Loan
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

    
