# pylint: disable=E1101
""" Module Serilizers """
from django.db import models
from rest_framework import serializers
from .models import Loan



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

    # pylint: disable=W0237
    def validate(self, data):
        """ Validate crucial data """
        customer = data.get('customer')
        if customer:
            credit_available = customer.score
            total_amount = Loan.objects.filter(
                customer=customer,
                status__in=(0, 1)
            ).aggregate(total_amount=models.Sum('amount')).get('total_amount', 0)

            if not total_amount:
                total_amount = 0

            if total_amount + data.get('amount') > credit_available:
                raise serializers.ValidationError({
                    "detail": f"You cannot create a loan greater than {credit_available} your current debt is {total_amount}."
                })
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = instance.customer
        if customer:
            external_id = getattr(customer, 'external_id', None)
            if external_id is not None:
                representation['customer_external_id'] = external_id
        return representation
