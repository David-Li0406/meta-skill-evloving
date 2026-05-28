# Quick Start: Admin Dashboard Validation

## Purpose
This guide provides quick validation scenarios to verify the admin dashboard implementation is working correctly. Use this after implementation to smoke test the feature.

---

## Prerequisites

1. **Database Setup**
   ```bash
   rails db:migrate
   rails db:seed
   ```

2. **Start Rails Server**
   ```bash
   rails server
   ```

3. **Test Credentials** (from seeds)
   - Username: `admin`
   - Password: `password123`

---

## Validation Scenarios

### Scenario 1: Basic Authentication (2 minutes)

**Objective**: Verify login/logout functionality

1. Navigate to `http://localhost:3000/admin`
2. ✅ Should redirect to `/admin/login`
3. Enter invalid credentials (username: `wrong`, password: `wrong`)
4. ✅ Should show error message "Invalid username or password"
5. ✅ Should remain on login page
6. Enter valid credentials (username: `admin`, password: `password123`)
7. ✅ Should redirect to `/admin/dashboard` or `/admin`
8. ✅ Should see admin header with username displayed
9. Click "Logout" button
10. ✅ Should redirect to homepage
11. ✅ Should clear session (trying to access `/admin` redirects to login)

**Pass Criteria**: Login, logout, and error handling work correctly.

---

### Scenario 2: Dashboard Statistics (2 minutes)

**Objective**: Verify dashboard displays correct statistics

1. Log in as admin
2. Navigate to `/admin/dashboard` (or `/admin`)
3. ✅ Should see total order count (3 if using seed data)
4. ✅ Should see total coupon count (8 if using seed data)
5. ✅ Should see unused coupon count
6. ✅ Should see orders breakdown by kit type
7. ✅ Should see recent orders list (5 most recent)
8. Click link to "Coupon Codes"
9. ✅ Should navigate to coupon codes page
10. Click "Dashboard" in navigation
11. ✅ Should return to dashboard

**Pass Criteria**: All statistics display correct numbers, navigation works.

---

### Scenario 3: Coupon Code Creation (3 minutes)

**Objective**: Verify auto-generation of coupon codes

1. Navigate to `/admin/coupon_codes`
2. ✅ Should see list of existing coupon codes
3. ✅ Codes should follow format: SK[number][3 letters] (e.g., SK1000AAA)
4. Note the highest number in the list (e.g., if SK1007HHH exists, highest is 1007)
5. Click "New Coupon Code" or "Create Coupon" button
6. ✅ Form should submit (may be single button, no form fields)
7. ✅ Should redirect back to coupon list
8. ✅ Should see success message
9. ✅ New coupon should appear in list
10. ✅ New coupon number should be highest + 1 (e.g., SK1008XYZ if previous was 1007)
11. ✅ New coupon status should be "unused"
12. Create 2 more coupons
13. ✅ Numbers should increment sequentially (1009, 1010, etc.)
14. ✅ Letter suffixes should be random (3 uppercase letters)

**Pass Criteria**: Coupons auto-generate with sequential numbers and random letters.

---

### Scenario 4: Coupon Code Filtering & Search (2 minutes)

**Objective**: Verify filtering and search functionality

1. On `/admin/coupon_codes` page
2. Click "Unused" filter
3. ✅ Should show only unused coupons
4. ✅ Should NOT show used coupons
5. Click "Used" filter
6. ✅ Should show only used coupons (those associated with orders)
7. Click "All" filter
8. ✅ Should show all coupons
9. Enter "SK1000" in search box
10. Submit search
11. ✅ Should show only codes matching "SK1000" (e.g., SK1000AAA)
12. Clear search
13. ✅ Should show all coupons again

**Pass Criteria**: Filters and search return correct results.

---

### Scenario 5: Coupon Code Deletion (3 minutes)

**Objective**: Verify deletion protection for used coupons

1. On `/admin/coupon_codes` page
2. Filter by "Unused"
3. Find a coupon with status "unused" and no associated order
4. Click "Delete" button for that coupon
5. ✅ Should show confirmation dialog (if implemented)
6. Confirm deletion
7. ✅ Should redirect to coupon list
8. ✅ Should show success message "Coupon deleted successfully"
9. ✅ Deleted coupon should no longer appear in list
10. Filter by "Used" (or "All" and look for used coupons)
11. Find a coupon with status "used" or associated with an order
12. ✅ Delete button should either:
    - Not appear for used coupons, OR
    - Appear but fail with error message when clicked
13. If delete button exists, click it
14. ✅ Should show error message "Cannot delete coupon code associated with orders"
15. ✅ Coupon should still exist in list

**Pass Criteria**: Unused coupons can be deleted, used coupons cannot.

---

### Scenario 6: Order Viewing (3 minutes)

**Objective**: Verify order list and detail views

1. Navigate to `/admin/orders`
2. ✅ Should see list of orders
3. ✅ Orders should be sorted newest first (check timestamps/dates)
4. ✅ Each row should show: Order ID, Customer Name, Kit Name, Coupon Code, Date
5. Click on an order (row or ID link)
6. ✅ Should navigate to order detail page `/admin/orders/:id`
7. ✅ Should see complete customer information:
   - Full name
   - Email address
   - Phone number
   - Full address (address1, address2, city, state, zip)
8. ✅ Should see order details:
   - Fitness kit name and description
   - Coupon code used
   - Order date/time
9. ✅ Should see special instructions (if any) or "N/A"
10. Click "Back to Orders" or navigate to `/admin/orders`
11. ✅ Should return to order list

**Pass Criteria**: Orders display correctly, all information shown.

---

### Scenario 7: Order Search (2 minutes)

**Objective**: Verify order search functionality

1. On `/admin/orders` page
2. Enter a customer first name (e.g., "John" if using seed data) in search box
3. Submit search
4. ✅ Should show only orders matching that customer name
5. Clear search, enter customer email (e.g., "jane.smith@example.com")
6. Submit search
7. ✅ Should show orders matching that email
8. Clear search, enter coupon code (e.g., "SK1003DDD")
9. Submit search
10. ✅ Should show orders using that coupon code
11. Enter search term with no matches (e.g., "NOMATCH")
12. ✅ Should show "No orders found" or empty list
13. Clear search
14. ✅ Should show all orders again

**Pass Criteria**: Search works for names, emails, and coupon codes.

---

### Scenario 8: Cursor Pagination (4 minutes)

**Objective**: Verify cursor-based pagination works

**Setup**: Need more than 25 coupons/orders. If seed data insufficient:
```bash
rails console
25.times { CouponCode.create!(code: CouponCode.generate_next_code, usage: 'unused') }
```

1. Navigate to `/admin/coupon_codes`
2. If total coupons <= 25:
   - ✅ "Next" button should be disabled
   - ✅ "Previous" button should be disabled
3. If total coupons > 25:
   - ✅ Should see first 25 coupons
   - ✅ "Next" button should be enabled
   - ✅ "Previous" button should be disabled
   - Click "Next"
   - ✅ Should load next page (different coupons)
   - ✅ URL should include cursor parameter
   - ✅ "Previous" button now enabled
   - Click "Previous"
   - ✅ Should return to first page
   - ✅ "Previous" button disabled again
4. Apply filter (e.g., "Unused")
5. Navigate through pages
6. ✅ Filter should persist across pagination
7. Apply search term
8. Navigate through pages
9. ✅ Search should persist across pagination

**Pass Criteria**: Pagination works, maintains state with filters/search.

---

### Scenario 9: Password Change (3 minutes)

**Objective**: Verify admin can change own password

1. While logged in, navigate to `/admin/password/edit` or click "Change Password" link
2. ✅ Should see password change form with 3 fields:
   - Current password
   - New password
   - Confirm new password
3. Enter incorrect current password
4. Enter new password and confirmation (matching)
5. Submit form
6. ✅ Should show error "Current password is incorrect"
7. ✅ Should remain on password form
8. Enter correct current password: `password123`
9. Enter mismatched new passwords (e.g., "newpass123" and "newpass456")
10. Submit form
11. ✅ Should show error "New password and confirmation don't match"
12. Enter correct current password: `password123`
13. Enter short new password: "short"
14. Submit form
15. ✅ Should show error about password length (minimum 8 characters)
16. Enter correct current password: `password123`
17. Enter valid new password: `newpassword123` (both fields)
18. Submit form
19. ✅ Should redirect to dashboard
20. ✅ Should show success message "Password updated successfully"
21. ✅ Should still be logged in (session persists)
22. Logout
23. Try logging in with old password `password123`
24. ✅ Should fail (invalid credentials)
25. Login with new password `newpassword123`
26. ✅ Should succeed

**Pass Criteria**: Password change works, validation enforced, session persists.

---

### Scenario 10: Session Timeout (Optional - 12+ hours)

**Objective**: Verify session expires after 12 hours

**Note**: This test requires waiting 12 hours or manually manipulating session data.

**Manual Test**:
1. Log in as admin
2. Note the time
3. Leave browser open
4. Wait 12 hours
5. Try to navigate to any admin page
6. ✅ Should redirect to login page
7. ✅ Session should be cleared

**Programmatic Test** (via console):
```bash
rails console
# Find or create a session in the sessions table (if using database sessions)
# Or manually set session[:admin_expires_at] to a past time and test
```

**Pass Criteria**: Sessions expire after 12 hours of inactivity.

---

### Scenario 11: Security Validation (5 minutes)

**Objective**: Verify unauthorized access is blocked

1. **Logout or open incognito window**
2. Try to access `/admin/dashboard` without logging in
3. ✅ Should redirect to `/admin/login`
4. Try to access `/admin/coupon_codes` without logging in
5. ✅ Should redirect to `/admin/login`
6. Try to access `/admin/orders` without logging in
7. ✅ Should redirect to `/admin/login`
8. **While logged out**, try to POST to create coupon endpoint:
   ```bash
   curl -X POST http://localhost:3000/admin/coupon_codes
   ```
9. ✅ Should redirect or return 401/403
10. Open browser developer tools → Network tab
11. Log in as admin
12. Navigate to any admin page with a form
13. Inspect form HTML
14. ✅ Should see `authenticity_token` field (CSRF protection)
15. Try submitting form without token (disable JavaScript, remove field)
16. ✅ Should fail with CSRF error

**Pass Criteria**: All admin routes require authentication, CSRF protection enabled.

---

## Quick Smoke Test (5 minutes)

If time is limited, run this abbreviated test:

1. ✅ Log in with valid credentials
2. ✅ See dashboard with statistics
3. ✅ Create new coupon code (auto-generated, sequential)
4. ✅ Filter coupons by status
5. ✅ Delete unused coupon
6. ✅ View order list (newest first)
7. ✅ Search for order by customer name
8. ✅ View order details
9. ✅ Change password
10. ✅ Logout

**All green?** ✅ Core functionality works!

---

## Performance Check

### Database Queries (N+1 Prevention)

1. Enable query logging:
   ```ruby
   # config/environments/development.rb
   config.log_level = :debug
   ```

2. Restart server

3. Navigate to `/admin/orders`

4. Check logs for queries

5. ✅ Should see:
   - One query to load orders
   - One query to eager load fitness kits
   - One query to eager load coupon codes
   - NO additional queries per row

6. ✅ Should NOT see:
   - "SELECT * FROM promise_fitness_kits WHERE id = ?" repeated for each order
   - "SELECT * FROM coupon_codes WHERE id = ?" repeated for each order

**Expected Pattern**:
```
Order Load (0.5ms)  SELECT "orders".* FROM "orders" ORDER BY created_at DESC LIMIT 26
PromiseFitnessKit Load (0.3ms)  SELECT "promise_fitness_kits".* FROM "promise_fitness_kits" WHERE "promise_fitness_kits"."id" IN (?, ?, ?)
CouponCode Load (0.2ms)  SELECT "coupon_codes".* FROM "coupon_codes" WHERE "coupon_codes"."id" IN (?, ?, ?)
```

**Pass Criteria**: No N+1 queries detected.

---

## Mobile Responsiveness Check

1. Open admin dashboard in desktop browser
2. Open browser dev tools
3. Toggle device toolbar (mobile view)
4. ✅ Layout should adapt to mobile width
5. ✅ Tables should be scrollable or stack
6. ✅ Forms should be usable
7. ✅ Navigation should work (hamburger menu or stacked)
8. Test on actual mobile device if available
9. ✅ All functionality should work on touch screens

**Pass Criteria**: Admin interface is mobile-friendly.

---

## Browser Compatibility

Test in multiple browsers:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari (macOS/iOS)
- ✅ Edge

**Pass Criteria**: Works in all major browsers.

---

## Final Checklist

After running all scenarios:

- [ ] Authentication works (login/logout)
- [ ] Dashboard shows correct statistics
- [ ] Coupon codes auto-generate with correct format
- [ ] Coupon filtering and search work
- [ ] Unused coupons can be deleted
- [ ] Used coupons cannot be deleted
- [ ] Orders display newest first
- [ ] Order details show complete information
- [ ] Order search works for name, email, coupon
- [ ] Cursor pagination works correctly
- [ ] Pagination maintains filter/search state
- [ ] Password change works with validation
- [ ] Session persists after password change
- [ ] Unauthorized access blocked
- [ ] CSRF protection enabled
- [ ] No N+1 queries
- [ ] Mobile responsive
- [ ] Works in major browsers
- [ ] No JavaScript console errors

**All checked?** 🎉 **Admin dashboard is ready for use!**

---

## Troubleshooting

### Login doesn't work
- Check admin users exist: `rails console` → `Admin.all`
- Verify password: `Admin.find_by(username: 'admin').authenticate('password123')`
- Check session configuration in `config/application.rb`

### Coupon codes not generating
- Check model method: `CouponCode.generate_next_code`
- Verify seed data has correct format (SK[number][letters])
- Check database has at least one coupon to determine next number

### Pagination not working
- Verify indexes exist: `rails db:migrate:status`
- Check PER_PAGE constant in controllers
- Verify cursor parameter in URL

### No orders showing
- Run seeds: `rails db:seed`
- Check Order.count in console
- Verify associations: `Order.first.promise_fitness_kit`

### Password change fails
- Verify bcrypt gem installed: `bundle list | grep bcrypt`
- Check has_secure_password in Admin model
- Verify password_digest column exists

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-08  
**Feature**: 004-admin-dashboard