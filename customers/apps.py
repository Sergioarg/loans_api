""" Apps Config """
from django.apps import AppConfig

class CustomersConfig(AppConfig):
    """ Config customer app """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
