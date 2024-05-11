""" Module with PaymentsViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from utils import calculate_total_debt
from customers.models import Customer
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Payment API
    """
    # pylint: disable=E1101
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # Customizing POST method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer')
        customer = Customer.objects.get(pk=customer_id)
        total_debt = calculate_total_debt(customer)

        # Check if customer has loans
        if total_debt == 0:
            response = {"message": "This customer has no loans"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)

        # Check payment are greater than total_debt
        payment = request.data.get('total_amount')
        if payment > total_debt:
            response = {"message": "total_amount is greater than total debts"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        

        response = super().create(request, *args, **kwargs)
        return response
