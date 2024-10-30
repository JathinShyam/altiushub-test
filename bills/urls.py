
from django.urls import path, include
from .views import index

from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, InvoiceSundrySet, InvoiceItemViewSet


router = DefaultRouter()
router.register('invoice', InvoiceViewSet)
router.register('items', InvoiceItemViewSet)
router.register('sundry', InvoiceSundrySet)


urlpatterns = [
    path('index/', index),
    path('', include(router.urls)),
]
