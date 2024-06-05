""" Module to test Customer Services """
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from utils.calculations import calculate_total_debt

class CustomersTests(APITestCase):
    """ Test customers app routes """
    def setUp(self):
        self.customers_url = reverse('customer-list')

        self.customer_body = {
            "external_id": "customer_01",
            "score": 1000.00
        }

        self.__create_user()
        self.__get_auth_token()

    def __create_user(self):
        """ Create test user """
        User.objects.create_user(username="test", password="test")

    def __get_auth_token(self) -> None:
        """ Get auth token """
        test_user_body = {"username": "test", "password": "test"}
        response = self.client.post(self.auth_url, test_user_body, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {response.data["token"]}')

        if not Customer.objects.filter(external_id='customer_01').exists():
            self.client.post(self.url_customers, self.customer_body, format='json')

    # Tests -------------------------------------------------------------------
    def test_create_customer(self):
        """ Test create new customer """
        # Arrange / Act
        response = self.client.post(self.customers_url, self.customer_body, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().external_id, 'customer_01')

    def test_get_customer(self):
        """ Test get customer by id """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'{self.customers_url}{customer_id}/')
        customer_expected = {
            'score': '1000.00',
            'status': 1,
            'external_id': 'customer_01',
            'preapproved_at': None
        }
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, customer_expected)

    def test_get_customers(self):
        """ Test get customers created """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')
        other_customer = {
            "external_id": "customer_02",
            "score": 2000.00
        }
        self.client.post(self.customers_url, other_customer, format='json')

        response = self.client.get(self.customers_url)
        customer_expected = {
            'score': '1000.00',
            'status': 1,
            'external_id': 'customer_01',
            'preapproved_at': None
        }
        other_customer_expected = {
            'score': '2000.00',
            'status': 1,
            'external_id': 'customer_02',
            'preapproved_at': None
        }

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(response.data['results'][0], customer_expected)
        self.assertEqual(response.data['results'][1], other_customer_expected)

    def test_get_customer_balance(self):
        """Test creating a new user"""
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'{self.customers_url}{customer_id}/balance/')
        response_expected = {
            'external_id': 'customer_01',
            'score': Decimal('1000.00'),
            'available_amount': Decimal('1000.00'),
            'total_debt': 0
        }
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_expected)

    def test_get_customer_loans(self):
        # Arrange / Act
        """ Test create get loans of customer """
        self.client.post(self.customers_url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'{self.customers_url}{customer_id}/loans/')
        response_expected = []
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_expected)

    def test_get_customer_payments(self):
        # Arrange / Act
        """ Test create get payments of customer """
        self.client.post(self.customers_url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'{self.customers_url}{customer_id}/payments/')
        response_expected = []
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_expected)

    def test_create_customer_existing_external_id(self):
        """ Test create customer with existing external_id """
        # Arrange / Act
        self.client.post(self.customers_url, self.customer_body, format='json')

        response = self.client.post(self.customers_url, self.customer_body, format='json')
        expected_result = {'external_id': ['customer with this external id already exists.']}

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_result)

    def test_initial_calculate_total_debt(self):
        """ Test create new customer """
        # Arrange / Act
        customer = Customer.objects.create(**self.customer_body)
        total_debt = calculate_total_debt(customer=customer)
        # Assert
        self.assertEqual(total_debt, 0)
