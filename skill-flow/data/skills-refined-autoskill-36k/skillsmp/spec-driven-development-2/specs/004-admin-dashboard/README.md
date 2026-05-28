# Spec 004: Admin Dashboard

## Status
**Current Phase**: Planning Complete ✅  
**Next Phase**: Implementation  
**Priority**: High  
**Estimated Effort**: 10-14 hours

---

## Overview

This specification defines a secure admin dashboard for PromiseKits that allows authorized administrators to:
- Authenticate and manage their own accounts
- Create and manage coupon codes with auto-generated sequential format
- View and search customer orders
- Access dashboard statistics and insights

The implementation follows Rails 8 conventions, uses Hotwire for interactivity, and implements cursor-based pagination for performance.

---

## Spec-Driven Development Process

This feature was developed using the spec-driven development workflow as defined in `SKILL.md`:

### ✅ Step 1: Constitution
Project principles already established in `.specify/memory/constitution.md`
- Rails conventions over configuration
- Test-first development (TDD)
- Hotwire-first interactivity
- Simplicity and YAGNI
- Security standards

### ✅ Step 2: Specification (`spec.md`)
Functional requirements defined with:
- User stories (admin authentication, coupon management, order viewing, password management)
- Acceptance criteria (authentication, CRUD operations, security)
- Data requirements (Admin model, coupon code format)
- Workflows (login, create coupon, search orders, change password)
- Edge cases and sample data

### ✅ Step 3: Clarification
Questions resolved:
1. **Coupon Deletion**: Can delete unused, cannot delete used
2. **Password Management**: Admins can change own passwords
3. **Admin Attribution**: Not tracking who created coupons
4. **Coupon Format**: SK + sequential integer + 3 random letters (e.g., SK187524MYQ)
5. **Order Sorting**: Newest first (descending)
6. **Pagination**: Cursor-based for performance
7. **Session Duration**: 12 hours

### ✅ Step 4: Implementation Plan (`plan.md`)
Technical architecture defined:
- **Tech Stack**: Rails 8, Hotwire Turbo, bcrypt, cursor pagination
- **Models**: Admin (new), CouponCode (modified), Order (modified)
- **Controllers**: Admin namespace with BaseController, Sessions, Dashboard, CouponCodes, Orders, Passwords
- **Views**: Admin layout, login, dashboard, coupon management, order viewing
- **Security**: Session-based auth, bcrypt hashing, CSRF protection, 12-hour timeout
- **Performance**: Eager loading, indexed queries, cursor pagination

### ✅ Step 4.5: Data Model (`data-model.md`)
Database schema documented:
- Admins table (username, password_digest)
- Indexes for performance (usage, created_at, composite indexes)
- Coupon code generation logic
- Cursor pagination query patterns
- Data integrity rules

### ✅ Step 5: Task Breakdown (`tasks.md`)
Implementation tasks ordered by dependency:
- **Phase 1**: Foundation & Authentication (6 tasks)
- **Phase 2**: Coupon Code Management (5 tasks)
- **Phase 3**: Order Viewing (4 tasks)
- **Phase 4**: Dashboard & Statistics (3 tasks)
- **Phase 5**: Password Management (3 tasks)
- **Phase 6**: Polish & Final Testing (6 tasks)

**Total**: 29 tasks with clear acceptance criteria

### ✅ Step 5.5: Quick Start Guide (`quickstart.md`)
Validation scenarios for testing:
- 11 detailed test scenarios
- Quick smoke test (5 minutes)
- Performance checks
- Security validation
- Mobile/browser compatibility tests

### ⏳ Step 6: Implementation (NEXT)
Ready to begin implementation following task order in `tasks.md`

---

## Key Features

### Coupon Code Auto-Generation
- Format: `SK[sequential_integer][3_random_letters]`
- Example sequence: SK1000AAA, SK1001BBB, SK1002CCC
- System finds highest integer and increments
- Three random uppercase letters suffix
- First code starts at SK1000AAA

### Cursor-Based Pagination
- More efficient than offset pagination
- Uses primary key (id) or created_at as cursor
- Fetches 25 records per page
- Maintains state with filters and search

### Security Features
- Bcrypt password hashing (cost factor 12)
- Session-based authentication
- 12-hour session timeout with sliding window
- CSRF protection on all forms
- Authorization checks on all admin routes
- SQL injection prevention via ActiveRecord

### Performance Optimization
- Eager loading to prevent N+1 queries
- Database indexes on foreign keys and filter columns
- Cursor pagination for large datasets
- Target: < 50ms for all queries

---

## File Structure

```
specs/004-admin-dashboard/
├── README.md                    # This file
├── spec.md                      # Functional specification
├── plan.md                      # Technical implementation plan
├── data-model.md                # Database schema and queries
├── tasks.md                     # Ordered task breakdown
└── quickstart.md                # Validation scenarios
```

---

## Dependencies

### Existing Models
- `PromiseFitnessKit` (from spec 001)
- `CouponCode` (from spec 001, will be modified)
- `Order` (from spec 001, will be modified)

### Gems Required
- `bcrypt` - Already in Rails (via has_secure_password)
- No additional gems needed (using Rails built-ins)

### Database Migrations
1. `CreateAdmins` - New admins table
2. `AddIndexesToCouponCodes` - Performance indexes
3. `AddIndexesToOrdersForPagination` - Cursor pagination indexes

---

## Implementation Checklist

Before starting implementation:
- [ ] Review constitution principles (`.specify/memory/constitution.md`)
- [ ] Review complete specification (`spec.md`)
- [ ] Review technical plan (`plan.md`)
- [ ] Review data model (`data-model.md`)
- [ ] Review task order (`tasks.md`)
- [ ] Set up test fixtures and seed data

During implementation:
- [ ] Follow TDD: Write test → Implement → Pass → Refactor
- [ ] Complete tasks in dependency order
- [ ] Check off acceptance criteria for each task
- [ ] Run tests frequently
- [ ] Check for N+1 queries (Bullet gem if available)

After implementation:
- [ ] Run full test suite (models, controllers, system tests)
- [ ] Validate with quick start scenarios (`quickstart.md`)
- [ ] Security audit (authentication, CSRF, SQL injection, XSS)
- [ ] Performance audit (query times, N+1 queries, indexes)
- [ ] Mobile responsiveness check
- [ ] Browser compatibility check
- [ ] Create implementation summary document

---

## Acceptance Criteria Summary

### Authentication (7 criteria)
- Admin login page at `/admin/login`
- Unauthenticated users redirected
- Valid credentials grant access
- Invalid credentials show error
- Logout clears session
- Session persists across requests
- Session timeout after 12 hours

### Coupon Management (9 criteria)
- View list with cursor pagination
- Auto-generate codes in SK[int][3letters] format
- Sequential integer increments
- Delete unused coupons
- Cannot delete used coupons
- Filter by status (all/unused/used)
- Search by code text
- Success/error messages

### Order Management (7 criteria)
- View list newest first
- Cursor pagination
- View individual order details
- Search by name, email, coupon code
- Display complete information
- Dashboard shows statistics

### Password Management (5 criteria)
- Change own password
- Require current password
- Validate new password (8+ chars)
- Show success message
- Remain logged in after change

### Security (5 criteria)
- Bcrypt password hashing
- CSRF protection enabled
- All routes require authentication
- Non-admins cannot access
- Session management

### User Experience (5 criteria)
- Distinct admin visual identity
- Form validation with errors
- Success messages
- Intuitive navigation
- Mobile responsive

**Total**: 38 acceptance criteria

---

## Testing Strategy

### Test Coverage Targets
- Models: 90%+
- Controllers: 90%+
- System tests: Critical workflows

### Test Types
1. **Unit Tests** (models) - Validations, methods, scopes
2. **Controller Tests** - Authentication, actions, responses
3. **System Tests** - End-to-end workflows with Capybara

### Key Test Scenarios
- Authentication flow (login/logout/timeout)
- Coupon code generation and validation
- Coupon deletion protection
- Order search across multiple fields
- Cursor pagination navigation
- Password change with validation
- Unauthorized access attempts

---

## Success Metrics

- [ ] All 38 acceptance criteria met
- [ ] All tests passing (90%+ coverage)
- [ ] No N+1 queries in admin views
- [ ] All queries < 50ms
- [ ] Page loads < 200ms
- [ ] Mobile responsive
- [ ] Works in Chrome, Firefox, Safari, Edge
- [ ] No security vulnerabilities
- [ ] Admin can complete all workflows

---

## Out of Scope (Future Enhancements)

- Password reset via email
- Multiple admin roles/permissions
- Two-factor authentication
- Email notifications to admins
- Export orders to CSV
- Bulk coupon generation
- Order fulfillment tracking
- Analytics dashboard with charts
- Admin activity audit log
- Admin user management (CRUD other admins)

---

## Next Steps

To begin implementation:

```bash
# 1. Review all spec documents
cat specs/004-admin-dashboard/spec.md
cat specs/004-admin-dashboard/plan.md
cat specs/004-admin-dashboard/tasks.md

# 2. Start with Phase 1, Task 1.1
# Create Admin model with tests

# 3. Follow TDD workflow
# Write test → Run (fails) → Implement → Run (passes) → Refactor
```

Refer to `tasks.md` for detailed step-by-step implementation guidance.

---

**Spec ID**: 004  
**Feature**: Admin Dashboard  
**Created**: 2025-01-08  
**Status**: Ready for Implementation  
**Estimated Duration**: 10-14 hours  
**Assigned To**: [Your Name]