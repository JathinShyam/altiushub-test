from django.contrib import admin
from .models import Invoice, InvoiceItem, InvoiceBillSundry

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceBillSundry)
