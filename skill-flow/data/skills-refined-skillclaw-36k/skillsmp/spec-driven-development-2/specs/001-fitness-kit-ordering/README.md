# Feature 001: Fitness Kit Ordering System

**Status**: Planning Complete ✅  
**Created**: 2025-01-XX  
**Tech Stack**: Rails 8, Hotwire Turbo, SQLite3, Minitest

---

## 📋 Overview

A customer-facing e-commerce system for ordering fitness kits using single-use coupon codes. Features complete order management with shipping information, email validation, and automatic order confirmation number generation.

---

## 📁 Documentation Structure

| Document | Purpose |
|----------|---------|
| **spec.md** | Functional requirements, user stories, acceptance criteria |
| **plan.md** | Technical implementation plan, architecture, code structure |
| **data-model.md** | Database schema, ERD, relationships, sample data |
| **contracts/order_endpoints.md** | HTTP endpoints, request/response formats |
| **quickstart.md** | Manual testing scenarios, validation checklists |

---

## 🎯 Key Features

### User-Facing
- Browse available fitness kits with descriptions
- Place orders with complete shipping information
- Single-use coupon code validation
- Auto-generated 6-digit order confirmation numbers
- Order confirmation page with full summary

### Data Models
- **PromiseFitnessKit**: Product catalog (name, description)
- **CouponCode**: Single-use promotional codes (code, usage)
- **Order**: Customer orders with shipping & contact info

### Validations
- Email format validation
- 10-digit phone numbers (accepts dashes, stores digits)
- US state codes only (2-letter)
- ZIP code format (5-digit or ZIP+4)
- Coupon codes must exist and be unused

---

## 🚀 Implementation Status

- [x] Specification complete (`spec.md`)
- [x] Clarification complete (questions resolved)
- [x] Technical plan complete (`plan.md`)
- [x] Data model defined (`data-model.md`)
- [x] API contracts defined (`contracts/order_endpoints.md`)
- [x] Testing scenarios documented (`quickstart.md`)
- [ ] Task breakdown (next: `/speckit.tasks`)
- [ ] Implementation (next: `/speckit.implement`)

---

## 🏗️ Architecture Summary

### Routes
```ruby
GET  /                                                  # Homepage with kits
GET  /promise_fitness_kits/:id/orders/new              # Order form
POST /promise_fitness_kits/:id/orders                  # Create order
GET  /orders/:id                                       # Confirmation page
```

### Database Schema
```
promise_fitness_kits (3 records)
├── id
├── name (unique)
└── description

coupon_codes (10 records: 5 unused, 5 used)
├── id
├── code (unique)
└── usage ("unused" or "used")

orders
├── id
├── promise_fitness_kit_id (FK)
├── coupon_code_id (FK)
├── order_confirmation (unique, auto-generated)
├── customer info (name, email, phone)
├── shipping address (address1, address2, city, state, zip)
└── description (optional notes)
```

### Test Coverage
- **Unit Tests**: Models with all validations
- **Integration Tests**: Controllers with success/error cases
- **System Tests**: End-to-end user workflows
- **Target Coverage**: 90%+ (per project constitution)

---

## 🧪 Quick Validation

Once implemented, run through these scenarios:

1. **Happy Path**: Order a kit with unused coupon → See confirmation
2. **Used Coupon**: Try used coupon → See error popup
3. **Invalid Coupon**: Try non-existent coupon → See error
4. **Phone Format**: Enter "415-555-1234" → Stores "4155551234"
5. **Concurrent Orders**: Place 2 orders simultaneously → Different confirmation numbers

See `quickstart.md` for detailed testing scenarios.

---

## 📊 Sample Data

### Fitness Kits (3)
- Beginner Strength Kit
- Cardio Endurance Kit
- Flexibility & Recovery Kit

### Coupon Codes (10)
- **Unused**: WELCOME2024, FITNESS50, NEWYEAR, SPRING25, HEALTH100
- **Used**: USED001, USED002, USED003, USED004, USED005

### Orders (5)
- Pre-seeded sample orders across different states
- Confirmation numbers: 000001 through 000005

---

## 🔒 Security & Performance

### Security Checklist
- ✅ Strong parameters for mass assignment protection
- ✅ CSRF protection enabled (Rails default)
- ✅ SQL injection prevention (ActiveRecord)
- ✅ XSS prevention (ERB auto-escaping)
- ✅ Email validation and normalization
- ✅ Input sanitization (phone, state, zip)

### Performance Requirements
- Homepage load: < 200ms
- Order submission: < 500ms
- No N+1 queries (verified with Bullet gem)
- Eager loading for associations

---

## 🎓 Constitution Alignment

This feature follows the PromiseKits constitution:

- ✅ **Rails Conventions**: RESTful routing, standard MVC structure
- ✅ **Test-First**: All code has corresponding tests (90%+ coverage)
- ✅ **Hotwire-First**: Turbo for form submissions, Stimulus for phone formatting
- ✅ **YAGNI**: No over-engineering, building for current requirements only
- ✅ **Data Integrity**: Foreign keys, database constraints, validations
- ✅ **Performance**: Indexed columns, eager loading, no N+1 queries
- ✅ **Security**: Strong parameters, CSRF protection, input sanitization

---

## 🔄 Next Steps

### Phase 1: Task Breakdown
```bash
# Generate implementation tasks
/speckit.tasks
```

### Phase 2: Implementation
```bash
# Execute tasks systematically
/speckit.implement
```

### Phase 3: Validation
- Run all tests: `rails test`
- Run system tests: `rails test:system`
- Check Rubocop: `rubocop`
- Manual QA using `quickstart.md`
- Verify acceptance criteria in `spec.md`

---

## 📝 Notes

- Order confirmation numbers are integers (1, 2, 3...) stored in DB
- Displayed as 6-digit format with leading zeros (000001, 000002...)
- Phone accepts dashes in input but stores only 10 digits
- Coupon codes are case-insensitive (normalized to uppercase)
- Email and order creation are transactional (all-or-nothing)

---

## 🔗 Related Documents

- Project Constitution: `../../.specify/memory/constitution.md`
- Spec-Driven Development Guide: `../../SKILL.md`

---

**Ready for**: Task Breakdown (`/speckit.tasks`)  
**Author**: Spec-Driven Development Process  
**Last Updated**: 2025-01-XX