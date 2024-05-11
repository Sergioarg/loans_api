""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from loans.models import Loan
from loans.serializers import LoanSerializer
from utils import calculate_total_debt

from payments.models import Payment
from payments.serializers import PaymentSerializer

from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet of Customer model
    """
    # pylint: disable=E1101, W0613
    queryset = Customer.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=True, methods=['GET'])
    def loans(self, request, pk) -> Response:

        """ Retrive all loans by customer id """
        customer = self.get_object()
        loans = Loan.objects.filter(customer=customer)
        serializer = LoanSerializer(loans, many=True)

        return Response(serializer.data)


    @action(detail=True, methods=['GET'])
    def balance(self, request, pk) -> Response:
        """ Returns all loans realted with the customer """

        customer = self.get_object()
        total_debt = calculate_total_debt(customer=customer)

        score = customer.score
        available_amount = score - total_debt

        return Response(
            {
                "external_id": customer.external_id,
                "score": score,
                "available_amount": available_amount,
                "total_debt": total_debt
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'])
    def payments(self, request, pk) -> Response:
        """ Retrive all payments of the user customer id """
        customer = self.get_object()
        payments = Payment.objects.filter(customer=customer)

        payments_serializer = PaymentSerializer(payments, many=True)

        return Response(payments_serializer.data, status=status.HTTP_200_OK)
