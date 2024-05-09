""" Urls used """
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from customers.views_sets import CustomerViewSet

# REST API
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

# Views
urlpatterns = [
    path('admin/', admin.site.urls),

    # API Routes
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
