# pylint: disable=E1101
""" Module Serilizers """
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Loan
from customers.models import Customer

class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Loan model.
    """
    class Meta:
        """ Class Meta"""
        model = Loan
        fields = (
            "external_id",
            "amount",
            "contract_version",
            "status",
            "outstanding",
            "customer",
        )
        extra_kwargs = {
            'customer': {'write_only': True},
            'contract_version': {'write_only': True}
        }
        read_only_fields = ("outstanding",)

    def validate_amount(self, amount):
        """Validate amount requested could be requested

        Args:
            amount (Decimal): amount requested

        Raises:
            serializers.ValidationError: amount is greater than score

        Returns:
            Decimal: amount requested
        """
        customer_id = self.initial_data.get('customer')
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except ObjectDoesNotExist as exc:
                _ = exc
                raise serializers.ValidationError("Customer not found.")

            credit_available = customer.score
            total_amount = Loan.objects.filter(
                customer=customer,
                status__in=(0, 1)
            ).aggregate(total_amount=models.Sum('amount')
            ).get('total_amount', 0)

            if not total_amount:
                total_amount = 0

            if total_amount + amount > credit_available:
                raise serializers.ValidationError({
                    "detail": f"You cannot create a loan greater than {credit_available} your current debt is {total_amount}."
                })
        return amount


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = instance.customer
        if customer:
            external_id = getattr(customer, 'external_id', None)
            if external_id is not None:
                representation['customer_external_id'] = external_id
        return representation
