""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    # pylint: disable=E1101
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    # permission_classes = (permissions.IsAuthenticated,)
