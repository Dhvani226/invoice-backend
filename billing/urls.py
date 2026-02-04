from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    login_view, dashboard_view, create_invoice_view,
    clients_view, products_view, invoice_pdf_view,
    ClientViewSet, ProductViewSet, InvoiceViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'invoices', InvoiceViewSet, basename='invoices')

urlpatterns = [
    # Frontend pages
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('create-invoice/', create_invoice_view, name='create-invoice'),
    path('manage-clients/', clients_view, name='clients'),
    path('manage-products/', products_view, name='products'),

    # PDF
    path('invoice/<int:pk>/pdf/', invoice_pdf_view, name='invoice-pdf'),

    # API
    path('', include(router.urls)),
]
