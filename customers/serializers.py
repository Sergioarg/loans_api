""" Module Serilizers """
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        """ Class Meta"""
        model = Customer
        fields = ('external_id', 'status', 'status', 'preapproved_at')
