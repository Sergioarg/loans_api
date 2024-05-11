# pylint: disable=E1101
""" Module Serilizers """
from rest_framework import serializers

from constans import LOANS_STATUS
from customers.models import Customer
from loans.models import Loan
from utils import calculate_total_debt

from .models import Payment, PaymentLoanDetail


class PaymentLoanDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        """ Class Meta"""
        model = PaymentLoanDetail
        fields = (
            "amount",
            "loan",
        )
        # "payment"

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payments and PaymentLoanDetail model.
    """
    payment_loan_details = PaymentLoanDetailSerializer(many=True)
    class Meta:
        """ Class Meta"""
        model = Payment
        fields = (
            "id",
            "total_amount",
            "status",
            "paid_at",
            "external_id",
            "customer",
            "payment_loan_details"
        )

    def validate_total_amount(self, total_amount):
        """Validate payment data received

        Args:
            data (dict): data of the payment

        Raises:
            serializers.ValidationError: in case customer dont have lons
            serializers.ValidationError: _description_

        Returns:
            dict: data of payment
        """
        customer_id = self.initial_data.get('customer')
        customer = Customer.objects.get(pk=customer_id)
        total_debt = calculate_total_debt(customer)

        # Check if customer has loans
        if total_debt == 0:
            raise serializers.ValidationError({
                "details": "This customer has no loans"
            })

        # Check payment are greater than total_debt
        if total_amount > total_debt:
            raise serializers.ValidationError({
                "total_amount": "total_amount is greater than total debts"
            })

        return total_amount

    def validate_payment_loan_details(self, payment_loan_details_data):
        """Validate payment loan details receivedd

        Args:
            payment_loan_details_data (list): list of dicts with info of payments

        Raises:
            serializers.ValidationError: Loan of other customer
            serializers.ValidationError: try to pay more

        Returns:
            dict: loans details with correct data
        """
        customer_id = self.initial_data.get('customer')
        customer = Customer.objects.get(pk=customer_id)

        for detail_data in payment_loan_details_data:
            loan = detail_data.get('loan')
            detail_data_amount = detail_data.get('amount')

            # Validate customer loans
            if customer != loan.customer:
                raise serializers.ValidationError({
                    "loan": f"This loan id {detail_data.get('loan').id} is invalid"
                })

            # Check if outstanding
            if detail_data_amount > loan.outstanding:
                raise serializers.ValidationError({
                    "amount": f"Amount {round(detail_data_amount, 2)} paid is greater than outstanding {loan.outstanding}"
                })

        return payment_loan_details_data

    def create(self, validated_data):
        payment_loan_details_data = validated_data.pop("payment_loan_details")

        payment = Payment.objects.create(**validated_data)
        for detail_data in payment_loan_details_data:
            loan = detail_data.get('loan')
            loan.outstanding = round(loan.outstanding - detail_data.get('amount'), 2)

            if loan.outstanding == 0:
                loan.status = LOANS_STATUS['PAID']
            loan.save()
            PaymentLoanDetail.objects.create(payment=payment, **detail_data)

        return payment

    # def update(self, instance, validated_data):
    #     payment_loan_details_data = validated_data.pop("payment_loan_details")

    #     instance = super().update(instance, validated_data)

    #     for detail_data in payment_loan_details_data:
    #         PaymentLoanDetail.objects.update_or_create(payment=instance, defaults=detail_data)

    #     return instance
