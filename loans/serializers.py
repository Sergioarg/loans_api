""" Module Serilizers """
from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        """ Class Meta"""
        model = Loan
        fields = (
            "id",
            "amount",
            "status",
            "customer_id"
            "external_id",
            "outstanding",
            "contract_version",
        )

        read_only_fields = ("outstanding", )
