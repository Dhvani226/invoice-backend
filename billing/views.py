from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from .models import Client, Product, Invoice
from .serializers import ClientSerializer, ProductSerializer, InvoiceSerializer

# -------------------------
# PDF Support
# -------------------------
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False


# -------------------------
# Template Views
# -------------------------
def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def create_invoice_view(request):
    return render(request, 'create-invoice.html')

def clients_view(request):
    return render(request, 'clients.html')

def products_view(request):
    return render(request, 'products.html')


# -------------------------
# API ViewSets
# -------------------------
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


# -------------------------
# Invoice PDF (JWT secured)
# -------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_pdf_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk, user=request.user)

    html = render_to_string("invoice_pdf.html", {
        "invoice": invoice
    })

    if not WEASYPRINT_AVAILABLE:
        return HttpResponse(html)

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_{invoice.invoice_number}.pdf"'
    return response
