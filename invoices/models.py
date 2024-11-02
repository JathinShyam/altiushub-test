from django.db import models
import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db.models import Sum, Max

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.PositiveIntegerField(unique=True, editable=False)
    customer_name = models.CharField(max_length=255)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    gstin = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_amount(self):
        items_total = self.invoice_items.aggregate(
            total=Sum('amount'))['total'] or Decimal('0')
        sundries_total = self.bill_sundries.aggregate(
            total=Sum('amount'))['total'] or Decimal('0')
        return items_total + sundries_total

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Get the maximum invoice number and add 1, or start from 1 if no invoices exist
            max_invoice_number = Invoice.objects.aggregate(Max('invoice_number'))['invoice_number__max']
            self.invoice_number = (max_invoice_number or 0) + 1
        
        # Calculate total amount
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate amount before saving
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        # Update invoice total
        self.invoice.save()

class InvoiceBillSundry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(Invoice, related_name='bill_sundries', on_delete=models.CASCADE)
    bill_sundry_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update invoice total
        self.invoice.save()
