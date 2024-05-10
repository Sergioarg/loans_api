# pylint: disable=E1101
""" Module Serilizers """
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = instance.customer
        if customer:
            external_id = getattr(customer, 'external_id', None)
            if external_id is not None:
                representation['customer_external_id'] = external_id
        return representation
