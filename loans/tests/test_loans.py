""" Module to test API """
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from loans.models import Loan

# pylint: disable=E1101
class LoansTests(APITestCase):
    """ Testing API """
    def setUp(self):
        self.customer_body = {
            "external_id": "customer_01",
            "score": 3000
        }
        self.loan_body = {
            "amount": 1000,
            "external_id": "loan_01",
            "customer": 1
        }

    def test_create_loan(self):
        """ Test create new user with a loan """
        # Arrange / Act
        url_customers = reverse('customer-list')
        self.client.post(url_customers, self.customer_body, format='json')

        url_loans = reverse('loan-list')
        response_loans = self.client.post(url_loans, self.loan_body, format='json')

        response_expected = {
            'external_id': 'loan_01',
            'amount': '1000.00',
            'status': 1,
            'outstanding': '1000.00',
            'customer_external_id': 'customer_01'
        }

        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.get().external_id, 'loan_01')
        self.assertEqual(response_loans.data, response_expected)

    def test_create_loan_grater_than_score(self):
        """ Test try to create new user with a loan greater than the score """

        # Arrange / Act
        url_customers = reverse('customer-list')
        self.client.post(url_customers, self.customer_body, format='json')

        url_loans = reverse('loan-list')
        self.loan_body["amount"] = 4000
        response_loan = self.client.post(url_loans, self.loan_body, format='json')

        # Assert
        self.assertEqual(response_loan.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creta_loan_get_customer_loans(self):
        """ Test create a new loan and test customer endpoint """
        # Arrange / Act
        url_customers = reverse('customer-list')
        self.client.post(url_customers, self.customer_body, format='json')

        url_loans = reverse('loan-list')
        self.client.post(url_loans, self.loan_body, format='json')
        response_loans = self.client.get('/customers/1/loans/')

        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_loans.data), 1)
