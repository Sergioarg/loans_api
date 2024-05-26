""" Module Serilizers """
from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from utils.states import LoanStatus
from customers.models import Customer
from .models import Loan
from utils.calculations import calculate_total_amount

class LoanSerializer(serializers.ModelSerializer):
    """ Serializer for the Loan model. """
    class Meta:
        """ Class Meta """
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

    def validate_amount(self, amount) -> int:
        """Validate amount requested could be requested

        Args:
            amount (Decimal): amount requested

        Raises:
            serializers.ValidationError: amount is greater than score

        Returns:
            Decimal: amount requested
        """
        loan = self.instance
        customer_id = self.initial_data.get('customer')

        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except ObjectDoesNotExist as exception:
                raise serializers.ValidationError(exception)

            total_amount = calculate_total_amount(customer)
            available_amount = customer.score - total_amount
            if total_amount + amount > customer.score:
                raise serializers.ValidationError(
                    f"You cannot create for this amount, credit available {available_amount}"
                )
        if loan and self.initial_data.get('amount'):
            raise serializers.ValidationError(
                "Cannot update amount after created"
            )

        return amount

    def validate_status(self, status) -> int:
        """Validate status of the new loan to create

        Args:
            attrs (dict): data received

        Raises:
            serializers.ValidationError: exception in case of status rejected or paid

        Returns:
            dict: data of the loan
        """
        # Check when is a new loan
        loan = self.instance
        if loan is None:
            if status == LoanStatus.REJECTED.value or status == LoanStatus.PAID.value:
                raise serializers.ValidationError(
                    f"You can't create a loan with the status {status}"
                )
        else:
            if status == LoanStatus.REJECTED.value and loan.status != LoanStatus.PENDING.value:
                raise serializers.ValidationError(
                    "Can update status to rejected only if the status is pending"
                )
            if status == LoanStatus.PAID.value and loan.outstanding > 0 :
                raise serializers.ValidationError(
                    f"Cannot update loan to paid with outstanding pending {loan.outstanding}"
                )

        return status

    def create(self, validated_data):
        if validated_data.get('status') == LoanStatus.ACTIVE.value:
            validated_data['taken_at'] = datetime.now()

        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer = instance.customer
        if customer:
            external_id = getattr(customer, 'external_id', None)
            if external_id is not None:
                representation['customer_external_id'] = external_id
        return representation
