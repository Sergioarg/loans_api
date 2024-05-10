""" Module Serilizers """
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """ Serializer of Customer model. """
    class Meta:
        model = Customer
        fields = (
            "score",
            "status",
            "external_id",
            "preapproved_at",
        )

        read_only_fields = ("outstanding", "")
