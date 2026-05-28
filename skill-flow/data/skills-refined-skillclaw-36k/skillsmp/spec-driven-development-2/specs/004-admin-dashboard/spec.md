# Spec 004: Admin Dashboard

## Overview
Create a secure admin dashboard that allows authorized administrators to manage coupon codes and view order records. The admin area must be protected from public access and provide essential administrative functions for the PromiseKits platform.

## User Stories

### As an Administrator
1. **Access Control**
   - I need to authenticate with a username and password to access the admin dashboard
   - I should be automatically redirected to login if I try to access admin pages without authentication
   - I should see a clear indication that I'm in the admin area (different header/styling)
   - I should be able to log out and return to the public site

2. **Coupon Code Management**
   - I can view a list of all coupon codes with their status (unused/used)
   - I can create new coupon codes (system auto-generates in format SK[integer][3letters])
   - I can delete unused coupon codes
   - I can see which coupon code is associated with which order (if used)
   - I can filter coupon codes by status (all/unused/used)
   - I can search for specific coupon codes by code text
   - Coupon codes follow format: SK + sequential integer + 3 random uppercase letters (e.g., SK187524MYQ)

3. **Order Management**
   - I can view a list of all orders (newest first, with cursor-based pagination)
   - I can search orders by customer name, email, or coupon code
   - I can view full order details including:
     - Customer information (name, address, phone, email)
     - Fitness kit ordered
     - Coupon code used
     - Order date/time
     - Any special delivery instructions
   - I can see order statistics (total orders, orders by kit type)

4. **Account Management**
   - I can change my own password while logged in
   - I can see my current username
   - Password changes require current password confirmation

### As the System
1. **Security**
   - Admin routes should not be accessible without authentication
   - Admin credentials should be stored securely
   - Failed login attempts should be logged
   - Sessions should expire after inactivity

2. **Data Integrity**
   - Coupon code changes should maintain referential integrity with existing orders
   - Deleting coupon codes that are associated with orders should be prevented
   - Editing a coupon code should update the code text but maintain the association with orders

## Acceptance Criteria

### Authentication
- [ ] Admin login page exists at `/admin/login`
- [ ] Unauthenticated users accessing `/admin/*` routes are redirected to login
- [ ] Valid credentials grant access to admin dashboard
- [ ] Invalid credentials show error message and remain on login page
- [ ] Logout functionality returns to public homepage
- [ ] Admin session persists across requests until logout

### Coupon Code Management
- [ ] Admin can view list of all coupon codes at `/admin/coupon_codes` (with cursor-based pagination)
- [ ] Coupon code list shows: code, status (unused/used), associated order ID (if used)
- [ ] Admin can create new coupon code (system auto-generates code)
- [ ] New coupon codes follow format: SK[sequential_integer][3_random_letters]
- [ ] System finds highest existing integer and increments by 1 for new codes
- [ ] New coupon codes default to 'unused' status
- [ ] Admin can delete unused coupon codes
- [ ] Cannot delete coupon codes associated with orders (show error message)
- [ ] Coupon code validation ensures format compliance
- [ ] Filter by status works correctly (all/unused/used)
- [ ] Search by code text returns matching results
- [ ] Pagination uses cursor-based approach for performance

### Order Management
- [ ] Admin can view list of all orders at `/admin/orders` (newest first)
- [ ] Order list uses cursor-based pagination for performance
- [ ] Order list shows: order ID, customer name, kit name, coupon code, order date
- [ ] Orders are sorted by created_at descending (newest first)
- [ ] Admin can view individual order details at `/admin/orders/:id`
- [ ] Order detail page shows complete customer and order information
- [ ] Search functionality works for customer name, email, and coupon code
- [ ] Dashboard shows summary statistics (total orders, breakdown by kit)

### Account Management
- [ ] Admin can change own password at `/admin/account/password`
- [ ] Password change requires current password confirmation
- [ ] New password must meet minimum security requirements
- [ ] Success message shown after password change
- [ ] Admin remains logged in after password change

### User Experience
- [ ] Admin area has distinct visual identity (different header/nav)
- [ ] Forms have proper validation with error messages
- [ ] Success messages appear after create/update/delete actions
- [ ] Navigation between admin sections is intuitive
- [ ] Mobile-responsive design for admin pages

### Security
- [ ] Admin credentials stored securely (hashed password with bcrypt)
- [ ] CSRF protection enabled on all admin forms
- [ ] Admin routes require authentication (before_action)
- [ ] Non-admin users cannot access admin area
- [ ] Session timeout after 12 hours of inactivity

## Data Requirements

### Admin Users
- Username (unique, required)
- Password (hashed, required)
- Email (optional, for password reset future feature)
- Created at timestamp
- Updated at timestamp

### Existing Models (Reference)
- **CouponCode**: code (string), usage (enum: unused/used)
- **Order**: Multiple fields including coupon_code_id foreign key
- **PromiseFitnessKit**: name, description, slug

## Workflows

### Admin Login Workflow
1. Admin visits `/admin` or any `/admin/*` route
2. System checks for active admin session
3. If not authenticated, redirect to `/admin/login`
4. Admin enters username and password
5. System validates credentials
6. On success: Create session, redirect to `/admin/dashboard`
7. On failure: Show error, remain on login page

### Create Coupon Code Workflow
1. Admin navigates to `/admin/coupon_codes`
2. Clicks "New Coupon Code" button
3. System auto-generates code in format SK[integer][3letters]:
   - Queries database for highest integer in existing codes
   - Increments by 1 (e.g., if highest is SK187524MYQ, next is SK187525...)
   - Generates 3 random uppercase letters (e.g., XNB)
   - Creates code like SK187525XNB
4. Submits form (or auto-creates)
5. System validates:
   - Code follows format SK[integer][3letters]
   - Code is unique (should always be due to sequential integers)
6. On success: Create coupon with 'unused' status, redirect to list, show success message
7. On failure: Show validation errors

### Delete Unused Coupon Code Workflow
1. Admin navigates to coupon code list
2. Clicks "Delete" button for an unused coupon code
3. System checks if coupon is associated with any orders
4. If unused: Delete coupon, redirect to list, show success message
5. If used: Prevent deletion, show error message "Cannot delete coupon code associated with orders"

### View Order Details Workflow
1. Admin navigates to `/admin/orders`
2. Clicks on an order row or order ID
3. System loads order details page
4. Page displays:
   - Order ID and timestamp
   - Customer: name, email, phone, full address
   - Fitness kit: name and description
   - Coupon code used
   - Special instructions (if any)
5. Admin can navigate back to order list

### Search Orders Workflow
1. Admin on `/admin/orders` page
2. Enters search term in search box (name, email, or coupon code)
3. Submits search
4. System filters orders matching search term
5. Results display in same list format with cursor pagination
6. Admin can clear search to see all orders

### Change Password Workflow
1. Admin navigates to `/admin/account/password`
2. Form shows fields: current password, new password, confirm new password
3. Admin fills in all fields
4. Submits form
5. System validates:
   - Current password is correct
   - New password meets requirements (min 8 characters)
   - New password and confirmation match
6. On success: Update password hash, show success message, remain logged in
7. On failure: Show validation errors, remain on form

## Edge Cases

### Authentication Edge Cases
- User tries to access admin without session → redirect to login
- User enters wrong password 5 times → (future: account lockout, for now just show error)
- Session expires (after 12 hours) while viewing admin page → redirect to login on next action
- User tries to access `/admin/login` while already authenticated → redirect to dashboard
- Admin changes password with incorrect current password → show validation error

### Coupon Code Edge Cases
- System generates duplicate code (extremely unlikely) → retry generation with different random letters
- Delete coupon that's associated with order → prevent deletion, show error message "Cannot delete used coupon"
- Delete unused coupon successfully → show success message, remove from list
- First coupon code creation (no existing codes) → start sequence at SK1000AAA
- Search with no matches → show "No results found" message
- Filter shows empty list (e.g., no unused coupons) → show "No coupons found" message
- Cursor pagination at end of list → disable "Next" button
- Cursor pagination at beginning of list → disable "Previous" button

### Order Edge Cases
- View order list with no orders → show "No orders yet" message
- Search returns no results → show "No orders found" message
- View order with missing coupon code (data integrity issue) → handle gracefully, show "No coupon code"
- Order has no special instructions → display field as empty/N/A

## Sample Data

### Admin Users (for development)
- Username: `admin`, Password: `password123` (will be hashed with bcrypt)
- Username: `testadmin`, Password: `testpass` (will be hashed with bcrypt)

### Coupon Codes (need to update seeds to new format)
- Replace existing codes with new format:
  - SK1000AAA (unused)
  - SK1001BBB (unused)
  - SK1002CCC (unused)
  - SK1003DDD (used - order #1)
  - SK1004EEE (used - order #2)
  - SK1005FFF (used - order #3)
  - SK1006GGG (used)
  - SK1007HHH (used)

### Orders (already exist in seeds)
- 3 sample orders with customer data

## Success Metrics
- Admin can log in successfully
- Admin can create, view, edit coupon codes
- Admin can view and search orders
- No unauthorized access to admin area
- All CRUD operations work without errors
- Mobile-friendly admin interface

## Out of Scope (Future Features)
- Password reset functionality
- Multiple admin roles (super admin vs. regular admin)
- Email notifications to admins
- Export orders to CSV
- Bulk coupon code creation (generate N codes at once)
- Order fulfillment status tracking
- Analytics dashboard with charts
- Admin activity audit log (who created/modified what)
- Two-factor authentication
- Forgot password / password reset via email
- Admin user management (create/edit/delete other admins)

## Clarifications Resolved

1. ✅ **Coupon Code Deletion**: Admins CAN delete unused coupon codes. Cannot delete used codes.
2. ✅ **Password Management**: Admins CAN change their own passwords (requires current password confirmation).
3. ✅ **Admin Attribution**: NOT tracking which admin created/modified coupon codes.
4. ✅ **Coupon Code Format**: SK + sequential integer + 3 random uppercase letters
   - Example: SK187524MYQ, SK187525XNB, SK187526KHK
   - Integer increments sequentially (187524, 187525, 187526...)
   - 3 letters are random uppercase A-Z
   - Total length: 11 characters (SK + up to 6 digits + 3 letters)
5. ✅ **Order Sorting**: Newest first (descending by created_at)
6. ✅ **Pagination**: Cursor-based pagination for both orders and coupon codes
7. ✅ **Session Duration**: 12 hours of inactivity before timeout

---

**Feature ID**: 004  
**Feature Name**: Admin Dashboard  
**Status**: Specification Draft  
**Created**: 2025-01-08  
**Priority**: High  
**Dependencies**: Existing Order, CouponCode, PromiseFitnessKit models