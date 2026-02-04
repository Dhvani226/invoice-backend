from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Product, Invoice, InvoiceItem


# =======================
# USER
# =======================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# =======================
# CLIENT
# =======================
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'address']


# =======================
# PRODUCT
# =======================
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'tax_percent']


# =======================
# INVOICE ITEM
# =======================
class InvoiceItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']   # only what frontend sends



# =======================
# INVOICE
# =======================
class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'client',
            'invoice_number',
            'date',
            'due_date',
            'subtotal',
            'tax',
            'discount',
            'total',
            'status',
            'items'
        ]
        read_only_fields = ['date', 'subtotal', 'tax', 'total']

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        items_data = validated_data.pop("items")

        invoice = Invoice.objects.create(
            user=user,
            discount=validated_data.get("discount", 0),
            **validated_data
        )

        subtotal = 0
        total_tax = 0

        for item in items_data:
            product = item["product"]
            qty = item["quantity"]

            price = product.price
            tax_percent = product.tax_percent

            line_total = price * qty
            tax_amount = (line_total * tax_percent) / 100

            subtotal += line_total
            total_tax += tax_amount

            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qty,
                price=price,
                discount=0,
                total=line_total
            )

        invoice.subtotal = subtotal
        invoice.tax = total_tax
        invoice.total = subtotal + total_tax - invoice.discount
        invoice.save()

        return invoice
