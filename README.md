# ShopSphere

ShopSphere is a Django-based e-commerce web application for browsing products,
managing a user shopping cart, and placing orders. It includes a server-rendered
HTML interface, Django authentication, product and category management through
the admin site, address management, checkout, and order history.

## Features

- Browse an active product catalogue and view product details.
- Filter products by category, trending status, and offers.
- Register, log in, log out, and manage a user profile.
- Upload and display a profile image.
- Change a password while logged in or reset it through the forgot-password flow.
- Add products to a user-specific cart.
- Increase, decrease, and remove cart items with stock checks.
- Manage delivery addresses.
- Review a cart at checkout and place an order against a selected address.
- Reduce product inventory when an order is placed.
- View previous orders, line items, totals, and order status.
- Manage categories and products through Django admin.
- Store product, category, and profile images as uploaded media.
- Protect authenticated pages with Django's `login_required` decorator.

## Technology stack

| Area | Technology |
| --- | --- |
| Backend | Python and Django |
| Current development versions | Python 3.15.2 and Django 6.1.3 |
| Database | SQLite |
| Frontend | Django templates, HTML, and CSS |
| Authentication | Django's built-in `User` model and auth system |
| Images | Pillow and Django `ImageField` |
| Testing | Django `TestCase` and Django test runner |

The project was generated from Django 5.2-era project files and currently
passes the test suite with Django 6.1.3. Pin the versions in a dependency file
before deploying or sharing a reproducible environment.

## Application architecture

The project is split into focused Django apps:

| App | Responsibility |
| --- | --- |
| `base` | Home page, catalogue filtering, product detail, and about page |
| `authen` | Registration, login, logout, profiles, profile images, and passwords |
| `products` | Categories, products, stock, availability, offers, and trends |
| `cart` | User-specific cart items and quantity management |
| `orders` | Delivery addresses, checkout, orders, and order items |
| `myproject` | Project settings, root URLs, WSGI, and ASGI configuration |

### Request flow

```text
Browser
  -> myproject/urls.py
  -> app urls.py
  -> view
  -> model/database operation
  -> template
  -> HTML response
```

### Data model

```text
User
  |-- PictureModel
  |-- CartModel --> ProductModel --> CategoryModel
  |-- AddressModel
  `-- Orders --> OrderItem --> ProductModel
```

Products use soft-delete and availability flags. Cart records are scoped to a
user. Checkout runs in a database transaction, creates an order and its line
items, reduces stock, marks zero-stock products unavailable, and clears the
user's cart.

## Project structure

```text
myproject/
├── manage.py
├── db.sqlite3                 # Local development database
├── myproject/                 # Django project configuration
├── base/                      # Home and catalogue browsing
├── authen/                    # Authentication and profiles
├── products/                  # Product catalogue models and admin
├── cart/                      # Cart models and views
├── orders/                    # Addresses, checkout, and orders
├── templates/                 # Shared templates
├── static/css/                # Project stylesheets
├── media/                     # Product, category, and profile images
└── Readme.md
```

## Requirements

- Python 3.11 or newer
- Django 5.2 or newer
- Pillow

There is currently no `requirements.txt` or `pyproject.toml` in this project,
so install the dependencies explicitly in a virtual environment.

## Local setup

From the repository root, enter the Django project directory:

```powershell
cd Project\Major_Project\myproject
```

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, use:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install "Django>=5.2" Pillow
```

Apply database migrations:

```bash
python manage.py migrate
```

Create an administrator for the Django admin:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in a browser. Use
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to manage
categories and products.

## Common management commands

Run commands from `Project/Major_Project/myproject/`:

```bash
# Check the Django configuration
python manage.py check

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Run the automated tests
python manage.py test

# Open the Django shell
python manage.py shell

# Collect static files for deployment
python manage.py collectstatic
```

## Main routes

| URL | Name | Purpose | Authentication |
| --- | --- | --- | --- |
| `/` | `home` | Product catalogue and filters | Public |
| `/view_product/<id>` | `view_product` | Product details and related products | Public |
| `/about/` | `about` | About page | Required |
| `/authen/register/` | `register` | Create an account | Public |
| `/authen/login_/` | `login_` | Sign in | Public |
| `/authen/logout/` | `logout` | Sign out | Required |
| `/authen/profile/` | `profile` | View profile | Required |
| `/authen/pupdate/` | `pupdate` | Update profile details/image | Required |
| `/authen/reset_password/` | `reset_password` | Change password | Required |
| `/authen/forgot_password/` | `forgot_password` | Reset password flow | Public |
| `/cart/cart/` | `cart` | View current cart | Required |
| `/cart/add_to_cart/<id>` | `add_to_cart` | Add or increment a product | Required |
| `/cart/plus/<id>` | `plus` | Increase cart quantity | Required |
| `/cart/minus/<id>` | `minus` | Decrease cart quantity | Required |
| `/cart/remove/<id>` | `remove` | Remove a cart item | Required |
| `/orders/address/` | `address` | List delivery addresses | Required |
| `/orders/add_address/` | `add_address` | Add a delivery address | Required |
| `/orders/update_address/<id>` | `update_address` | Edit an owned address | Required |
| `/orders/remove_add/<id>` | `remove_add` | Delete an owned address | Required |
| `/orders/check_out/` | `check_out` | Review cart and place order | Required |
| `/orders/order_/` | `order_` | View order history | Required |
| `/admin/` | Django admin | Manage site data | Staff user |

The application currently uses server-rendered pages and does not expose a
REST or JSON API.

## Admin and initial data

1. Run `python manage.py createsuperuser`.
2. Visit `/admin/` and sign in.
3. Create one or more categories.
4. Create products and assign each product to a category.
5. Add product images, prices, descriptions, and quantities.
6. Optionally mark products as trending or on offer.

The repository includes sample media and a local SQLite database. For a clean
installation, use migrations and add catalogue data through the admin instead
of relying on the checked-in database contents.

## Testing

The project uses Django's built-in test runner. Run:

```bash
python manage.py test
```

The current tests cover:

- Anonymous users being redirected away from cart actions.
- Cart quantities and totals being scoped to the logged-in user.
- Checkout creating an order and line items, reducing stock, and clearing the cart.
- Users being unable to update another user's address.

The verified local result is **4 tests passed**.

## Configuration and media

Project configuration is in [`myproject/settings.py`](myproject/settings.py).
The current development configuration uses:

- SQLite at `db.sqlite3`
- Static files under `static/`
- Uploaded media under `media/`
- `MEDIA_URL = "/media/"`
- `STATIC_URL = "/static/"`
- UTC timezone

Uploaded images are stored in these locations:

| Upload type | Directory |
| --- | --- |
| Category images | `media/category/` |
| Product images | `media/products/` |
| Profile images | `media/uploads/` |

## Production checklist

The checked-in settings are intended for local development and must be
hardened before deployment:

- Move `SECRET_KEY` to an environment variable and rotate the development key.
- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS` for the deployment domain.
- Use a production database and configure its connection securely.
- Configure a durable object store or persistent media volume for uploads.
- Run `collectstatic` and serve static files through a web server or CDN.
- Configure HTTPS, secure cookies, CSRF trusted origins, and security headers.
- Do not commit credentials, private uploads, virtual environments, or generated
  cache files.
- Add a dependency lock/requirements file and pin versions used in deployment.
- Configure email delivery if password-reset email functionality is added.

The current forgot-password implementation changes a password through a
username/session form; it is not an email-token reset flow. Treat this as a
development feature until a secure, expiring, email-based reset process is
implemented.

## Known limitations and next improvements

- No payment provider or payment confirmation workflow is implemented.
- Product search, reviews, wishlists, coupons, and order cancellation are not
  currently available in the UI.
- The project has no formal dependency manifest or environment-specific settings.
- Some mutation endpoints use links/GET requests; production deployments should
  prefer POST forms with CSRF protection for state-changing actions.
- Add stronger validation, database constraints, and concurrency handling around
  stock reservation before accepting real orders.
- Add broader tests for registration, authentication, product filtering,
  profile updates, address CRUD, and invalid checkout cases.

## Contributing

1. Create a feature branch.
2. Make a focused change and add or update targeted tests.
3. Run `python manage.py check` and `python manage.py test`.
4. Review migrations and media changes before committing.
5. Open a pull request describing the behavior change, validation performed,
   and any required configuration.

Please keep secrets and local databases out of commits, and avoid committing
`__pycache__`, `.venv`, editor metadata, and generated files.
