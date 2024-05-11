# pylint: disable=E0401, E0611
""" Urls used """
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from loans.views import LoansViewSet
from payments.views import PaymentViewSet
from customers.views import CustomerViewSet

# REST API
router = DefaultRouter()
router.register(r'api/customers', CustomerViewSet)
router.register(r'api/loans', LoansViewSet)
router.register(r'api/payments', PaymentViewSet)

# Views
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
]
