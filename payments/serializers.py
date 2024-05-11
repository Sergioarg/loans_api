# pylint: disable=E1101
""" Module Serilizers """
from rest_framework import serializers
from .models import Payment, PaymentLoanDetail
from utils import calculate_total_debt
from customers.models import Customer
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
    # payment_loan_detail = PaymentLoanDetailSerializer(many=True)
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
            # "payment_loan_detail"
        )

    def validate(self, attrs):
        # Check if is the firts creation
        if self.instance is None:
            payment = self.validate_payment_data(attrs)

        return payment

    def validate_payment_data(self, data):
        """Validate payment data received

        Args:
            data (dict): data of the payment

        Raises:
            serializers.ValidationError: in case customer dont have lons
            serializers.ValidationError: _description_

        Returns:
            dict: data of payment
        """
        customer = data.get('customer')
        total_debt = calculate_total_debt(customer)

        # Check if customer has loans
        if total_debt == 0:
            raise serializers.ValidationError({
                "details": "This customer has no loans"
            })

        # Check payment are greater than total_debt
        payment = data.get('total_amount')
        if payment > total_debt:
            raise serializers.ValidationError({
                "details": "total_amount is greater than total debts"
            })
        return data

    # def create(self, validated_data):

    #     payment_loan_detail_data = validated_data.pop("payment_loan_detail")
    #     payment = Payment.objects.create(**validated_data)

    #     for detail_data in payment_loan_detail_data:
    #         PaymentLoanDetail.objects.create(payment=payment, **detail_data)

    #     return payment

    # def update(self, instance, validated_data):
    #     payment_loan_detail_data = validated_data.pop("payment_loan_detail")

    #     instance = super().update(instance, validated_data)

    #     for detail_data in payment_loan_detail_data:
    #         PaymentLoanDetail.objects.update_or_create(payment=instance, defaults=detail_data)

    #     return instance
