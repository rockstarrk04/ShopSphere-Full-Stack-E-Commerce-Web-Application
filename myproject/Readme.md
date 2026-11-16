# ShopSphere project overview

This is a Django-based e-commerce website called **ShopSphere**. It supports:

- User registration and login
- User profiles and profile images
- Product categories and products
- Product filtering by category, trending status, and offers
- Shopping cart management
- Address management
- Checkout preview
- Django admin
- SQLite database
- Static CSS and uploaded media files

The project is located in:

- `myproject/`
- Django configuration: `myproject/settings.py`
- Database: `db.sqlite3`

---

# 1. Overall architecture

The project follows Django’s standard structure:

```text
myproject/
│
├── manage.py
├── db.sqlite3
├── myproject/       Project configuration
├── base/            Home page and product browsing
├── authen/          Authentication and profiles
├── products/        Product and category models
├── cart/            Shopping cart
├── orders/          Addresses, orders, checkout
├── templates/       Shared templates
├── static/          CSS files
└── media/           Uploaded/product/category images
```

Django separates functionality into **apps**:

| App | Responsibility |
|---|---|
| `base` | Home page, product listing, product details |
| `authen` | Login, registration, logout, profiles, passwords |
| `products` | Categories and products |
| `cart` | Add/remove/update cart items |
| `orders` | Addresses, checkout, order-related models |
| `myproject` | Global Django configuration |

The request flow is generally:

```text
Browser
   ↓
Global URL configuration
   ↓
App URL configuration
   ↓
View function
   ↓
Model/database operations
   ↓
Template
   ↓
HTML response
```

---

# 2. `manage.py`

File:

- `manage.py`

This is Django’s command-line entry point.

It sets:

```python
DJANGO_SETTINGS_MODULE = "myproject.settings"
```

Then it passes commands to Django.

Typical commands include:

```powershell
py manage.py runserver
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py shell
py manage.py test
```

`manage.py` itself does not contain application logic.

---

# 3. `myproject` configuration package

Folder:

- `myproject/`

## 3.1 `settings.py`

File:

- `settings.py`

This controls the entire Django project.

### Installed applications

The project enables Django’s built-in apps:

```python
django.contrib.admin
django.contrib.auth
django.contrib.contenttypes
django.contrib.sessions
django.contrib.messages
django.contrib.staticfiles
```

It also enables local apps:

```python
base
authen
products
cart
orders
```

### Middleware

Middleware runs around every request.

The project uses:

- Security middleware
- Session middleware
- Common HTTP middleware
- CSRF protection
- Authentication middleware
- Message middleware
- Clickjacking protection

Important examples:

- `AuthenticationMiddleware` makes `request.user` available.
- `SessionMiddleware` enables login sessions.
- `CsrfViewMiddleware` protects POST forms.
- `MessageMiddleware` supports messages such as “Login Successful”.

### Templates

The global template directory is:

```python
BASE_DIR / "templates"
```

This contains shared templates such as:

- `main.html`
- `nav.html`

Each app also has its own template directory.

### Database

The project uses SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

The database stores:

- Users
- Products
- Categories
- Cart items
- Addresses
- Orders
- Django sessions and admin data

### Static files

Static CSS files are served from:

```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

Examples:

- `nav.css`
- `cart.css`
- `login.css`

### Media files

Uploaded images are stored in:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Examples:

- Product images
- Category images
- User profile images

During development, `urls.py` serves media files directly.

---

## 3.2 Global `urls.py`

File:

- `myproject/urls.py`

This is the top-level URL router.

```python
path("admin/", admin.site.urls)
path("", include("base.urls"))
path("authen/", include("authen.urls"))
path("cart/", include("cart.urls"))
path("orders/", include("orders.urls"))
```

This means:

| URL prefix | App |
|---|---|
| `/` | `base` |
| `/authen/` | `authen` |
| `/cart/` | `cart` |
| `/orders/` | `orders` |
| `/admin/` | Django admin |

For example:

```text
/authen/login_/
```

is first matched by the global `authen/` prefix, then by the `authen` app’s `login_/` route.

---

## 3.3 `asgi.py` and `wsgi.py`

Files:

- `asgi.py`
- `wsgi.py`

These expose the Django application to deployment servers.

- WSGI is commonly used with traditional synchronous servers.
- ASGI supports asynchronous servers and WebSockets.

They are deployment entry points, not feature modules.

---

# 4. `products` app

Folder:

- `products/`

This app defines the product catalogue.

## 4.1 Models

File:

- `products/models.py`

### `CategoryModel`

Represents a product category.

Fields:

| Field | Purpose |
|---|---|
| `cname` | Category name |
| `image` | Category image |
| `is_delete` | Soft-delete flag |
| `createdat` | Creation timestamp |

Example categories might be:

- Electronics
- Fashion
- Mobiles
- Cosmetics
- Fresh products

### `ProductModel`

Represents a product.

Fields:

| Field | Purpose |
|---|---|
| `category` | Foreign key to category |
| `pname` | Product name |
| `price` | Product price |
| `pdesc` | Short description |
| `quantity` | Available quantity |
| `pimage` | Product image |
| `created_at` | Creation timestamp |
| `is_delete` | Soft-delete flag |
| `is_available` | Whether product is available |
| `trending` | Whether product appears in trending results |
| `offer` | Whether product appears in offers |

The relationship is:

```text
CategoryModel 1 ─── many ProductModel
```

A category can have many products, but every product belongs to one category.

## 4.2 Admin

File:

- `products/admin.py`

Both categories and products are registered in Django admin.

The admin provides:

- Product listing
- Product search
- Category search
- Product availability management
- Soft deletion
- Product image management

## 4.3 Views

File:

- `products/views.py`

Currently this file only contains the default import and does not provide product views. Product browsing is implemented in the `base` app instead.

---

# 5. `base` app

Folder:

- `base/`

This app handles the public-facing catalogue pages.

## 5.1 URLs

File:

- `base/urls.py`

Routes:

| URL | View | Purpose |
|---|---|---|
| `/` | `home` | Product listing |
| `/about/` | `about` | About page |
| `/view_product/<id>` | `view_product` | Product details |

## 5.2 Home view

Function:

- `home`

The home page:

1. Checks whether the user is logged in.
2. Loads the user’s profile image if logged in.
3. Reads GET parameters.
4. Filters products.
5. Collects category names.
6. Renders `home.html`.

### Category filtering

A URL such as:

```text
/?category=Electronics
```

filters products by category.

### Trending products

A URL containing:

```text
/?trend=
```

loads products where:

```python
trending=True
```

### Offers

A URL containing:

```text
/?offer=
```

loads products where:

```python
offer=True
```

### Default listing

Without filters, it displays all products satisfying:

```python
is_delete=False
is_available=True
```

The products are randomized using:

```python
.order_by("?")
```

## 5.3 About view

Function:

- `about`

This page requires login through:

```python
@login_required(login_url="login_")
```

It renders:

- `about.html`

## 5.4 Product details view

Function:

- `view_product`

It:

1. Finds an available, non-deleted product.
2. Displays its information.
3. Finds up to three related products from the same category.
4. Renders `view_product.html`.

The `get_object_or_404()` helper returns a 404 response if the product does not exist.

## 5.5 Templates

### `home.html`

File:

- `home.html`

Displays:

- Category filter buttons
- Product name
- Price
- Description
- Quantity
- Product image
- Add-to-cart link
- Product details link

### `view_product.html`

File:

- `view_product.html`

Displays:

- Main product information
- Related products
- Back link

Some “Add to Cart” buttons in this template are currently visual buttons only and are not connected to the cart URL.

---

# 6. `authen` app

Folder:

- `authen/`

This handles authentication and user account management.

## 6.1 Models

File:

- `authen/models.py`

### `PictureModel`

Stores a profile image for a Django user.

Fields:

| Field | Purpose |
|---|---|
| `image` | Uploaded profile image |
| `user` | Foreign key to Django’s built-in `User` |

Relationship:

```text
User 1 ─── many PictureModel
```

The application normally creates one profile image record per user.

## 6.2 Registration form

File:

- `authen/forms.py`

`RegisterForm` collects:

- First name
- Last name
- Email
- Username
- Password
- Confirm password

The `clean()` method verifies that the two passwords match.

The `save()` method uses:

```python
User.objects.create_user(...)
```

This is important because Django hashes the password instead of storing it as plain text.

## 6.3 URLs

File:

- `authen/urls.py`

| URL | Purpose |
|---|---|
| `/authen/login_/` | Login |
| `/authen/logout/` | Logout |
| `/authen/register/` | Registration |
| `/authen/profile/` | View profile |
| `/authen/pupdate/` | Update profile |
| `/authen/reset_password/` | Change password while logged in |
| `/authen/forgot_password/` | Reset password using username |

## 6.4 Login

Function:

- `login_`

Process:

```text
User submits username/password
        ↓
authenticate()
        ↓
If valid:
    login()
    create success message
    redirect to home
        ↓
If invalid:
    create error message
    redirect back to login
```

The login session is maintained by Django’s session middleware.

## 6.5 Logout

Function:

- `logout_`

This:

1. Logs out the current user.
2. Clears the authentication session.
3. Displays a success message.
4. Redirects to login.

It requires authentication.

## 6.6 Registration

Function:

- `register`

Process:

```text
GET request → display form
POST request → validate form
                ↓
             create User
                ↓
        create PictureModel
                ↓
          redirect to login
```

A default profile image is created for the user.

## 6.7 Profile page

Function:

- `profile`

It displays:

- Profile image
- Full name
- Username
- Email
- Profile update link
- Password reset link
- Logout link

Template:

- `profile.html`

## 6.8 Profile image helper

Function:

- `profile_img`

This retrieves the profile image belonging to the current user.

Other apps use this helper to display the profile image in the navigation bar.

## 6.9 Profile update

Function:

- `update`

It updates:

- First name
- Last name
- Email
- Profile image

The template uses:

```html
enctype="multipart/form-data"
```

This is required for file uploads.

## 6.10 Password change

Function:

- `reset_password`

Uses Django’s built-in `PasswordChangeForm`.

After changing the password, this line keeps the user logged in:

```python
update_session_auth_hash(request, user)
```

## 6.11 Forgot-password flow

Function:

- `forgot_password`

The current flow is:

```text
Enter username
      ↓
Username stored in session
      ↓
Enter new password
      ↓
Passwords compared
      ↓
Password changed
```

This is a simple username-based reset mechanism. It does not currently use email verification or a secure password-reset token.

---

# 7. `cart` app

Folder:

- `cart/`

This implements the shopping basket.

## 7.1 Model

File:

- `cart/models.py`

### `CartModel`

Fields:

| Field | Purpose |
|---|---|
| `user` | Owner of the cart item |
| `product_c` | Product in the cart |
| `product_count` | Quantity selected |
| `total_price` | Price for that cart line |
| `created_at` | Creation timestamp |

Relationship:

```text
User 1 ─── many CartModel
Product 1 ─── many CartModel
```

## 7.2 URLs

File:

- `cart/urls.py`

| URL | Purpose |
|---|---|
| `/cart/add_to_cart/<id>` | Add product |
| `/cart/cart/` | Show cart |
| `/cart/remove/<id>` | Remove item |
| `/cart/plus/<id>` | Increase quantity |
| `/cart/minus/<id>` | Decrease quantity |

All cart operations require login.

## 7.3 Add to cart

Function:

- `add_to_cart`

Behavior:

- If the user does not already have the product:
  - Creates a new cart row.
- If the item already exists:
  - Increases quantity.
  - Increases total price.

## 7.4 View cart

Function:

- `cart`

It:

1. Retrieves the current user’s cart rows.
2. Adds all cart item totals.
3. Sends the grand total to the template.

Template:

- `cart.html`

## 7.5 Increase and decrease quantity

Functions:

- `plus`
- `minus`

Increasing quantity:

```text
quantity += 1
total_price += product.price
```

Decreasing quantity:

```text
if quantity > 1:
    quantity -= 1
    total_price -= product.price
else:
    delete cart row
```

## 7.6 Security detail

The cart item lookup includes:

```python
user=request.user
```

That prevents one logged-in user from modifying another user’s cart item by changing the ID in the URL.

---

# 8. `orders` app

Folder:

- `orders/`

This app currently handles addresses and checkout preparation. It also contains order models, but the complete order-placement process is not implemented.

## 8.1 Models

File:

- `orders/models.py`

### `AddressModel`

Stores delivery addresses.

Fields:

| Field | Purpose |
|---|---|
| `user` | Address owner |
| `fullname` | Recipient name |
| `mobile` | Contact number |
| `address_line` | Street/address information |
| `city` | City |
| `state` | State |
| `pincode` | Postal code |
| `is_default` | Default address flag |
| `created_at` | Creation timestamp |

### `Orders`

Represents an order.

Fields:

| Field | Purpose |
|---|---|
| `user` | Customer |
| `address` | Delivery address |
| `total_amount` | Order total |
| `status` | Order status |
| `created_at` | Creation time |

Available statuses:

```text
pending
confirmed
shipped
delivered
canclled
```

There is a spelling mistake in `canclled`; it should normally be `cancelled`.

### `OrderItem`

Represents an individual product inside an order.

Fields:

| Field | Purpose |
|---|---|
| `order` | Parent order |
| `product` | Purchased product |
| `price` | Price at purchase |
| `quantity` | Purchased quantity |

The `related_name="items"` allows:

```python
order.items.all()
```

## 8.2 Forms

File:

- `orders/forms.py`

`AddressForm` is a `ModelForm` for `AddressModel`.

It includes all address fields except:

```python
user
```

The user is assigned inside the view from `request.user`.

## 8.3 URLs

File:

- `orders/urls.py`

| URL | Purpose |
|---|---|
| `/orders/check_out/` | Checkout preview |
| `/orders/order_/` | Order page |
| `/orders/add_address/` | Add address |
| `/orders/address/` | List addresses |
| `/orders/update_address/<id>` | Edit address |
| `/orders/remove_add/<id>` | Delete address |

## 8.4 Add address

Function:

- `add_address`

Process:

```text
Display blank address form
        ↓
Validate submitted form
        ↓
Attach current user
        ↓
Save address
        ↓
Redirect to checkout
```

## 8.5 List addresses

Function:

- `address`

Loads all addresses belonging to the current user.

Template:

- `address.html`

## 8.6 Update and delete addresses

Functions:

- `update_address`
- `remove_add`

These allow address editing and deletion.

The current implementation looks up addresses only by ID, rather than by both ID and current user. This means authorization protection should be added before treating these routes as production-ready.

## 8.7 Checkout

Function:

- `check_out`

It loads:

- Current user’s addresses
- Current user’s cart items
- Grand total

Template:

- `check_out.html`

The checkout page currently displays a “Place Order” button, but the view does not yet create an `Orders` record or `OrderItem` records.

## 8.8 Order page

Function:

- `order_`

It simply renders:

- `order_.html`

There is currently no implemented order-history query in this view.

---

# 9. Shared templates

Folder:

- `templates/`

## 9.1 `main.html`

File:

- `main.html`

This is the base template.

It:

1. Loads static files.
2. Includes the navigation bar.
3. Provides a `head` block.
4. Provides a `content` block.

Other templates use:

```django
{% extends 'main.html' %}
```

This avoids duplicating the HTML structure.

## 9.2 `nav.html`

File:

- `nav.html`

This displays:

- ShopSphere logo
- Trending button
- Offers button
- Home
- Cart
- Orders
- Profile
- Login/register links
- Logout
- About

The navigation changes based on:

```django
{% if request.user.is_authenticated %}
```

---

# 10. Static CSS

Folder:

- `static/css/`

Important stylesheets:

| CSS file | Used for |
|---|---|
| `nav.css` | Navigation |
| `style.css` | Product/home layout |
| `login.css` | Login page |
| `register.css` | Registration |
| `profile.css` | Profile |
| `profile-update.css` | Profile editing |
| `cart.css` | Shopping cart |
| `address.css` | Address pages |
| `checkout.css` | Checkout |

Templates load CSS using:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/cart.css' %}">
```

---

# 11. Media files

Folder:

- `media/`

Subfolders:

```text
media/
├── category/
├── products/
└── uploads/
```

Purpose:

- `category/`: category images
- `products/`: product images
- `uploads/`: user-uploaded profile images or other uploaded files

Images are stored on disk, while database fields store the file paths.

---

# 12. Database relationships

The main data model is:

```text
User
 ├── PictureModel
 ├── CartModel ─── ProductModel ─── CategoryModel
 ├── AddressModel
 └── Orders
       └── OrderItem ─── ProductModel
```

More explicitly:

```text
CategoryModel
    └── ProductModel

User
    ├── PictureModel
    ├── CartModel
    ├── AddressModel
    └── Orders
            └── OrderItem
```

---

# 13. Complete user journey

## New visitor

```text
Home page
   ↓
Browse products
   ↓
View product
   ↓
Try Add to Cart
   ↓
Redirected to login because cart requires authentication
```

## New user

```text
Register
   ↓
Django User created
   ↓
PictureModel created
   ↓
Login
   ↓
Browse products
```

## Shopping flow

```text
Login
   ↓
Add product to cart
   ↓
Increase/decrease quantity
   ↓
Remove products if needed
   ↓
View total
   ↓
Checkout
   ↓
Choose or add address
```

## Account flow

```text
Login
   ↓
Profile
   ├── Update profile
   ├── Change password
   └── Logout
```

---

# 14. Current unfinished or problematic areas

These are important when understanding the project’s actual status.

1. **Order creation is not implemented.**  
   The checkout button does not currently save `Orders` or `OrderItem` rows.

2. **Order history is not implemented.**  
   The `order_` view only renders a template.

3. **Some order views do not require login.**  
   Address and checkout views should normally use `@login_required`.

4. **Address ownership checks are incomplete.**  
   Updating or deleting an address should verify that it belongs to `request.user`.

5. **Some product detail Add-to-Cart buttons are not functional.**

6. **`offer_msg` is referenced in `home.html`, but the view does not send it.**

7. **There are template syntax issues such as:**

   ```django
   {% else % }
   ```

   The normal syntax is:

   ```django
   {% else %}
   ```

8. **The password reset flow is not email-verified.**  
   Anyone who knows a username could potentially attempt to reset the password.

9. **Prices use `FloatField` and integer totals in the cart.**  
   E-commerce systems generally use `DecimalField` for money.

10. **Product stock is displayed but not reduced when items are added or ordered.**

11. **`order_by("?")` can be inefficient for large databases.**

12. **The project currently has `DEBUG = True` and an exposed development secret key.**  
   These settings should not be used in production.

13. **The repository has many uncommitted changes and generated files.**  
   The explanation above describes the current working tree, not necessarily only the last committed version.

---

# 15. Most important files to study first

If you want to understand the project efficiently, study them in this order:

1. `myproject/urls.py`
2. `myproject/settings.py`
3. `products/models.py`
4. `base/views.py`
5. `base/urls.py`
6. `authen/views.py`
7. `cart/views.py`
8. `orders/models.py`
9. `orders/views.py`
10. `templates/main.html`

In short, this project has the foundation of an online store: catalogue, authentication, cart, addresses, and checkout UI. The major missing business operation is converting the cart into a persistent order.

`Inspect database records` completed

Read Terminal
Completed with input: {
  "shellId": "5",
  "delay": 0
}

`Inspect migration state` completed

Read Terminal
Completed with input: {
  "shellId": "3",
  "delay": 0
}

`Read remaining Python modules` completed

Read Terminal
Completed with input: {
  "shellId": "4",
  "delay": 0
}

`Run Django system checks` completed

Read Terminal
Completed with input: {
  "shellId": "6",
  "delay": 0
}

## Verified current project state

- Django system check: **passed with 0 issues**
- Applied migrations: all current migrations are applied
- Users: **5**
- Profile pictures: **5**
- Categories: **5**
- Products: **26**
- Cart items: **6**
- Addresses: **2**
- Orders: **0**
- Order items: **0**

The database currently contains categories such as Electronics, Fashion, Fresh, Cosmetics, and Mobiles. Only one product is marked as trending, and no products are currently marked as offers.

The most important practical conclusion is:

> Product browsing, authentication, profiles, cart management, and addresses contain data and are functioning as the main features. Checkout is only a preview stage because there are currently no saved orders or order items, and the order-creation logic is not implemented yet.