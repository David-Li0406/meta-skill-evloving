# API Contracts: Order Endpoints

**Feature ID**: 001-fitness-kit-ordering  
**Last Updated**: 2025-01-XX

---

## Overview

This document defines the HTTP endpoints for the fitness kit ordering system. All endpoints follow RESTful conventions and use Rails form submissions with Turbo.

---

## Endpoints

### 1. Homepage - List Fitness Kits

**Endpoint**: `GET /`  
**Route Name**: `root_path`  
**Controller**: `HomeController#index`  
**Authentication**: None required

#### Request

```http
GET / HTTP/1.1
Host: example.com
Accept: text/html
```

#### Response (Success)

**Status**: `200 OK`  
**Content-Type**: `text/html`

**Body**: HTML page containing:
- List of all available fitness kits
- Each kit displays: name, description, "Order This Kit" button
- Empty state if no kits available

#### Example Response Data

```html
<!-- Rendered view with @promise_fitness_kits -->
<div class="fitness-kits">
  <div class="kit-card">
    <h2>Beginner Strength Kit</h2>
    <p>Perfect for those starting their fitness journey...</p>
    <a href="/promise_fitness_kits/1/orders/new">Order This Kit</a>
  </div>
  <!-- More kits... -->
</div>
```

---

### 2. New Order Form

**Endpoint**: `GET /promise_fitness_kits/:promise_fitness_kit_id/orders/new`  
**Route Name**: `new_promise_fitness_kit_order_path(promise_fitness_kit)`  
**Controller**: `OrdersController#new`  
**Authentication**: None required

#### Request

```http
GET /promise_fitness_kits/1/orders/new HTTP/1.1
Host: example.com
Accept: text/html
```

#### URL Parameters

| Parameter              | Type    | Required | Description                    |
|------------------------|---------|----------|--------------------------------|
| promise_fitness_kit_id | integer | Yes      | ID of the fitness kit to order |

#### Response (Success)

**Status**: `200 OK`  
**Content-Type**: `text/html`

**Body**: HTML form containing:
- Selected fitness kit details (name, description)
- Order form with all required fields
- Coupon code input field
- Submit button

#### Response (Kit Not Found)

**Status**: `404 Not Found`  
**Content-Type**: `text/html`

**Body**: Rails 404 error page

---

### 3. Create Order

**Endpoint**: `POST /promise_fitness_kits/:promise_fitness_kit_id/orders`  
**Route Name**: `promise_fitness_kit_orders_path(promise_fitness_kit)`  
**Controller**: `OrdersController#create`  
**Authentication**: None required

#### Request

```http
POST /promise_fitness_kits/1/orders HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded
Accept: text/html

order[first_name]=John&
order[last_name]=Doe&
order[email]=john@example.com&
order[phone]=123-456-7890&
order[address1]=123+Main+St&
order[address2]=&
order[city]=San+Francisco&
order[state]=CA&
order[zip]=94102&
order[description]=&
order[coupon_code_input]=WELCOME2024
```

#### URL Parameters

| Parameter              | Type    | Required | Description                    |
|------------------------|---------|----------|--------------------------------|
| promise_fitness_kit_id | integer | Yes      | ID of the fitness kit to order |

#### Form Parameters

| Parameter                    | Type   | Required | Validation                           |
|------------------------------|--------|----------|--------------------------------------|
| order[first_name]            | string | Yes      | Present                              |
| order[last_name]             | string | Yes      | Present                              |
| order[email]                 | string | Yes      | Valid email format                   |
| order[phone]                 | string | Yes      | 10 digits (accepts dashes in input)  |
| order[address1]              | string | Yes      | Present                              |
| order[address2]              | string | No       | Optional                             |
| order[city]                  | string | Yes      | Present                              |
| order[state]                 | string | Yes      | 2-letter US state code               |
| order[zip]                   | string | Yes      | 5 digits or ZIP+4 format             |
| order[description]           | text   | No       | Optional                             |
| order[coupon_code_input]     | string | Yes      | Must match existing unused coupon    |

#### Response (Success - Order Created)

**Status**: `302 Found` (Redirect)  
**Location**: `/orders/:id`  
**Flash Message**: "Order placed successfully!"

```http
HTTP/1.1 302 Found
Location: /orders/1
Set-Cookie: _promisekits_session=...
```

**Follow-up GET /orders/:id returns**:
- Status: `200 OK`
- Order confirmation page with order details

#### Response (Invalid Coupon Code)

**Status**: `422 Unprocessable Entity`  
**Content-Type**: `text/html`

**Body**: Order form re-rendered with error message:
- Flash error: "Invalid coupon code"
- Form fields retain submitted values
- Turbo response updates page without full reload

```html
<div class="alert alert-error">
  Invalid coupon code
</div>
<!-- Form with preserved values -->
```

#### Response (Used Coupon Code)

**Status**: `422 Unprocessable Entity`  
**Content-Type**: `text/html`

**Body**: Order form re-rendered with error message:
- Flash error: "This code has been used before and can no longer be used to place an order"
- Form fields retain submitted values

```html
<div class="alert alert-error">
  This code has been used before and can no longer be used to place an order
</div>
<!-- Form with preserved values -->
```

#### Response (Validation Errors)

**Status**: `422 Unprocessable Entity`  
**Content-Type**: `text/html`

**Body**: Order form re-rendered with validation errors:
- Error summary at top of form
- Inline errors next to invalid fields
- Form fields retain submitted values

```html
<div class="alert alert-error">
  <h3>10 errors prohibited this order:</h3>
  <ul>
    <li>Email must be a valid email</li>
    <li>Phone must be exactly 10 digits</li>
    <li>State must be a valid US state</li>
    <!-- More errors... -->
  </ul>
</div>
<!-- Form with preserved values and inline errors -->
```

#### Response (Kit Not Found)

**Status**: `404 Not Found`  
**Content-Type**: `text/html`

**Body**: Rails 404 error page

---

### 4. Order Confirmation Page

**Endpoint**: `GET /orders/:id`  
**Route Name**: `order_path(order)`  
**Controller**: `OrdersController#show`  
**Authentication**: None required

#### Request

```http
GET /orders/1 HTTP/1.1
Host: example.com
Accept: text/html
```

#### URL Parameters

| Parameter | Type    | Required | Description          |
|-----------|---------|----------|----------------------|
| id        | integer | Yes      | ID of the order      |

#### Response (Success)

**Status**: `200 OK`  
**Content-Type**: `text/html`

**Body**: HTML page containing:
- Success message with order confirmation number (formatted: 000001)
- Order summary:
  - Fitness kit name
  - Customer name and shipping address
  - Contact information (email, phone)
  - Order notes (if provided)
- Link to return home

#### Example Response Data

```html
<div class="success-message">
  <h1>✓ Order Confirmed!</h1>
  <p>Your order confirmation number is: <strong>000001</strong></p>
  <p>A confirmation email has been sent to <strong>john@example.com</strong></p>
</div>

<div class="order-summary">
  <h2>Order Summary</h2>
  
  <h3>Fitness Kit</h3>
  <p><strong>Beginner Strength Kit</strong></p>
  
  <h3>Shipping To</h3>
  <p>
    John Doe<br>
    123 Main St<br>
    San Francisco, CA 94102
  </p>
  
  <h3>Contact Information</h3>
  <p>
    Email: john@example.com<br>
    Phone: (415) 555-1234
  </p>
</div>
```

#### Response (Order Not Found)

**Status**: `404 Not Found`  
**Content-Type**: `text/html`

**Body**: Rails 404 error page

---

## Data Transformations

### Phone Number
- **Input**: Accepts "123-456-7890" or "1234567890"
- **Storage**: Stores "1234567890" (digits only)
- **Display**: Shows "(123) 456-7890"

### Email
- **Input**: Any email format with whitespace
- **Storage**: Lowercase, trimmed (e.g., "john@example.com")
- **Display**: Lowercase format

### State
- **Input**: Accepts "ca", "CA", " CA "
- **Storage**: Uppercase, trimmed (e.g., "CA")
- **Validation**: Must be valid 2-letter US state code

### Coupon Code
- **Input**: Accepts "welcome2024", "WELCOME2024", " welcome2024 "
- **Lookup**: Normalized to uppercase, trimmed
- **Validation**: Must exist and have usage = "unused"

### Order Confirmation
- **Storage**: Integer (1, 2, 3...)
- **Display**: 6-digit format with leading zeros (000001, 000002, 000003...)

---

## Error Handling

### Client-Side Validation (HTML5)
- Required fields marked with `required` attribute
- Email fields use `type="email"`
- Form cannot be submitted with missing required fields

### Server-Side Validation (Rails)
- All validations enforced in model layer
- Errors displayed in form with specific messages
- Form data preserved on validation errors
- Turbo handles form resubmission without full page reload

### Common Error Messages

| Field       | Error Condition        | Message                                  |
|-------------|------------------------|------------------------------------------|
| email       | Invalid format         | "Email must be a valid email"            |
| phone       | Not 10 digits          | "Phone must be exactly 10 digits"        |
| phone       | Contains letters       | "Phone must contain only digits"         |
| state       | Not US state           | "State must be a valid US state"         |
| zip         | Invalid format         | "Zip must be 5 digits or ZIP+4"          |
| coupon_code | Doesn't exist          | "Invalid coupon code"                    |
| coupon_code | Already used           | "This code has been used before..."      |
| first_name  | Missing                | "First name can't be blank"              |

---

## Security Considerations

### CSRF Protection
- All POST requests include CSRF token
- Rails `form_with` helper automatically includes token
- Invalid token results in `ActionController::InvalidAuthenticityToken` exception

### Strong Parameters
- Controller uses `order_params` whitelist
- Only permitted attributes can be mass-assigned
- `coupon_code_input` handled separately (not part of order model)

### SQL Injection Prevention
- All queries use ActiveRecord parameterization
- No raw SQL with user input
- Foreign key constraints enforced at database level

### Input Sanitization
- Phone: Remove non-digit characters
- Email: Downcase and trim
- State: Upcase and trim
- Coupon code: Upcase and trim before lookup

---

## Performance

### Expected Response Times
- GET / (homepage): < 200ms
- GET /orders/new: < 200ms
- POST /orders (create): < 500ms
- GET /orders/:id: < 200ms

### Caching Strategy (Future)
- Fragment cache for fitness kit list
- Page cache for static content
- Russian doll caching for nested content

### N+1 Query Prevention
- Use `includes(:promise_fitness_kit, :coupon_code)` when loading orders
- Bullet gem monitors queries in development
- Eager load associations in controller actions

---

## Testing Checklist

### Controller Tests
- [ ] GET / returns 200 and lists kits
- [ ] GET /orders/new returns 200 with form
- [ ] POST /orders with valid data creates order
- [ ] POST /orders with valid data redirects to show
- [ ] POST /orders with invalid coupon shows error
- [ ] POST /orders with used coupon shows specific error
- [ ] POST /orders with invalid data shows validation errors
- [ ] GET /orders/:id returns 200 with order details
- [ ] All endpoints handle 404 for missing records

### System Tests
- [ ] User can browse kits
- [ ] User can select kit and see order form
- [ ] User can submit valid order and see confirmation
- [ ] User sees error popup for used coupon
- [ ] User sees error for invalid coupon
- [ ] User sees validation errors for invalid data
- [ ] Phone formatting works in real-time

---

**Status**: Complete  
**Ready for Implementation**: Yes