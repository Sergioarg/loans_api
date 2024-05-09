""" Urls used """
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# pylint: disable=E0401, E0611
from loans.views import LoansViewSet
from payments.views import PaymentViewSet
from customers.views import CustomerViewSet


# REST API
router = DefaultRouter()
router.register(r'loans', LoansViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'customers', CustomerViewSet)

# Views
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
