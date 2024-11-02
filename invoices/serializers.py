from rest_framework import serializers
from .models import Invoice, InvoiceItem, InvoiceBillSundry

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'item_name', 'quantity', 'price', 'amount']
        read_only_fields = ['amount']

    def validate(self, data):
        # Validate quantity and price are greater than zero
        if data['quantity'] <= 0 or data['price'] <= 0:
            raise serializers.ValidationError(
                "Quantity and price must be greater than zero"
            )
        return data

class InvoiceBillSundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceBillSundry
        fields = ['id', 'bill_sundry_name', 'amount']

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)
    bill_sundries = InvoiceBillSundrySerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'date', 'invoice_number', 'customer_name',
            'billing_address', 'shipping_address', 'gstin',
            'total_amount', 'invoice_items', 'bill_sundries'
        ]
        read_only_fields = ['invoice_number', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('invoice_items')
        sundries_data = validated_data.pop('bill_sundries')

        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        for sundry_data in sundries_data:
            InvoiceBillSundry.objects.create(invoice=invoice, **sundry_data)

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('invoice_items', [])
        sundries_data = validated_data.pop('bill_sundries', [])

        # Update invoice fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Clear existing items and sundries
        instance.invoice_items.all().delete()
        instance.bill_sundries.all().delete()

        # Create new items and sundries
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=instance, **item_data)

        for sundry_data in sundries_data:
            InvoiceBillSundry.objects.create(invoice=instance, **sundry_data)

        instance.save()
        return instance
