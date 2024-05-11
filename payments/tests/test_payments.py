# # pylint: disable=E1101
# """ Module to test API """
# from django.contrib.auth.models import User
# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from loans.models import Loan
# from payments.models import Payment, PaymentLoanDetail
# from customers.models import Customer

# class PaymentsTests(APITestCase):
#     """ Test Payments Services """

#     def setUp(self):

#         test_customer_id_one = 1
#         test_customer_id_two = 1

#         self.customer_body_one = {
#             "external_id": "customer_01",
#             "score": 5000
#         }
#         self.customer_body_two = {
#             "external_id": "customer_02",
#             "score": 6000
#         }

#         self.loan_body = {
#             "amount": 3000,
#             "external_id": "loan_01",
#             "customer": test_customer_id_one
#         }

#         self.loan_body_two = {
#             "amount": 3000,
#             "external_id": "loan_02",
#             "customer": test_customer_id_two
#         }

#         self.payment_body = {
#             "total_amount": 2000,
#             "external_id": "payment_01",
#             "customer": test_customer_id_one,
#             "payment_loan_detail": [
#             ]
#         }

#         self.url_payments = reverse('payment-list')
#         self.url_loans = reverse('loan-list')

#         User.objects.create_user(username="test", password="test")
#         auth_url = reverse("api-token-auth")
#         test_user_body = {"username": "test", "password": "test"}
#         response = self.client.post(auth_url, test_user_body, format='json')
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.data['token'])

#         if not Customer.objects.filter(external_id='customer_01').exists():
#             url_customers = reverse('customer-list')
#             self.client.post(url_customers, self.customer_body_one, format='json')

#     def test_create_payment_of_customer_without_loans(self):
#         """ Test create new user with a loan """
#         # Arrange / Act
#         response_payments = self.client.post(self.url_payments, self.payment_body, format='json')

#         # Assert
#         self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_create_payment_greater_than_total_debts(self):
#         """ Test create new user with a loan """
#         # Arrange / Act
#         self.client.post(self.url_loans, self.loan_body, format='json')

#         self.payment_body['total_amount'] = 7000
#         response_payments = self.client.post(self.url_payments, self.payment_body, format='json')
#         response_expected = {'total_amount': ['total_amount is greater than total debts']}

#         # Assert
#         self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response_payments.json(), response_expected)

#     def test_create_payment_loan_01(self):
#         """ Test create new user with a loan """
#         # Arrange / Act
#         self.client.post(self.url_loans, self.loan_body, format='json')

#         response_payments = self.client.post(self.url_payments, self.payment_body, format='json')
#         breakpoint()

#         # Assert
#         self.assertEqual(response_payments.status_code, status.HTTP_400_BAD_REQUEST)
