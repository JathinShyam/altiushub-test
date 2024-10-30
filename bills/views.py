from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    InvoiceBillSundry,
    InvoiceHeader,
    InvoiceItems,
)
from rest_framework import serializers
from .serializers import InvoiceItemsSerializer, InvoiceDetailSerializer, InvoiceHeaderSerializer, InvoiceBillSundrySerializer

# Create your views here.
def index(request):
    return HttpResponse("Hi")

class InvoiceViewSet(viewsets.ModelViewSet):
    """View for manage Invoice APIs."""
    serializer_class = InvoiceDetailSerializer
    queryset = InvoiceHeader.objects.all()


    def get_queryset(self):
        items = self.request.query_params.get('items')
        sundry = self.request.query_params.get('sundry')
        queryset = self.queryset
        if items:
            item_ids = self._params_to_ints(items)
            queryset = queryset.filter(items__id__in=item_ids)
        if sundry:
            sundry_ids = self._params_to_ints(sundry)
            queryset = queryset.filter(sundry__id__in=sundry_ids)

        return queryset.filter().order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return InvoiceHeaderSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new invoice"""
        serializer.save(user=self.request.user)


class InvoiceHeaderAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for Invoice attributes."""

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter().distinct()


class InvoiceSundrySet(InvoiceViewSet):
    """Manage Invoice in the database."""
    serializer_class = InvoiceBillSundrySerializer
    queryset = InvoiceBillSundry.objects.all()


class InvoiceItemViewSet(InvoiceViewSet):
    """Manage items in the database."""
    serializer_class = InvoiceItemsSerializer
    queryset = InvoiceItems.objects.all()