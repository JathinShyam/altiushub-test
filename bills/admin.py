from django.contrib import admin

from .models import InvoiceBillSundry, InvoiceHeader, InvoiceItems

admin.site.register(InvoiceItems)
admin.site.register(InvoiceHeader)
admin.site.register(InvoiceBillSundry)