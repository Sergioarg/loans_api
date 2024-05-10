""" Register models """
from django.contrib import admin
from .models import Loan

class LoansAdmin(admin.ModelAdmin):
    """ Configurations of model Customer in Admin panel """

    list_display = (
        'id', 'external_id',
        'amount', 'customer' ,'updated_at'
    )

    search_fields = ('external_id', 'status', 'score')

admin.site.register(Loan, LoansAdmin)
