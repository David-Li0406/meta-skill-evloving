# Quickstart Guide: Fitness Kit Ordering System

**Feature ID**: 001-fitness-kit-ordering  
**Purpose**: Manual validation scenarios for quick testing  
**Last Updated**: 2025-01-XX

---

## Prerequisites

Before testing, ensure the following are complete:

```bash
# 1. Database migrations run
rails db:migrate

# 2. Seed data loaded
rails db:seed

# 3. Server running
rails server

# 4. Visit homepage
open http://localhost:3000
```

---

## Quick Validation Scenarios

### Scenario 1: Happy Path - Successful Order ✅

**Objective**: Place a complete order with valid data

**Steps**:
1. Navigate to homepage: `http://localhost:3000`
2. Click "Order This Kit" on "Beginner Strength Kit"
3. Fill out the form:
   - First Name: `Jane`
   - Last Name: `Smith`
   - Email: `jane.smith@example.com`
   - Phone: `415-555-1234` (accepts dashes)
   - Address 1: `123 Fitness Ave`
   - Address 2: _(leave blank)_
   - City: `San Francisco`
   - State: `CA`
   - ZIP: `94102`
   - Coupon Code: `WELCOME2024` (unused code)
4. Click "Place Order"

**Expected Result**:
- Redirects to confirmation page
- Shows confirmation number: `000001` (or next sequential)
- Displays order summary with all details
- Success message: "Order placed successfully!"
- Email confirmation message displayed

**Verify in Console**:
```bash
rails console
Order.last
# Should show the order with:
# - order_confirmation: 1
# - phone: "4155551234" (digits only)
# - email: "jane.smith@example.com" (lowercase)
# - state: "CA" (uppercase)

CouponCode.find_by(code: 'WELCOME2024').usage
# Should be "used"
```

---

### Scenario 2: Used Coupon Code Error ❌

**Objective**: Verify used coupon codes are rejected

**Steps**:
1. Navigate to homepage
2. Select any fitness kit
3. Fill out form with valid data
4. Enter coupon code: `USED001` (pre-marked as used in seeds)
5. Submit form

**Expected Result**:
- Form re-renders with error
- Error message: "This code has been used before and can no longer be used to place an order"
- All form data preserved (user doesn't lose input)
- No order created in database
- Status code: 422 Unprocessable Entity

**Verify in Console**:
```bash
Order.where(coupon_code: CouponCode.find_by(code: 'USED001')).count
# Should be 1 (only the seeded order, no new order)
```

---

### Scenario 3: Invalid Coupon Code ❌

**Objective**: Verify non-existent coupon codes are rejected

**Steps**:
1. Navigate to order form
2. Fill out valid data
3. Enter coupon code: `NOTEXIST999`
4. Submit form

**Expected Result**:
- Error message: "Invalid coupon code"
- Form data preserved
- No order created

---

### Scenario 4: Phone Number Validation and Formatting 📞

**Objective**: Test phone number validation and normalization

**Test Cases**:

| Input          | Expected Storage | Expected Display | Valid? |
|----------------|------------------|------------------|--------|
| 415-555-1234   | 4155551234       | (415) 555-1234   | ✅     |
| 4155551234     | 4155551234       | (415) 555-1234   | ✅     |
| 415 555 1234   | 4155551234       | (415) 555-1234   | ✅     |
| 123-4567       | N/A              | N/A              | ❌ (too short) |
| 415-555-12345  | N/A              | N/A              | ❌ (too long)  |
| abc-def-ghij   | N/A              | N/A              | ❌ (letters)   |

**Steps**:
1. Fill form with phone: `415-555-1234`
2. Submit valid order
3. Check confirmation page shows: `(415) 555-1234`
4. Check database stores: `4155551234`

**Verify**:
```bash
Order.last.phone
# => "4155551234"

Order.last.formatted_phone
# => "(415) 555-1234"
```

---

### Scenario 5: Email Validation 📧

**Objective**: Test email format validation and normalization

**Test Cases**:

| Input                    | Expected Storage         | Valid? |
|--------------------------|--------------------------|--------|
| user@example.com         | user@example.com         | ✅     |
| User@Example.COM         | user@example.com         | ✅     |
| user+tag@example.com     | user+tag@example.com     | ✅     |
| invalid.email            | N/A                      | ❌     |
| @example.com             | N/A                      | ❌     |
| user@                    | N/A                      | ❌     |

**Steps**:
1. Try submitting with email: `Test@EXAMPLE.COM`
2. Verify stored as: `test@example.com`

---

### Scenario 6: State Validation 🗺️

**Objective**: Verify only US states are accepted

**Valid Examples**: `CA`, `NY`, `TX`, `FL`, `WA`, `DC`

**Invalid Examples**: `XX`, `ZZ`, `ABC`, `California` (full name)

**Steps**:
1. Fill form with state: `ca` (lowercase)
2. Submit order
3. Verify stored as: `CA` (uppercase)

**Test Invalid**:
1. Fill form with state: `XX`
2. Submit
3. See error: "State must be a valid US state"

---

### Scenario 7: ZIP Code Format 📮

**Objective**: Test ZIP code validation

**Test Cases**:

| Input        | Valid? | Notes                      |
|--------------|--------|----------------------------|
| 94102        | ✅     | 5-digit                    |
| 94102-1234   | ✅     | ZIP+4                      |
| 02134        | ✅     | Preserves leading zero     |
| 1234         | ❌     | Too short                  |
| 123456       | ❌     | Too long (without dash)    |
| ABCDE        | ❌     | Letters                    |

**Steps**:
1. Submit order with ZIP: `02134`
2. Verify leading zero preserved in storage and display

---

### Scenario 8: Required vs Optional Fields 📝

**Required Fields** (form cannot submit without):
- First Name
- Last Name
- Email
- Phone
- Address 1
- City
- State
- ZIP
- Coupon Code

**Optional Fields** (can be blank):
- Address 2
- Order Description/Notes

**Steps**:
1. Try submitting form with only optional fields filled
2. Should see validation errors for all required fields
3. Fill all required fields, leave optional blank
4. Should submit successfully

---

### Scenario 9: Order Confirmation Number Sequence 🔢

**Objective**: Verify confirmation numbers increment properly

**Steps**:
1. Note current highest order confirmation number
2. Place first order → Note confirmation (e.g., 000006)
3. Place second order → Should be 000007
4. Place third order → Should be 000008

**Verify Display Format**:
- Database stores: `6`, `7`, `8` (integers)
- UI displays: `000006`, `000007`, `000008` (6-digit with leading zeros)

**Console Check**:
```bash
Order.maximum(:order_confirmation)
# => 8

Order.last.formatted_order_confirmation
# => "000008"
```

---

### Scenario 10: Concurrent Orders (Edge Case) 🏃‍♂️🏃‍♀️

**Objective**: Test that multiple orders don't get duplicate confirmation numbers

**Setup** (requires two browser sessions or tabs):
1. Open order form in Tab 1 and Tab 2
2. Fill both forms completely
3. Use different unused coupon codes
4. Submit both forms quickly (within 1 second)

**Expected Result**:
- Both orders succeed
- Confirmation numbers are different
- No duplicate order_confirmation values in database

**Verify**:
```bash
Order.pluck(:order_confirmation).uniq.count == Order.count
# => true (no duplicates)
```

---

### Scenario 11: Multiple Kits Ordering 🎁

**Objective**: Verify orders can be placed for different fitness kits

**Steps**:
1. Order "Beginner Strength Kit" with coupon `FITNESS50`
2. Order "Cardio Endurance Kit" with coupon `NEWYEAR`
3. Order "Flexibility & Recovery Kit" with coupon `SPRING25`

**Expected Result**:
- All three orders created successfully
- Each has unique confirmation number
- Each references correct fitness kit
- All three coupons marked as "used"

---

## Database Inspection Commands

### Check Available Fitness Kits
```bash
rails console
PromiseFitnessKit.all.pluck(:id, :name)
```

### Check Available Coupon Codes
```bash
CouponCode.unused.pluck(:code)
# Should show: ["WELCOME2024", "FITNESS50", "NEWYEAR", "SPRING25", "HEALTH100"]
```

### Check Recent Orders
```bash
Order.recent.includes(:promise_fitness_kit, :coupon_code).limit(5).each do |o|
  puts "Order ##{o.formatted_order_confirmation}: #{o.promise_fitness_kit.name} - #{o.full_name}"
end
```

### Check if Coupon is Used
```bash
CouponCode.find_by(code: 'WELCOME2024').used?
# => true or false
```

### Count Orders
```bash
Order.count
# Should be 5 from seeds initially
```

---

## Reset Test Data

If you need to reset the database for testing:

```bash
# Reset database and reload seeds
rails db:reset

# This will:
# 1. Drop the database
# 2. Recreate it
# 3. Run all migrations
# 4. Load seed data
```

Or just reload seeds (keeps existing data, adds seeds):

```bash
rails db:seed
```

---

## Browser Console Checks

### Check for JavaScript Errors
1. Open browser DevTools (F12)
2. Go to Console tab
3. Refresh page
4. Should see no errors (red messages)

### Check Turbo is Working
1. Submit order form
2. Watch Network tab in DevTools
3. Should see AJAX request, not full page reload
4. Page updates smoothly without flicker

---

## Performance Validation

### Check for N+1 Queries

With Bullet gem enabled in development:

1. Visit homepage
2. Click through to order form
3. Submit order
4. View confirmation page
5. Check terminal for Bullet warnings

**Expected**: No N+1 query warnings

**If warnings appear**:
- Add `.includes()` to controller queries
- Verify in `application.log`

---

## Common Issues & Solutions

### Issue: "Coupon code has already been used"
**Solution**: Use a different unused coupon from the seed data (WELCOME2024, FITNESS50, NEWYEAR, SPRING25, HEALTH100)

### Issue: Order confirmation shows as "1" instead of "000001"
**Solution**: Check that view uses `@order.formatted_order_confirmation` not `@order.order_confirmation`

### Issue: Phone stored with dashes
**Solution**: Check `normalize_attributes` callback in Order model is stripping non-digits

### Issue: Duplicate order confirmation numbers
**Solution**: Check that `generate_order_confirmation` uses database lock or transaction

### Issue: Form data lost on validation error
**Solution**: Ensure controller renders `:new` with status `:unprocessable_entity` (not redirect)

---

## Success Criteria Checklist

After running all scenarios, verify:

- [ ] Can browse all fitness kits on homepage
- [ ] Can select a kit and see order form
- [ ] Can place order with valid data
- [ ] Order confirmation number displays correctly (6-digit)
- [ ] Coupon codes validate (unused only)
- [ ] Used coupon shows specific error message
- [ ] Invalid coupon shows error
- [ ] Phone accepts dashes, stores digits only
- [ ] Email converts to lowercase
- [ ] State converts to uppercase
- [ ] ZIP preserves leading zeros
- [ ] Required fields enforced
- [ ] Optional fields work when blank
- [ ] Confirmation page shows all order details
- [ ] Multiple orders increment confirmation number
- [ ] No JavaScript errors in console
- [ ] No N+1 query warnings in logs
- [ ] Page loads under 200ms

---

**Status**: Ready for Testing  
**Estimated Testing Time**: 30-45 minutes for all scenarios
