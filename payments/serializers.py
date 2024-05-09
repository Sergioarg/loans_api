""" Module Serilizers """
from rest_framework import serializers
from .models import Payment, PaymentLoanDetail


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        """ Class Meta"""
        model = Payment
        fields = (
            "id",
            "total_amount",
            "status",
            "paid_at",
            "customer_id"
        )

        read_only_fields = ("outstanding", )


class PaymentLoanDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        """ Class Meta"""
        model = PaymentLoanDetail
        fields = (
            "amount",
            "loan_id",
            "payment_id"
        )

        read_only_fields = ("outstanding", )
