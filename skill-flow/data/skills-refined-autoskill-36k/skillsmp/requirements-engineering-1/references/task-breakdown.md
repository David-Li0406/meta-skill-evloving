# Task Breakdown Patterns

## Technical Layer Strategy

Break features into standard Rails layers:

```
1. Database Layer (migrations, schema changes)
2. Model Layer (ActiveRecord models, validations)
3. Service Layer (business logic, external APIs)
4. Controller Layer (HTTP endpoints, routing)
5. View/Component Layer (UI, Hotwire components)
6. Testing Layer (RSpec tests, coverage)
```

---

## Example: JWT Authentication

**User Story**: "Add JWT authentication with refresh tokens"

### Epic Structure

```
AUTH-001 - JWT Authentication System (Epic)

AUTH-002: Add User authentication columns (DB)
├─ Migration: add_auth_columns_to_users
├─ Columns: password_digest, refresh_token, token_expires_at
└─ Dependencies: None

AUTH-003: Implement JWT token generation (Model)
├─ User model: generate_jwt_token, generate_refresh_token
├─ Token expiration logic
└─ Dependencies: AUTH-002

AUTH-004: Create AuthService for login/refresh (Service)
├─ AuthService.login(email, password)
├─ AuthService.refresh_token(refresh_token)
├─ AuthService.verify_token(jwt)
└─ Dependencies: AUTH-003

AUTH-005: Add authentication endpoints (Controller)
├─ POST /auth/login
├─ POST /auth/refresh
├─ POST /auth/logout
└─ Dependencies: AUTH-004

AUTH-006: Add RSpec tests (Testing)
├─ Model tests for token generation
├─ Service tests for auth flow
├─ Controller tests for endpoints
└─ Dependencies: AUTH-005
```

---

## Dependency Detection Rules

Automatic dependency assignment:

```
Database → Models (models depend on schema)
Models → Services (services use models)
Services → Controllers (controllers call services)
Controllers → Views (views render from controllers)
All layers → Tests (tests validate each layer)
```

---

## Example: Payment Processing

**Feature**: "Add payment processing with Stripe integration and invoice generation"

### Extracted Components

- Stripe integration
- Invoice generation

### Task Breakdown

```
PAY-001 - Payment Processing System (Epic)

PAY-002: Add payments table (DB)
├─ Migration: create_payments
├─ Columns: amount, status, stripe_id, user_id
└─ Dependencies: None

PAY-003: Add invoices table (DB)
├─ Migration: create_invoices
├─ Columns: payment_id, total, pdf_url
└─ Dependencies: PAY-002

PAY-004: Payment and Invoice models (Model)
├─ Payment: belongs_to :user, has_one :invoice
├─ Invoice: belongs_to :payment
└─ Dependencies: PAY-002, PAY-003

PAY-005: Stripe integration service (Service)
├─ PaymentService.charge(user, amount)
├─ PaymentService.refund(payment)
└─ Dependencies: PAY-004

PAY-006: Invoice generation service (Service)
├─ InvoiceService.generate(payment)
├─ PDF generation with Prawn/WickedPDF
└─ Dependencies: PAY-004

PAY-007: Payment controller endpoints (Controller)
├─ POST /payments
├─ GET /payments/:id
├─ POST /payments/:id/refund
└─ Dependencies: PAY-005, PAY-006

PAY-008: RSpec tests (Testing)
├─ Payment model specs
├─ Service specs with VCR cassettes
├─ Controller request specs
└─ Dependencies: PAY-007
```

---

## Complexity-Based Breakdown

### Simple Feature (Low Complexity)

```
- 1-2 files changed
- No new models
- Single layer modification
- Example: "Add email field to user profile"
```

### Standard Feature (Medium Complexity)

```
- 3-5 files changed
- May add new model
- Multiple layer modifications
- Example: "Add user notifications"
```

### Complex Feature (High Complexity)

```
- 6+ files changed
- Multiple new models
- External API integration
- Cross-cutting concerns
- Example: "Add subscription billing with Stripe"
```
