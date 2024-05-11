# pylint: disable=E1101
""" Module Serilizers """
from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from constans import LOANS_STATUS
from customers.models import Customer
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
                raise serializers.ValidationError({
                    "customer": "Customer not found."
                })

            credit_available = customer.score
            total_amount = Loan.objects.filter(
                customer=customer,
                status__in=(0, LOANS_STATUS['PENDING'])
            ).aggregate(total_amount=models.Sum('amount')
            ).get('total_amount', 0)

            if not total_amount:
                total_amount = 0

            if total_amount + amount > credit_available:
                raise serializers.ValidationError({
                    "amount": f"You cannot create a loan greater than {credit_available} your current debt is {total_amount}."
                })
        return amount

    def validate(self, attrs):
        """ Validations """

        if self.instance is None:
            loan = self.validate_new_loan(attrs)
        else:
            loan = self.validate_existing_loan(attrs)

        return loan

    def validate_new_loan(self, attrs):
        """Validate status of the new loan to create

        Args:
            attrs (dict): data received

        Raises:
            serializers.ValidationError: exception in case of status rejected or paid

        Returns:
            dict: data of the loan
        """
        status = attrs.get('status')
        if status == LOANS_STATUS['ACTIVE']:
            attrs['taken_at'] = datetime.now()
        elif status == LOANS_STATUS['REJECTED'] or status == LOANS_STATUS['PAID']:
            raise serializers.ValidationError({
                "status": f"You can't create a loan with the status {status}"
            })
        return attrs

    def validate_existing_loan(self, attrs):
        # TODO: Implement
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = instance.customer
        if customer:
            external_id = getattr(customer, 'external_id', None)
            if external_id is not None:
                representation['customer_external_id'] = external_id
        return representation
