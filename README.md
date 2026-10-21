# ELION HUB Marketplace — Django Backend Starter

This is the first backend foundation for the ELION HUB Marketplace. It is designed to be deployed separately from the current GitHub Pages storefront.

## Included
- Django admin for managing categories, vendors, products, orders, and order items
- Public JSON endpoints for active categories and approved/active products
- Vendor application endpoint (applications require admin review)
- Basic order-request endpoint for development/testing
- PostgreSQL configuration for Render and SQLite fallback for local development
- CORS configuration for the current GitHub Pages storefront

## Important limitations
This is a **starter foundation, not a production-ready marketplace**. Real customer/seller accounts, seller dashboards, inventory locking, delivery confirmation, refunds, payment processing, commission settlement, and seller payouts are not implemented yet. Do not collect real payments or use it for live orders until those are built and tested. Paystack is not integrated.

## Deploy on Render (phone-friendly)
1. Upload the files in this folder to a new GitHub repository, or upload them into a separate folder/repository from your existing `index.html`.
2. In Render, create a **Blueprint** from that repository and let it read `render.yaml`.
3. Wait for deployment. Open the service URL ending in `.onrender.com`.
4. Open `/admin/` and create an admin account only after the service is deployed. If the host provides a Shell, run `python manage.py createsuperuser`. Do not share the admin password or secret key in chat.
5. Test `/api/health/`, `/api/categories/`, and `/api/products/`.

## API endpoints
- `GET /api/health/` — health check
- `GET /api/categories/` — active categories
- `GET /api/products/` — active products; optional `?category=slug` and `?q=search`
- `POST /api/vendor-applications/` — submit a vendor application as JSON (`store_name`, `contact_name`, `email`, `phone`, optional `message`)
- `POST /api/order-requests/` — basic test order request as JSON. This is not a payment endpoint and should not be used for real orders until order validation/authentication is implemented.

## Connecting the existing storefront
Once Render gives you the backend URL, configure the storefront JavaScript to fetch product data from `https://YOUR-SERVICE.onrender.com/api/products/`. Keep the existing GitHub Pages URL for the storefront. The frontend integration is the next step after the backend is deployed.

## Local development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
