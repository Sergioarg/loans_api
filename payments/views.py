""" Module with CustomerViewSet """
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from customers.models import Customer
from .serializers import PaymentSerializer
from utils import calculate_total_debt


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    # pylint: disable=E1101
    queryset = Payment.objects.all().order_by('id')
    serializer_class = PaymentSerializer
    # permission_classes = (permissions.IsAuthenticated,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer')
        customer = Customer.objects.get(pk=customer_id)
        total_debt = calculate_total_debt(customer)

        if total_debt == 0:
            response = {"message": "This customer has no loans"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        return response
