""" Apps Config """

from django.apps import AppConfig

class LoansConfig(AppConfig):
    """ Register Loans App """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loans'
