""" Module with CustomerViewSet """
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # pylint: disable=E1101
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
