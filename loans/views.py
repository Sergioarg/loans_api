# pylint: disable=E1101
""" Module with LoanViewSet """
from rest_framework import viewsets, permissions
from .models import Loan
from .serializers import LoanSerializer

class LoansViewSet(viewsets.ModelViewSet):
    """ Loans ViewSet """
    queryset = Loan.objects.all().order_by('id')
    serializer_class = LoanSerializer
    permission_classes = (permissions.IsAuthenticated,)
