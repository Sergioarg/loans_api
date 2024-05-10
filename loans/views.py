""" Module with CustomerViewSet """
from rest_framework import viewsets
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
