from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Vendor(models.Model):
    store_name = models.CharField(max_length=120)
    contact_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.store_name

class VendorApplication(models.Model):
    store_name = models.CharField(max_length=120)
    contact_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[("pending","Pending"),("approved","Approved"),("rejected","Rejected")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.store_name} ({self.status})"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price_ngn = models.PositiveIntegerField(help_text="Price in whole Nigerian naira")
    image_url = models.URLField(blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class OrderRequest(models.Model):
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)
    delivery_address = models.TextField()
    items_json = models.JSONField(default=list)
    status = models.CharField(max_length=20, default="requested")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order request #{self.pk} - {self.customer_name}"
