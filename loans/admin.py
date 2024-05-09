from django.contrib import admin
from .models import Loan

class LoansAdmin(admin.ModelAdmin):
    """ Configurations of Admin panel """

    # list_display = (
    #     'id', 'external_id',
    #     'status', 'score', 'created_at',
    #     'updated_at', 'preapproved_at'
    # )

    search_fields = ('external_id', 'status', 'score')

# Register your models here.
admin.site.register(Loan, LoansAdmin)
