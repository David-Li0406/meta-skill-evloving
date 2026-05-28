# Feature Specification: Fitness Kit Ordering System

**Feature ID**: 001-fitness-kit-ordering  
**Status**: Draft  
**Created**: 2025-01-XX  
**Last Updated**: 2025-01-XX

---

## Overview

A customer-facing e-commerce system that allows users to browse fitness kits and place orders using single-use coupon codes. Each order captures complete shipping and contact information, validates coupon codes, and generates unique order confirmation numbers.

---

## User Stories

### US-1: Browse Fitness Kits
**As a** customer  
**I want to** view available fitness kits with descriptions  
**So that** I can choose which kit to order

**Acceptance Criteria:**
- Display all available fitness kits on the homepage
- Show kit name and full description for each kit
- Kits are presented in a clean, readable format
- Users can select a kit to proceed to order form

---

### US-2: Place Order with Coupon Code
**As a** customer  
**I want to** place an order for a fitness kit using a coupon code  
**So that** I can receive the kit at my address

**Acceptance Criteria:**
- Order form displays selected fitness kit name
- Form captures all required shipping and contact information
- Coupon code field is mandatory
- Form validates all inputs before submission
- Successful order displays confirmation message with order number
- User receives email with order confirmation number

**Required Form Fields:**
- First Name
- Last Name
- Address Line 1
- City
- State (2-letter code)
- ZIP Code
- Phone Number
- Email Address
- Coupon Code

**Optional Fields:**
- Address Line 2
- Order Description/Notes

---

### US-3: Coupon Code Validation
**As a** customer  
**I want to** receive immediate feedback on coupon code validity  
**So that** I know if I can complete my order

**Acceptance Criteria:**
- System validates coupon code exists in database
- System checks if coupon code has already been used
- If code is unused, order proceeds successfully
- If code is used, display popup message: "This code has been used before and can no longer be used to place an order"
- If code doesn't exist, display error: "Invalid coupon code"
- Used coupon codes cannot be reused
- Form cannot be submitted without a valid, unused coupon code
---

### US-4: Order Confirmation Number
**As a** customer  
**I want to** receive a unique order confirmation number  
**So that** I can reference my order when inquiring about status

**Acceptance Criteria:**
- Each order receives a unique confirmation number
- Confirmation number is auto-generated based on total order count
- Format: `XXXXX` (e.g., 000001, 000002)
- Confirmation number is displayed on success page
- Confirmation number is sent via email to customer
- No two orders can have the same confirmation number

---

## Data Models

### PromiseFitnessKit
**Purpose**: Catalog of available fitness kits

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | Primary Key | Auto-generated ID |
| name | string | NOT NULL, UNIQUE | Product name (also used as SKU) |
| description | text | NOT NULL | Full product description |
| created_at | datetime | NOT NULL | Timestamp |
| updated_at | datetime | NOT NULL | Timestamp |

**Relationships:**
- `has_many :orders`

**Validations:**
- Name must be present
- Name must be unique
- Description must be present

---

### CouponCode
**Purpose**: Single-use promotional codes for orders

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | Primary Key | Auto-generated ID |
| code | string | NOT NULL, UNIQUE | The coupon code itself (e.g., "SK18444IVF") |
| usage | string | NOT NULL | Either "unused" or "used" |
| created_at | datetime | NOT NULL | Timestamp |
| updated_at | datetime | NOT NULL | Timestamp |

**Relationships:**
- `has_many :orders`

**Validations:**
- Code must be present
- Code must be unique
- Usage must be either "unused" or "used"
- Code should be uppercase and alphanumeric

**Business Rules:**
- Coupons start as "unused"
- When an order is successfully created, coupon.usage changes to "used"
- Used coupons cannot be used again

---

### Order
**Purpose**: Customer orders for fitness kits

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | integer | Primary Key | Auto-generated ID |
| promise_fitness_kit_id | integer | Foreign Key, NOT NULL | Reference to ordered kit |
| coupon_code_id | integer | Foreign Key, NOT NULL | Reference to used coupon |
| order_confirmation | integer | NOT NULL, UNIQUE | Confirmation number (6-digit with leading zeros: 000001) |
| first_name | string | NOT NULL | Customer first name |
| last_name | string | NOT NULL | Customer last name |
| address1 | string | NOT NULL | Primary address line |
| address2 | string | NULL | Secondary address line (optional) |
| city | string | NOT NULL | City name |
| state | string | NOT NULL | 2-letter state code |
| zip | string | NOT NULL | ZIP code (supports 5-digit and ZIP+4) |
| phone | string | NOT NULL | Phone number (10 digits only, area code mandatory) |
| email | string | NOT NULL | Customer email address |
| description | text | NULL | Order notes/description (optional) |
| created_at | datetime | NOT NULL | Timestamp |
| updated_at | datetime | NOT NULL | Timestamp |

**Relationships:**
- `belongs_to :promise_fitness_kit`
- `belongs_to :coupon_code`

**Validations:**
- All required fields must be present
- Email must be valid format (e.g., user@example.com)
- ZIP must be 5 digits or ZIP+4 format (12345 or 12345-6789)
- State must be valid 2-letter US state code
- Phone must be exactly 10 digits (area code + 7-digit number)
- Phone accepts input with dashes (e.g., 123-456-7890) but stores only digits (1234567890)
- Coupon code must exist and be unused at time of order creation
- Order confirmation must be unique

**Business Rules:**
- Order confirmation auto-generated as 6-digit integer with leading zeros (000001, 000002, etc.)
- On successful order creation, associated coupon code.usage changes to "used"
- Cannot create order with already-used coupon code

---

## User Workflows

### Workflow 1: Successful Order Placement

1. **Customer visits homepage**
   - Sees list of all available fitness kits
   - Each kit shows name and description

2. **Customer selects a kit**
   - Clicks "Order This Kit" button
   - Redirects to order form with kit pre-selected

3. **Customer fills out order form**
   - Enters all required shipping information
   - Enters email address
   - Enters coupon code

4. **Customer submits form**
   - Client-side validation checks for missing fields
   - Server validates all inputs
   - Server checks coupon code exists and is unused

5. **Order is created**
   - System generates next order confirmation number
   - System saves order to database
   - System marks coupon code as "used"

6. **Success confirmation displayed**
   - Page shows success message
   - Displays order confirmation number
   - Shows summary of order details

7. **Confirmation email sent**
   - Email sent to customer's provided address
   - Contains order confirmation number
   - Includes order summary

---

### Workflow 2: Order with Used Coupon Code

1. **Customer visits homepage**
2. **Customer selects a kit**
3. **Customer fills out order form**
   - Enters all information including used coupon code

4. **Customer submits form**
   - Server validates coupon code
   - Finds that coupon.usage = "used"

5. **Error popup displayed**
   - Modal/popup appears with message:
   - "This code has been used before and can no longer be used to place an order"
   - Form remains filled (data not lost)
   - Customer can try different coupon code

---

### Workflow 3: Order with Invalid Coupon Code

1. **Customer visits homepage**
2. **Customer selects a kit**
3. **Customer fills out order form**
   - Enters coupon code that doesn't exist in database

4. **Customer submits form**
   - Server validates coupon code
   - Code not found in database

5. **Error message displayed**
   - Inline error or popup with message:
   - "Invalid coupon code"
   - Form remains filled
   - Customer can correct the coupon code

---

## Edge Cases

### EC-1: Empty States
- **No fitness kits in database**: Display message "No fitness kits available at this time"
- **All coupon codes used**: Customer cannot complete order; display appropriate message

### EC-2: Concurrent Orders
- **Two users submit same unused coupon simultaneously**: First transaction wins, second receives "code has been used" error
- Implement database-level locking or transaction isolation

### EC-3: Data Validation
- **Email with spaces**: Trim whitespace before validation
- **Phone with various formats**: Accept 123-456-7890 or 1234567890 as input, but store only digits (1234567890)
- **Phone must have area code**: Validate exactly 10 digits
- **ZIP code with leading zeros**: Store as string to preserve "01234"
- **State code lowercase**: Convert to uppercase before saving
- **State must be US state**: Validate against list of valid US state codes

### EC-4: Order Confirmation Number Generation
- **First order ever**: Should be 000001 (integer 1, displayed with leading zeros)
- **Concurrent order creation**: Ensure atomic increment, no duplicate numbers
- **Deleted orders**: Number sequence continues (gaps are acceptable)

### EC-5: Coupon Code Usage
- **Order creation fails after marking coupon used**: Rollback transaction, keep coupon unused
- **Case sensitivity**: Treat "SAVE20" and "save20" as same code (normalize to uppercase)

---

## Non-Functional Requirements

### Performance
- Order form submission response < 500ms
- Homepage with fitness kits loads in < 200ms
- Handle 10 concurrent order submissions without conflicts

### Security
- Validate all user inputs server-side (never trust client)
- Sanitize inputs to prevent SQL injection
- Use strong parameters for mass assignment protection
- CSRF protection enabled (Rails default)
- Email addresses stored lowercase for consistency

### Usability
- Form displays clear error messages
- Required fields marked with asterisk (*)
- Phone and ZIP formatting hints shown
- Success confirmation clearly visible
- Email confirmation sent within 30 seconds

### Reliability
- Coupon usage must be transactional (all-or-nothing)
- Order confirmation numbers must never duplicate
- Failed orders don't mark coupons as used

---

## Sample Data Requirements

### Fitness Kits (minimum 3)
1. **Beginner Strength Kit**
   - Description: "Perfect for those starting their fitness journey. Includes resistance bands, workout guide, and nutrition plan."

2. **Cardio Endurance Kit**
   - Description: "Boost your cardiovascular health. Includes jump rope, interval timer, and 30-day cardio challenge guide."

3. **Flexibility & Recovery Kit**
   - Description: "Essential tools for mobility and recovery. Includes foam roller, stretching guide, and recovery protocols."

### Coupon Codes (minimum 10)
- 5 unused codes: "WELCOME2024", "FITNESS50", "NEWYEAR", "SPRING25", "HEALTH100"
- 5 used codes: "USED001", "USED002", "USED003", "USED004", "USED005"

### Orders (minimum 5)
- Mix of all three fitness kits
- Various shipping addresses across different US states
- Order confirmations: 000001 through 000005
- Each using one of the "used" coupon codes
- Phone numbers with valid 10-digit format

---

## Success Criteria

✅ **Definition of Done:**
1. All three database tables created with proper schema
2. Foreign key relationships established and enforced
3. All validations working correctly
4. Homepage displays all fitness kits
5. Order form captures all required information
6. Coupon code validation prevents reuse
7. Order confirmation numbers auto-generate sequentially
8. Success page displays after order placement
9. Email sent with order confirmation (can be logged in development)
10. All edge cases handled gracefully
11. 90%+ test coverage (per constitution)
12. No N+1 queries (verified with Bullet gem)
13. All Rubocop violations resolved
14. Manual QA completed for all workflows

---

## Out of Scope (Future Features)

- Admin portal for managing kits and viewing orders
- Order status tracking beyond confirmation
- Payment processing
- Inventory management
- Order editing or cancellation
- User accounts/authentication
- Order history for returning customers
- Email customization
- Shipping method selection
- Tax calculation
- Multiple items per order

---

## Questions for Clarification

- [x] Order confirmation format: 6-digit integer with leading zeros (000001)
- [ ] Email confirmation: Deferred - will decide later
- [x] State validation: US states only
- [x] Phone validation: Accept dashes in input, store only 10 digits, area code mandatory
- [ ] Fitness kit images: Deferred - will decide later
- [x] Coupon code generation: Admin will create (implementation deferred)

---

## Acceptance Checklist

- [ ] Specification reviewed and approved
- [ ] All ambiguities resolved via `/speckit.clarify`
- [ ] Sample data requirements defined
- [ ] Edge cases documented
- [ ] Success criteria clear and measurable
- [ ] Out of scope items identified
- [ ] Ready for technical planning (`/speckit.plan`)
