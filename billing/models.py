from django.db import models
from django.contrib.auth.models import User

# Customer
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


# Product or Service
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    tax_percent = models.FloatField(default=0)

    def __str__(self):
        return self.name


# Invoice
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)

    # 🔥 ADD THIS (matches DB)
    discount = models.FloatField(default=0)

    total = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")

    def __str__(self):
        return self.invoice_number


# Invoice Row
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    discount = models.FloatField(default=0)

    # 🔴 FIX
    total = models.FloatField(default=0)

