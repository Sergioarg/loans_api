""" Register models """
from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    """ Configurations of model Customer in Admin panel """
    fields = ('external_id', 'status', 'score',)

    list_display = (
        'id', 'external_id',
        'status', 'score', 'created_at',
        'updated_at', 'preapproved_at'
    )

    search_fields = ('external_id', 'status', 'score')

admin.site.register(Customer, CustomerAdmin)
