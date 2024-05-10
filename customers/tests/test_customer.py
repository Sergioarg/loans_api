""" Module to test API """
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer

# pylint: disable=E1101
class CustomersTests(APITestCase):
    """ Testing API """
    def setUp(self):
        self.customer_body = {
            "external_id": "customer_01",
            "score": 1000.00
        }

    def test_create_customer(self):
        """ Test create new customer """
        # Arrange / Act
        url = reverse('customer-list')
        response = self.client.post(url, self.customer_body, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().external_id, 'customer_01')

    def test_get_customer(self):
        """ Test get customer by id """
        # Arrange / Act
        url = reverse('customer-list')
        self.client.post(url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'/customers/{customer_id}/')
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
        url = reverse('customer-list')
        self.client.post(url, self.customer_body, format='json')
        other_customer = {
            "external_id": "customer_02",
            "score": 2000.00
        }
        self.client.post(url, other_customer, format='json')

        response = self.client.get('/customers/')
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
        url = reverse('customer-list')
        self.client.post(url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'/customers/{customer_id}/balance/')
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
        url = reverse('customer-list')
        self.client.post(url, self.customer_body, format='json')
        customer_id = 1
        response = self.client.get(f'/customers/{customer_id}/loans/')
        response_expected = []
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_expected)

    def test_create_customer_existing_external_id(self):
        """ Test create customer with existing external_id """
        # Arrange / Act
        url = reverse('customer-list')
        self.client.post(url, self.customer_body, format='json')

        response = self.client.post(url, self.customer_body, format='json')
        expected_result = {'external_id': ['customer with this external id already exists.']}

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_result)
