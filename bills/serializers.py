from rest_framework import serializers

from .models import InvoiceBillSundry, InvoiceHeader, InvoiceItems


class InvoiceItemsSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceItems."""

    # Validation for amount, quantity and price
    def validate_quantity_and_price(self):
        if not (self.Quantity > 0 and self.Price > 0):
            raise serializers.ValidationError("Please make sure you entered positive numbers.")

    class Meta:
        model = InvoiceItems
        fields = ['InvoiceNumber', 'itemName', 'Quantity', 'Price', 'Amount']
        read_only_fields = ['InvoiceNumber']

class InvoiceBillSundrySerializer(serializers.ModelSerializer):
    """ Serializer for InvoiceBillSundry."""

    class Meta:
        model = InvoiceItems
        fields = ['InvoiceNumber', 'billSundryName','Amount']
        read_only_fields = ['InvoiceNumber']


class InvoiceHeaderSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceHeader."""
    items = InvoiceItemsSerializer(many=True, required=False)
    sundry = InvoiceBillSundrySerializer(many=True, required=False)

    class Meta:
        model = InvoiceHeader
        fields = ['InvoiceNumber', 'CustomerName', 'BillingAddress', 'ShippingAddress', 'GSTIN', 'TotalAmount', 'Date']
        read_only_fields = ['InvoiceNumber']

class InvoiceDetailSerializer(InvoiceHeaderSerializer):
    """Serializer for InvoiceHeader detail view."""

    def _get_or_create_sundry(self, sundry, InvoiceHeader):
        """Handle getting or creating InvoiceBillSundry as needed."""
        for each_sundry in sundry:
            sundry_obj, created = InvoiceBillSundry.objects.get_or_create(
                **each_sundry,
            )
            InvoiceHeader.InvoiceBillSundry.add(sundry_obj)

    def _get_or_create_items(self, items, recipe):
        """Handle getting or creating items as needed."""
        for item in items:
            item_obj, created = InvoiceItems.objects.get_or_create(
                **item,
            )
            
            InvoiceHeader.InvoiceItems.add(item_obj)

    def create(self, validated_data):
        """Create a Invoice Header."""
        items = validated_data.pop('items', [])
        sundry = validated_data.pop('sundry', [])
        invoice = InvoiceHeader.objects.create(**validated_data)
        self._get_or_create_items(items, invoice)
        self._get_or_create_sundry(sundry, invoice)

        return invoice

    def update(self, instance, validated_data):
        """Update Invoice."""
        items = validated_data.pop('items', None)
        sundry = validated_data.pop('sundry', None)
        if items is not None:
            instance.tags.clear()
            self._get_or_create_items(items, instance)
        if sundry is not None:
            instance.sundry.clear()
            self._get_or_create_ingredients(sundry, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

