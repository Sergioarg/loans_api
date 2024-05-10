""" Register apps and model Payment in admin """
from django.contrib import admin
from .models import Payment, PaymentLoanDetail

class PaymentsAdmin(admin.ModelAdmin):
    """ Configurations of Admin panel """

    list_display = (
        'id', 'total_amount', 'status',
    )

    search_fields = ('external_id', 'status', 'payment_at')

# Register your models here.
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(PaymentLoanDetail)
