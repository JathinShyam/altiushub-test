from django.db import models

class InvoiceHeader(models.Model):
    InvoiceNumber = models.AutoField(primary_key=True) 
    CustomerName = models.CharField(max_length=30)
    BillingAddress = models.TextField()
    ShippingAddress = models.TextField()
    GSTIN = models.CharField(max_length=30)
    InvoiceItems = models.ManyToManyField('InvoiceItems')
    InvoiceBillSundry = models.ManyToManyField('InvoiceBillSundry')
    TotalAmount = models.DecimalField(decimal_places=2, max_digits=6)
    Date = models.DateField()

class InvoiceItems(models.Model):
    InvoiceNumber = models.ForeignKey(InvoiceHeader, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=30)
    Quantity = models.DecimalField(decimal_places=2, max_digits=6)
    Price = models.DecimalField(decimal_places=2, max_digits=6)
    Amount = models.DecimalField(decimal_places=2, max_digits=6)

class InvoiceBillSundry(models.Model):
    InvoiceNumber = models.ForeignKey(InvoiceHeader, on_delete=models.CASCADE)
    billSundryName = models.CharField(max_length=30)
    Amount = models.DecimalField(decimal_places=2, max_digits=6)
