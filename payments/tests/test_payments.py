# pylint: disable=E1101
""" Module to test API """
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from constans import LOANS_STATUS
class PaymentsTests(APITestCase):
    """ Test Payments Services """

    def setUp(self):

        self.customer_body = {
            "external_id": "customer_01",
            "score": 5000
        }

        self.loan_body = {
            "amount": 3000,
            "external_id": "loan_01",
            "customer": 1
        }

        self.payment_body = {
            "total_amount": 3000,
            "external_id": "payment_01",
            "customer": 1,
            "payment_loan_details": [
                {"loan": 1, "amount": 3000}
            ]
        }

        self.loans_url = reverse('loan-list')
        self.payments_url = reverse('payment-list')

        User.objects.create_user(username="test", password="test")
        auth_url = reverse("api-token-auth")
        test_user_body = {"username": "test", "password": "test"}
        response = self.client.post(auth_url, test_user_body, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

        if not Customer.objects.filter(external_id='customer_01').exists():
            url_customers = reverse('customer-list')
            self.client.post(url_customers, self.customer_body, format='json')

    def test_create_payment_of_customer_without_loans(self):
        """ Test create new user with a loan """
        # Arrange / Act
        response_payments = self.client.post(self.payments_url, self.payment_body, format='json')

        # Assert
        self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_greater_than_total_debts(self):
        """ Test create grather than total debts """
        # Arrange / Act
        self.client.post(self.loans_url, self.loan_body, format='json')

        self.payment_body['total_amount'] = 7000
        response_payments = self.client.post(self.payments_url, self.payment_body, format='json')

        # Assert
        self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_with_out_payment_loans_details_key(self):
        """ Test create grather than total debts """
        # Arrange / Act
        self.payment_body["payment_loan_detail"] = self.payment_body.pop("payment_loan_details")
        self.client.post(self.loans_url, self.loan_body, format='json')

        response_payments = self.client.post(self.payments_url, self.payment_body, format='json')

        # Assert
        self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_correct_and_check_loan_status_paid(self):
        """ Test create grather than total debts """
        # Arrange / Act
        create_loan = self.client.post(self.loans_url, self.loan_body, format='json')
        response_payments = self.client.post(self.payments_url, self.payment_body, format='json')
        get_loan = self.client.get(f"{self.loans_url}1/").data

        # Assert
        self.assertEqual(get_loan.get('status'), LOANS_STATUS["PAID"])
        self.assertEqual(get_loan.get('outstanding'), '0.00')
        self.assertEqual(create_loan.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_payments.status_code, status.HTTP_201_CREATED)
