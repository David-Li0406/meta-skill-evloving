# Example: Flow/Page Prompt

A complete, self-contained prompt for a multi-step user flow.

---

## Checkout Flow

### Context
The checkout flow where authenticated users complete their purchase. Accessed from the cart (via "Checkout" button). Users review their order, select delivery address, choose payment method, and confirm purchase.

**User state when entering:**
- Authenticated (redirected to login if not)
- Has at least 1 item in cart
- Cart validated (items in stock, prices current)

**Flow exits:**
- Success: Order confirmation page
- Cancel: Return to cart
- Error: Error state with retry/support options

### Flow Structure

```
Cart → [Checkout Button]
           ↓
    ┌─────────────────┐
    │ 1. Review Order │ ← Shows cart summary
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 2. Delivery     │ ← Select/add address
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 3. Payment      │ ← Select/add payment
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 4. Confirm      │ ← Final review + place order
    └────────┬────────┘
             ↓
    ┌─────────────────┐
    │ 5. Success      │ ← Order confirmation
    └─────────────────┘
```

### Page Layout

**Desktop (>1024px):**
```
┌────────────────────────────────────────────────────┐
│ [← Back to Cart]              Checkout    Step 1/4 │
├─────────────────────────────────┬──────────────────┤
│                                 │                  │
│   [Step Content]                │  Order Summary   │
│                                 │  ────────────    │
│   Form fields, selections,      │  Item 1    $XX   │
│   options for current step      │  Item 2    $XX   │
│                                 │  ────────────    │
│                                 │  Subtotal  $XX   │
│                                 │  Delivery  $XX   │
│                                 │  Tax       $XX   │
│                                 │  ────────────    │
│                                 │  Total    $XXX   │
│                                 │                  │
├─────────────────────────────────┴──────────────────┤
│                    [Continue]                      │
└────────────────────────────────────────────────────┘
```

**Mobile (<640px):**
```
┌─────────────────────────────────┐
│ [←]  Checkout           1 of 4  │
├─────────────────────────────────┤
│                                 │
│   [Step Content]                │
│                                 │
│   Vertically stacked            │
│   form fields                   │
│                                 │
├─────────────────────────────────┤
│ Summary (collapsible)    [$XXX] │
├─────────────────────────────────┤
│         [Continue]              │
└─────────────────────────────────┘
```

### Step 1: Review Order

**Content:**
- List of cart items with:
  - Product image (48x48px)
  - Name
  - Quantity (editable)
  - Price
  - Remove button
- Promo code input (expandable)
- Continue button

**States:**
| State | Content | Actions |
|-------|---------|---------|
| Default | Cart items listed | Edit qty, remove, continue |
| Updating | Item shows spinner | Wait |
| Promo applied | Discount shown | Remove promo |
| Promo invalid | Error message | Try again |
| Item removed | Item slides out | Undo (5s) |
| Cart empty | Empty state | Return to shop |

### Step 2: Delivery Address

**Content:**
- Saved addresses (radio list)
- "Add new address" option
- Address form (when adding):
  - Full name
  - Street address
  - Apartment/suite (optional)
  - City
  - State/Province
  - Postal code
  - Phone number
- Delivery instructions (optional textarea)

**States:**
| State | Content | Actions |
|-------|---------|---------|
| Has addresses | Radio list + "Add new" | Select, edit, add |
| No addresses | Add form immediately | Fill form |
| Adding | Form visible | Submit or cancel |
| Saving | Form disabled, spinner | Wait |
| Save error | Error message | Retry |

**Validation:**
- Required: Name, street, city, state, postal, phone
- Phone: Valid format
- Postal: Valid for selected country

### Step 3: Payment Method

**Content:**
- Saved cards (radio list) showing:
  - Card brand icon
  - Last 4 digits
  - Expiry
- "Add new card" option
- Card form (when adding):
  - Card number
  - Expiry (MM/YY)
  - CVC
  - Name on card
  - "Save for future" checkbox

**States:**
| State | Content | Actions |
|-------|---------|---------|
| Has cards | Radio list + "Add new" | Select, add |
| No cards | Add form immediately | Fill form |
| Adding | Stripe Elements form | Submit or cancel |
| Validating | Form disabled | Wait |
| Card error | Specific error message | Fix and retry |

**Security:**
- Card input via Stripe Elements (PCI compliant)
- CVC not stored
- Show security badge

### Step 4: Confirm & Place Order

**Content:**
- Order summary (all items)
- Delivery address (with "Change" link)
- Payment method (with "Change" link)
- Order total breakdown
- Terms checkbox
- "Place Order" button

**States:**
| State | Content | Actions |
|-------|---------|---------|
| Ready | All info shown | Review and place |
| Processing | Full-screen loader | Wait |
| Success | Redirect to confirmation | - |
| Payment failed | Error + options | Retry or change card |
| Stock error | Affected items shown | Remove items or cancel |
| Server error | Generic error | Retry or contact support |

### Step 5: Order Confirmation

**Content:**
- Success illustration
- "Thank you for your order!"
- Order number
- Estimated delivery date
- Order details (collapsible)
- "Continue Shopping" button
- "View Order" button

**Actions:**
- Email confirmation sent
- Order tracking available

### Interactions

**Navigation:**
- Progress indicator clickable for completed steps
- Back button goes to previous step
- Browser back works correctly
- Direct URL to step redirects to step 1 if state missing

**Persistence:**
- Form data persisted in session
- Survives page refresh within session
- Cleared on order completion

**Keyboard:**
- Tab through fields
- Enter to submit (when valid)
- Escape to close modals

### Error Handling

| Error | Where | Treatment | Recovery |
|-------|-------|-----------|----------|
| Session expired | Any step | Modal | Re-login (preserve cart) |
| Network error | Any step | Toast + retry | Manual retry |
| Validation error | Form fields | Inline errors | Fix and retry |
| Payment declined | Step 3/4 | Modal | Try different card |
| Item out of stock | Step 4 | Blocking modal | Remove item |
| Price changed | Step 1/4 | Notification | Continue or cancel |

### Animations

**Step transitions:**
- Current step slides left
- New step slides in from right
- Duration: 300ms
- Easing: ease-out

**Progress indicator:**
- Step completion: checkmark draws in (200ms)
- Active step: pulse ring (subtle, continuous)

**Place order:**
- Button → spinner (immediate)
- Success → confetti (500ms)
- Error → shake (200ms)

**Reduced motion:**
- Steps crossfade (instant)
- No confetti
- No shake

### Constraints

**This prompt includes:**
- All 5 steps UI
- Form validation
- State management within flow
- Error handling
- Animations
- Mobile responsive

**This prompt does NOT include:**
- Actual payment processing (mock/stub)
- Email sending
- Order database operations
- Inventory management
- Shipping rate calculations
- Tax calculations

### Verification

- [ ] Happy path E2E test passes:
  - [ ] Add item to cart
  - [ ] Start checkout
  - [ ] Select address
  - [ ] Select payment
  - [ ] Place order
  - [ ] See confirmation
- [ ] Error states tested:
  - [ ] Payment decline
  - [ ] Network failure
  - [ ] Stock change
  - [ ] Session expiration
- [ ] Form validation works
- [ ] Mobile layout correct
- [ ] Tablet layout correct
- [ ] Desktop layout correct
- [ ] Light theme verified
- [ ] Dark theme verified
- [ ] Keyboard navigation complete
- [ ] Screen reader flow logical
- [ ] Browser back button works
- [ ] Page refresh preserves state
