# pylint: disable=E1101
""" Module to test API """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from loans.models import Loan
from payments.models import Payment, PaymentLoanDetail
from customers.models import Customer

class PaymentsTests(APITestCase):
    """ Test loans app routes """

    def setUp(self):
        customer_id = 1
        self.customer_body = {
            "external_id": "customer_01",
            "score": 3000
        }
        self.loan_body = {
            "amount": 1000,
            "external_id": "loan_01",
            "customer": customer_id
        }
        self.payment_body = {
            "total_amount": 200,
            "external_id": "payment_010",
            "customer": customer_id,
            "payment_loan_detail": [
                {"loan": 1, "amount": 100},
                {"loan": 2, "amount": 200}
            ]
        }
        if not Customer.objects.filter(external_id='customer_01').exists():
            url_customers = reverse('customer-list')
            self.client.post(url_customers, self.customer_body, format='json')

    def test_create_payment_of_customer_without_loans(self):
        """ Test create new user with a loan """
        # Arrange / Act
        url_payments = reverse('payment-list')
        response_payments = self.client.post(url_payments, self.payment_body, format='json')
        response_expected = {'message': 'This customer has no loans'}

        # Assert
        self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_payments.json(), response_expected)
