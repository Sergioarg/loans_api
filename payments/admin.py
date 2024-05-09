from django.contrib import admin
from .models import Payment

class PaymentsAdmin(admin.ModelAdmin):
    """ Configurations of Admin panel """

    # list_display = (
    #     'id', 'external_id',
    #     'status', 'score', 'created_at',
    #     'updated_at', 'preapproved_at'
    # )

    search_fields = ('external_id', 'status', 'score')

# Register your models here.
admin.site.register(Payment, PaymentsAdmin)
