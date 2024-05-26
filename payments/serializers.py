""" Module Serilizers """
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from utils.states import LoanStatus, PaymentStatus
from customers.models import Customer
from loans.models import Loan
from utils.calculations import calculate_total_debt
from .models import Payment, PaymentLoanDetail

class PaymentLoanDetailSerializer(serializers.ModelSerializer):
    """ Serializer for the Customer model. """
    class Meta:
        """ Class Meta """
        model = PaymentLoanDetail
        fields = ("amount", "loan")

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payments and PaymentLoanDetail model.
    """
    payment_loan_details = PaymentLoanDetailSerializer(many=True, read_only=True)
    class Meta:
        """ Class Meta """
        model = Payment
        fields = (
            "total_amount",
            "status",
            "paid_at",
            "external_id",
            "customer",
            "payment_loan_details"
        )
        extra_kwargs = {
            'customer': {'write_only': True}
        }

    def validate(self, attrs):
        # Validating payment_loan_details manually

        attrs = super().validate(attrs)
        init_loan_details = self.initial_data.get('payment_loan_details')
        payment_loan_details = self.validate_payment_loan_details(init_loan_details)
        attrs['payment_loan_details'] = payment_loan_details

        return attrs

    def validate_total_amount(self, total_amount):
        """Validate payment data received

        Args:
            data (dict): data of the payment

        Raises:
            serializers.ValidationError: in case customer dont have lons
            serializers.ValidationError: _description_

        Returns:
            dict: data of payment
        """
        payment = self.instance
        customer_id = self.initial_data.get('customer')

        try:
            customer = Customer.objects.get(pk=customer_id)
        except ObjectDoesNotExist as exception:
            raise serializers.ValidationError(exception)

        total_debt = calculate_total_debt(customer)

        if total_debt == 0:
            raise serializers.ValidationError(
                "The customer does not have loans"
            )

        if total_amount > total_debt:
            raise serializers.ValidationError(
                f"total_amount is greater than total debts is {total_debt}"
            )

        if payment:
            if self.initial_data.get('total_amount'):
                raise serializers.ValidationError(
                    "Cannot update total_amount after created"
                )
            if self.initial_data.get('payment_loan_details'):
                raise serializers.ValidationError(
                    "Cannot update payment_loan_details after created"
                )
        return total_amount


    def validate_status(self, status):
        """Validate status

        Args:
            status (int): status recieved

        Raises:
            serializers.ValidationError: Try to change status rejected to accepted

        Returns:
            int: status correct
        """
        payment = self.instance
        if payment:
            if payment.status == PaymentStatus.REJECTED.value and status == PaymentStatus.COMPLETED.value:
                raise serializers.ValidationError(
                    "Cannot change rejected status to accepted status"
                )
        return status


    def validate_payment_loan_details(self, payment_loan_details_data):
        """Validate payment loan details receivedd

        Args:
            payment_loan_details_data (list): list of dicts with info of payments

        Raises:
            serializers.ValidationError: Cummon edge cases at moment to create payment

        Returns:
            list: list of dicts loans details with correct data
        """
        customer_id = self.initial_data.get('customer')
        customer = Customer.objects.get(pk=customer_id)
        total_amount = self.initial_data.get('total_amount')

        if not payment_loan_details_data:
            raise serializers.ValidationError({
                "payment_loan_details": "This field is required"
            })

        if not isinstance(payment_loan_details_data, list):
            raise serializers.ValidationError({
                "payment_loan_details": "This field should be a list of dicts"
            })

        details_amouts = 0
        for detail_data in payment_loan_details_data:
            try:
                loan = Loan.objects.get(pk=detail_data.get('loan'))
            except ObjectDoesNotExist as exception:
                raise serializers.ValidationError({
                    "loan": exception
                })

            detail_data_amount = detail_data.get('amount')
            # Validate customer loans
            if customer != loan.customer:
                raise serializers.ValidationError({
                    "loan": f"Loan {loan.id} does not belong to customer {customer_id}"
                })

            # Check if outstanding
            if detail_data_amount > loan.outstanding:
                raise serializers.ValidationError({
                    "amount": f"Loan {loan.id} Amount {round(detail_data_amount, 2)} paid is greater than outstanding {loan.outstanding}"
                })
            details_amouts += detail_data_amount
            detail_data['loan'] = loan

        if total_amount != details_amouts:
            raise serializers.ValidationError({
                "amount": f"All amounts {round(details_amouts, 2)} should be equal to {total_amount}"
            })

        return payment_loan_details_data

    def create(self, validated_data):
        payment_loan_details_data = validated_data.pop("payment_loan_details")
        payment = Payment.objects.create(**validated_data)
        for detail_data in payment_loan_details_data:
            loan = detail_data.get('loan')

            if payment.status == PaymentStatus.COMPLETED.value:
                loan.outstanding = round(loan.outstanding - detail_data.get('amount'), 2)

            if loan.outstanding == 0:
                loan.status = LoanStatus.PAID.value

            loan.save()
            PaymentLoanDetail.objects.create(payment=payment, **detail_data)

        return payment

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        payment = instance

        if payment:
            rep['customer_external_id'] = payment.customer.external_id
            loan_detail = PaymentLoanDetail.objects.filter(payment=payment)
            if loan_detail.exists():
                rep['loan_external_id'] = loan_detail[0].loan.external_id
                rep['payment_amount'] = loan_detail[0].amount

        return rep
