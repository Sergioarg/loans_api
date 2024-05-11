# pylint: disable=E1101
""" Module to test Loans API """
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from loans.models import Loan
from constans import LOANS_STATUS

class LoansTests(APITestCase):
    """ Test Loans app routes """

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
        self.customers_url = reverse('customer-list')
        self.url_loans = reverse('loan-list')

        # User Auth
        User.objects.create_user(username="test", password="test")
        auth_url = reverse("api-token-auth")
        test_user_body = {"username": "test", "password": "test"}
        response = self.client.post(auth_url, test_user_body, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

    def test_create_loan(self):
        """ Test create new user with a loan """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')
        response_loans = self.client.post(self.url_loans, self.loan_body, format='json')

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
        self.assertEqual(Loan.objects.get().status, LOANS_STATUS['PENDING'])
        self.assertEqual(response_loans.data, response_expected)

    def test_create_loan_grater_than_score(self):
        """ Test try to create new user with a loan greater than the score """

        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.loan_body["amount"] = 4000
        response_loan = self.client.post(self.url_loans, self.loan_body, format='json')

        # Assert
        self.assertEqual(response_loan.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_creta_loan_get_customer_loans(self):
        """ Test create a new loan and test customer endpoint """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.client.post(self.url_loans, self.loan_body, format='json')
        response_loans = self.client.get(f'{self.customers_url}1/loans/')

        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_loans.data), 1)

    def test_create_loan_with_existing_external_id(self):
        """ Test create customer with existing external_id """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.client.post(self.url_loans, self.loan_body, format='json')

        response = self.client.post(self.url_loans, self.loan_body, format='json')
        expected_result = {'external_id': ['loan with this external id already exists.']}

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_result)


    def test_create_loan_with_status_active(self):
        """ Test create new user loan with status active (2) """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.loan_body['status'] = LOANS_STATUS['ACTIVE']
        response_loans = self.client.post(self.url_loans, self.loan_body, format='json')


        response_expected = {
            'external_id': 'loan_01',
            'amount': '1000.00',
            'status': 2,
            'outstanding': '1000.00',
            'customer_external_id': 'customer_01'
        }

        loan = Loan.objects.get()
        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_201_CREATED)
        self.assertEqual(loan.taken_at.date(), datetime.now().date())
        self.assertEqual(loan.status, LOANS_STATUS['ACTIVE'])
        self.assertEqual(response_loans.data, response_expected)

    def test_create_loan_with_status_rejected(self):
        """ Test create new user loan with status rejected (3) """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.loan_body['status'] = LOANS_STATUS['REJECTED']
        response_loans = self.client.post(self.url_loans, self.loan_body, format='json')

        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_loan_with_status_paid(self):
        """ Test create new user loan with status paid (4) """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        self.loan_body['status'] = LOANS_STATUS['PAID']
        response_loans = self.client.post(self.url_loans, self.loan_body, format='json')

        # Assert
        self.assertEqual(response_loans.status_code, status.HTTP_400_BAD_REQUEST)
