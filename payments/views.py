""" Module with PaymentsViewSet """
from rest_framework import permissions, viewsets

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Payment API
    """
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)
