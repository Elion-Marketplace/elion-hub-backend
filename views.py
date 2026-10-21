import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Category, Product, VendorApplication, OrderRequest

def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

@require_GET
def health(request):
    return JsonResponse({"ok": True, "service": "ELION HUB Marketplace API", "stage": "starter"})

@require_GET
def categories(request):
    data = list(Category.objects.filter(is_active=True).order_by("name").values("id", "name", "slug"))
    return JsonResponse({"results": data})

@require_GET
def products(request):
    qs = Product.objects.filter(is_active=True, stock_quantity__gt=0, category__is_active=True).select_related("category", "vendor")
    category = request.GET.get("category")
    query = request.GET.get("q", "").strip()
    if category:
        qs = qs.filter(category__slug=category)
    if query:
        qs = qs.filter(name__icontains=query)
    results = [{
        "id": p.id, "name": p.name, "slug": p.slug, "description": p.description,
        "price_ngn": p.price_ngn, "image_url": p.image_url, "stock_quantity": p.stock_quantity,
        "category": p.category.name, "category_slug": p.category.slug,
        "seller": p.vendor.store_name if p.vendor and p.vendor.approved else "ELION HUB"
    } for p in qs.order_by("-created_at")[:100]]
    return JsonResponse({"results": results, "count": len(results)})

@csrf_exempt
@require_POST
def vendor_application(request):
    data = _json_body(request)
    required = ("store_name", "contact_name", "email", "phone")
    if data is None:
        return JsonResponse({"error": "Send valid JSON."}, status=400)
    if any(not str(data.get(k, "")).strip() for k in required):
        return JsonResponse({"error": "store_name, contact_name, email and phone are required."}, status=400)
    try:
        validate_email(data["email"])
    except ValidationError:
        return JsonResponse({"error": "Enter a valid email address."}, status=400)
    app = VendorApplication.objects.create(
        store_name=str(data["store_name"]).strip()[:120],
        contact_name=str(data["contact_name"]).strip()[:120],
        email=str(data["email"]).strip(),
        phone=str(data["phone"]).strip()[:30],
        message=str(data.get("message", "")).strip()[:2000],
    )
    return JsonResponse({"message": "Application received for review.", "application_id": app.id}, status=201)

@csrf_exempt
@require_POST
def order_request(request):
    # Development-only request capture. It does not charge customers or reserve inventory.
    data = _json_body(request)
    required = ("customer_name", "customer_email", "customer_phone", "delivery_address", "items")
    if data is None:
        return JsonResponse({"error": "Send valid JSON."}, status=400)
    if any(not data.get(k) for k in required):
        return JsonResponse({"error": "Customer details, delivery address and items are required."}, status=400)
    if not isinstance(data["items"], list) or not data["items"]:
        return JsonResponse({"error": "items must be a non-empty list."}, status=400)
    try:
        validate_email(data["customer_email"])
    except ValidationError:
        return JsonResponse({"error": "Enter a valid email address."}, status=400)
    safe_items = []
    for item in data["items"][:50]:
        if not isinstance(item, dict):
            return JsonResponse({"error": "Each item must contain a product_id and quantity."}, status=400)
        try:
            pid, qty = int(item.get("product_id")), int(item.get("quantity", 1))
        except (TypeError, ValueError):
            return JsonResponse({"error": "Product IDs and quantities must be numbers."}, status=400)
        if qty < 1 or qty > 20 or not Product.objects.filter(id=pid, is_active=True, stock_quantity__gte=qty).exists():
            return JsonResponse({"error": "An item is unavailable or the quantity is invalid."}, status=400)
        safe_items.append({"product_id": pid, "quantity": qty})
    order = OrderRequest.objects.create(
        customer_name=str(data["customer_name"]).strip()[:120],
        customer_email=str(data["customer_email"]).strip(),
        customer_phone=str(data["customer_phone"]).strip()[:30],
        delivery_address=str(data["delivery_address"]).strip()[:2000],
        items_json=safe_items,
    )
    return JsonResponse({
        "message": "Test order request saved. No payment was taken.",
        "order_request_id": order.id,
        "status": order.status
    }, status=201)
