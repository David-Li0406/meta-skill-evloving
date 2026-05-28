# Example: Writing User Stories

## 📝 Prompt

```
Write user stories with acceptance criteria for a "Save for Later" feature in an e-commerce app.

Context:
- Users want to bookmark products without adding to cart
- Business goal: Increase conversion rate
- Technical: React frontend, REST API backend
- Users can be logged in or guest

Include:
- User stories (As a... I want... So that...)
- Acceptance criteria (Given/When/Then)
- Edge cases
- Technical considerations
- Priority and effort estimates
```

## ✅ Example Output

# User Stories: Save for Later Feature

## Epic
**As a shopper**, I want to save products for later review, so that I can make better purchasing decisions without losing track of items I'm interested in.

---

## Story 1: Save Product for Later (Logged-in User)

**Priority**: P0 (Must Have)  
**Effort**: 5 Story Points  
**Sprint**: Sprint 23

### User Story
```
As a logged-in user
I want to save products to a "Save for Later" list
So that I can review them later without adding them to my cart
```

### Acceptance Criteria

**AC1: Save Product from Product Detail Page**
```gherkin
Given I am logged in
And I am viewing a product detail page
When I click the "Save for Later" button
Then the product is added to my saved list
And I see a success message "Product saved"
And the button changes to "Saved" with a checkmark icon
```

**AC2: Saved Products Persist Across Sessions**
```gherkin
Given I have saved products in my list
When I log out and log back in
Then I see all my saved products in the list
```

**AC3: View Saved Products**
```gherkin
Given I have saved products
When I navigate to "Saved Items" from the user menu
Then I see a list of all saved products with:
  - Product image
  - Product name
  - Current price
  - Save date
  - "Add to Cart" button
  - "Remove" button
```

**AC4: Remove from Saved List**
```gherkin
Given I am viewing my saved items
When I click "Remove" on a saved product
Then the product is removed from the list
And I see a message "Product removed from saved items"
```

**AC5: Add Saved Product to Cart**
```gherkin
Given I am viewing my saved items
When I click "Add to Cart" on a saved product
Then the product is added to my cart
And the product remains in my saved list
And I see a message "Added to cart"
```

### Edge Cases

1. **Product No Longer Available**
   - Show "Out of Stock" badge
   - Disable "Add to Cart" button
   - Allow removal from saved list

2. **Price Changed**
   - Show price change indicator (up/down arrow)
   - Display old vs new price

3. **Product Deleted**
   - Remove from saved list automatically
   - Don't show error to user

4. **Maximum Saved Items**
   - Limit: 100 items per user
   - Show warning at 90 items
   - Prevent saving beyond limit with message

### Technical Considerations

**API Endpoints:**
```
POST   /api/v1/users/{userId}/saved-items
GET    /api/v1/users/{userId}/saved-items
DELETE /api/v1/users/{userId}/saved-items/{itemId}
```

**Database Schema:**
```sql
CREATE TABLE saved_items (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  product_id UUID NOT NULL,
  saved_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, product_id)
);
```

**Frontend Components:**
- `SaveForLaterButton` (product detail page)
- `SavedItemsList` (saved items page)
- `SavedItemCard` (individual item)

### Definition of Done
- [ ] Backend API endpoints implemented and tested
- [ ] Frontend components implemented
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests pass
- [ ] Accessibility tested (WCAG AA)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Product Owner approval

---

## Story 2: Save Product for Later (Guest User)

**Priority**: P1 (Should Have)  
**Effort**: 3 Story Points  
**Sprint**: Sprint 23

### User Story
```
As a guest user
I want to save products temporarily
So that I can keep track of interesting items during my browsing session
```

### Acceptance Criteria

**AC1: Guest Can Save Products**
```gherkin
Given I am not logged in
And I am viewing a product detail page
When I click "Save for Later"
Then the product is saved to browser localStorage
And I see a success message with "Sign in to save permanently"
```

**AC2: View Guest Saved Items**
```gherkin
Given I am a guest with saved items
When I navigate to "Saved Items"
Then I see my saved products
And I see a banner "Sign in to save your items permanently"
```

**AC3: Convert Guest Saves on Login**
```gherkin
Given I am a guest with 5 saved items
When I log in or create an account
Then all my saved items are transferred to my account
And I see a message "5 items saved to your account"
```

**AC4: Guest Saves Expire**
```gherkin
Given I saved items as a guest 30 days ago
When I return to the site
Then those items are no longer in my saved list
And I see no error message
```

### Edge Cases

1. **localStorage Full**
   - Show error: "Unable to save. Try logging in."
   - Suggest creating account

2. **Browser Cookies Disabled**
   - Show message: "Enable cookies to save items"
   - Offer email reminder option

3. **Guest Saves + Existing Account Saves**
   - Merge both lists without duplicates
   - Show count: "X new items saved"

### Technical Considerations

**localStorage Schema:**
```json
{
  "savedItems": [
    {
      "productId": "prod-123",
      "savedAt": "2026-01-20T10:00:00Z"
    }
  ],
  "expiresAt": "2026-02-19T10:00:00Z"
}
```

**Migration Logic:**
- On login, POST all guest items to API
- Clear localStorage after successful migration
- Handle duplicates (user might have saved same item)

### Definition of Done
- [ ] localStorage implementation complete
- [ ] Guest-to-user migration working
- [ ] Expiration logic implemented
- [ ] Unit tests (>80% coverage)
- [ ] Cross-browser testing complete
- [ ] Privacy policy updated
- [ ] Product Owner approval

---

## Story 3: Email Reminder for Saved Items

**Priority**: P2 (Nice to Have)  
**Effort**: 5 Story Points  
**Sprint**: Sprint 24

### User Story
```
As a logged-in user with saved items
I want to receive email reminders about my saved products
So that I don't forget about items I was interested in
```

### Acceptance Criteria

**AC1: Opt-in to Email Reminders**
```gherkin
Given I have saved items
When I visit my saved items page
Then I see an option "Email me about price drops and restocks"
And it is unchecked by default
```

**AC2: Receive Price Drop Notification**
```gherkin
Given I have opted in to email reminders
And a saved product's price drops by >10%
When the price check job runs
Then I receive an email within 1 hour with:
  - Product name and image
  - Old price vs new price
  - Savings amount
  - "Add to Cart" button
```

**AC3: Receive Restock Notification**
```gherkin
Given I have opted in to email reminders
And a saved out-of-stock product comes back in stock
When the inventory check job runs
Then I receive an email within 1 hour
```

**AC4: Unsubscribe from Reminders**
```gherkin
Given I receive reminder emails
When I click "Unsubscribe" in the email
Then I am unsubscribed from all saved item notifications
And I see confirmation message
```

### Edge Cases

1. **Multiple Price Drops in One Day**
   - Send only one daily digest
   - List all products with price drops

2. **User Has Many Saved Items**
   - Limit email to top 5 price drops
   - Include link to see all changes

3. **Email Delivery Failure**
   - Retry 3 times
   - Log failure for monitoring
   - Don't remove preference

### Technical Considerations

**Scheduled Jobs:**
```
- Price check: Every 4 hours
- Stock check: Every 2 hours
- Email sending: Batched, max 1000/minute
```

**Email Template:**
- Responsive HTML email
- Plain text fallback
- UTM parameters for tracking

**Notification Preferences Table:**
```sql
CREATE TABLE notification_preferences (
  user_id UUID PRIMARY KEY,
  email_enabled BOOLEAN DEFAULT false,
  email_frequency VARCHAR(20) DEFAULT 'instant',
  last_email_sent_at TIMESTAMP
);
```

### Acceptance Criteria - Email Content

**Email should include:**
- Subject: "💰 Price drop on [ProductName]"
- Hero image of product
- Clear price comparison
- Call to action button
- Unsubscribe link (required by law)

### Definition of Done
- [ ] Email template designed and approved
- [ ] Background jobs implemented
- [ ] Email sending service integrated
- [ ] Unsubscribe mechanism working
- [ ] Email deliverability tested
- [ ] GDPR compliance verified
- [ ] Analytics tracking added
- [ ] Product Owner approval

---

## Story 4: Analytics for Saved Items

**Priority**: P3 (Metrics/Learning)  
**Effort**: 2 Story Points  
**Sprint**: Sprint 24

### User Story
```
As a product manager
I want to track saved items metrics
So that I can understand user behavior and optimize the feature
```

### Acceptance Criteria

**AC1: Track Save Events**
```gherkin
Given a user saves a product
When the save action completes
Then an analytics event is sent with:
  - Event: "product_saved"
  - User ID
  - Product ID
  - Source (detail page, search results, etc.)
  - Timestamp
```

**AC2: Track Conversion from Saved Items**
```gherkin
Given a user adds a saved product to cart
When the action completes
Then an analytics event is sent with:
  - Event: "saved_item_purchased"
  - Time from save to purchase
  - Price at save vs price at purchase
```

**AC3: Dashboard Metrics**
```gherkin
Given I am viewing the analytics dashboard
When I navigate to "Save for Later" section
Then I see:
  - Total saved items
  - Save-to-purchase conversion rate
  - Average time from save to purchase
  - Most saved products
  - Save-to-cart rate
```

### Technical Considerations

**Analytics Events:**
```javascript
analytics.track('product_saved', {
  userId: '123',
  productId: '456',
  productName: 'Laptop',
  productPrice: 999.99,
  source: 'product_detail',
  timestamp: '2026-01-20T10:00:00Z'
});
```

**Metrics to Track:**
- Daily active users using saved items
- Saved items per user (P50, P90, P99)
- Conversion rate: saved → cart → purchase
- Time to purchase from save
- Most saved categories

### Definition of Done
- [ ] Analytics events implemented
- [ ] Dashboard queries optimized
- [ ] Data pipeline tested
- [ ] Privacy review completed
- [ ] Documentation updated
- [ ] Product Owner approval

---

## Summary

| Story | Priority | Effort | Dependencies |
|-------|----------|--------|--------------|
| 1. Save Product (Logged-in) | P0 | 5 | None |
| 2. Save Product (Guest) | P1 | 3 | Story 1 |
| 3. Email Reminders | P2 | 5 | Story 1 |
| 4. Analytics | P3 | 2 | Story 1 |

**Total Effort**: 15 Story Points  
**Estimated Completion**: 2 Sprints (4 weeks)

## Success Metrics

**Key Performance Indicators:**
- 30% of users save at least one product (30 days post-launch)
- 20% conversion rate from saved items to cart
- 5% increase in overall purchase conversion
- 50% of saved items result in purchase within 30 days

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low adoption | High | A/B test prominent placement |
| Performance issues | Medium | Implement caching, pagination |
| Privacy concerns | High | Clear messaging, GDPR compliance |
| Email spam complaints | Medium | Easy unsubscribe, frequency controls |
