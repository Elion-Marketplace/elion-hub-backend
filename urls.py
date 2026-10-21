from django.contrib import admin
from django.urls import path
from marketplace import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", views.health, name="api-health"),
    path("api/categories/", views.categories, name="api-categories"),
    path("api/products/", views.products, name="api-products"),
    path("api/vendor-applications/", views.vendor_application, name="vendor-application"),
    path("api/order-requests/", views.order_request, name="order-request"),
]
