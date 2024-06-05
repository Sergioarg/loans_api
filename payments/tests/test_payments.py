""" Module of Payment's Tests """
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer
from utils.states import LoanStatus, PaymentStatus


class PaymentsTests(APITestCase):
    """ Test Payments Actions """
    def setUp(self):
        self.loans_url = reverse('loan-list')
        self.payments_url = reverse('payment-list')
        self.auth_url = reverse("api-token-auth")
        self.url_customers = reverse('customer-list')

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
        self.__create_user()
        self.__get_auth_token()


    # Private Methods ---------------------------------------------------------
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

    def __create_payment(self, payment_body: dict) -> None:
        """ Create a new payment """
        response = self.client.post(self.payments_url, payment_body, format='json')

        return response

    # Tests -------------------------------------------------------------------
    def test_create_payment_of_customer_without_loans(self):
        """ Test create new user with a loan """
        # Arrange / Act
        response_payment = self.__create_payment(self.payment_body)

        # Assert
        self.assertEqual(response_payment.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_greater_than_total_debts(self):
        """ Test create grather than total debts """
        # Arrange / Act
        self.client.post(self.loans_url, self.loan_body, format='json')

        self.payment_body['total_amount'] = 7000
        response_payment = self.__create_payment(self.payment_body)

        # Assert
        self.assertEqual(response_payment.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_without_payment_loans_details_key(self):
        """ Test create grather than total debts """
        # Arrange / Act
        self.payment_body.pop("payment_loan_details")
        self.client.post(self.loans_url, self.loan_body, format='json')

        response_payment = self.__create_payment(self.payment_body)

        # Assert
        self.assertEqual(response_payment.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_with_payment_loans_details_key_diffrent_as_list(self):
        """ Test create grather than total debts """
        # Arrange / Act
        self.payment_body["payment_loan_details"] = "TEST"
        self.client.post(self.loans_url, self.loan_body, format='json')
        response_payment = self.__create_payment(self.payment_body)

        # Assert
        self.assertEqual(response_payment.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_correct_and_check_loan_status_paid(self):
        """ Test create grather than total debts """
        # Arrange / Act
        create_loan = self.client.post(self.loans_url, self.loan_body, format='json')
        response_payment = self.__create_payment(self.payment_body)
        loan = self.client.get(f"{self.loans_url}1/").data

        # Assert
        self.assertEqual(loan.get('status'), LoanStatus.PAID.value)
        self.assertEqual(loan.get('outstanding'), '0.00')
        self.assertEqual(create_loan.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_payment.status_code, status.HTTP_201_CREATED)

    def test_create_payment_status_rejected_and_check_loan_outstanding(self):
        """ Test create payment with status rejected than total debts """
        # Arrange / Act
        create_loan = self.client.post(self.loans_url, self.loan_body, format='json')
        self.payment_body["status"] = PaymentStatus.REJECTED.value
        response_payment = self.__create_payment(self.payment_body)

        get_loan = self.client.get(f"{self.loans_url}1/").data
        total_amount = float(response_payment.data.get('total_amount'))
        # Assert
        self.assertEqual(get_loan.get('status'), LoanStatus.PENDING.value)
        self.assertEqual(float(get_loan.get('outstanding')), total_amount)
        self.assertEqual(create_loan.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_payment.status_code, status.HTTP_201_CREATED)
