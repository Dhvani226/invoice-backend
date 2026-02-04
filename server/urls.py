from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from billing.views import login_view, dashboard_view, create_invoice_view, clients_view, products_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('create-invoice/', create_invoice_view, name='create-invoice'),
    path('manage-clients/', clients_view, name='clients'),
    path('manage-products/', products_view, name='products'),
    path('api/', include('billing.urls')),  # include router
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
