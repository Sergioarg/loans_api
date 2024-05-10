# pylint: disable=E1101
""" Module Serilizers """
from rest_framework import serializers
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
