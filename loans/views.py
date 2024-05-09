""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
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

    @action(detail=False, methods=['GET'], url_path='customer/(?P<customer_id>[^/.]+)')
    def get_loans_by_customer(self, request, customer_id=None):
        """ Retrive all loans by customer id """
        loans = self.queryset.filter(customer_id=customer_id)
        serializer = self.serializer_class(loans, many=True)

        return Response(serializer.data)
