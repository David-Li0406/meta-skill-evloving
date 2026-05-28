# Pass Enhancement Techniques

Advanced techniques to extract maximum value from each of the 6 forced passes.

## Pass 1: Mental Model - Deep Dive

### Surfacing Hidden Assumptions

Ask these probing questions:
- "What would a first-time user expect to happen?"
- "What does a power user assume they can do?"
- "What terminology might confuse users from related products?"

### Mental Model Mapping

Create a comparison table:
```markdown
| Concept | User Expects | System Actually Does | Gap |
|---------|--------------|---------------------|-----|
| "Save" | Immediate persistence | Async with delay | Show saving indicator |
| "Delete" | Gone forever | Soft delete (recoverable) | Clarify in UI |
```

### Misconception Prevention Strategies

| Misconception Type | Prevention Strategy |
|--------------------|---------------------|
| Terminology confusion | Use common words, avoid jargon |
| Wrong scope assumption | Clear boundaries in first interaction |
| Missing capability belief | Feature discovery prompts |
| Overly powerful assumption | Explicit limitations shown |

### Example Output (Enhanced)

```markdown
## Pass 1: Mental Model

**Primary user intent:** Find and order food for delivery as quickly as possible.

**Likely misconceptions:**
1. "Adding to cart means I'm committed" → Reality: Cart is tentative, can modify freely
2. "Price shown is final" → Reality: Delivery fees and taxes added at checkout
3. "All items available" → Reality: Some items may be sold out

**UX principles to reinforce:**
- Cart is a staging area, not a commitment
- Price transparency: show "+" indicator for additional fees
- Real-time availability feedback before checkout

**Terminology audit:**
| Term We Use | User Might Think | Clarification Needed |
|-------------|------------------|----------------------|
| "Subtotal" | Final price | Label "Before fees" |
| "Reserve" | Guaranteed | "Subject to availability" |
```

## Pass 2: Information Architecture - Deep Dive

### Concept Enumeration Techniques

**Method 1: Noun extraction**
Read PRD, highlight every noun. Each noun is a potential concept.

**Method 2: User story inventory**
"As a [user], I need to see/manage/interact with [concept]"

**Method 3: Data entity mapping**
What entities exist in the database? Each maps to a user concept.

### Progressive Disclosure Planning

| Disclosure Level | Content Type | Trigger |
|------------------|--------------|---------|
| Immediate | Core actions, primary data | Page load |
| On demand | Secondary info, advanced actions | User click/hover |
| Contextual | Related content | User behavior pattern |
| Hidden | Admin/power features | Feature flag or role |

### IA Validation Questions

- "Can a user find X within 3 clicks?"
- "Are related concepts grouped together?"
- "Does the hierarchy match user mental model?"
- "Are labels self-explanatory?"

### Example Output (Enhanced)

```markdown
## Pass 2: Information Architecture

**All user-visible concepts:**
- Products (items for sale)
- Categories (product groupings)
- Cart (selected items)
- Order (submitted cart)
- Profile (user identity)
- Addresses (delivery locations)
- Payment methods (saved cards)

**Grouped structure:**

### Shopping (Primary)
- Products: Primary — core task
- Categories: Primary — navigation aid
- Cart: Primary — always accessible
- Search: Secondary — power user tool

### Account (Secondary)
- Profile: Secondary — infrequent access
- Addresses: Hidden — only during checkout
- Payment: Hidden — only during checkout
- Order History: Secondary — post-purchase

**Navigation structure:**
```
Home
├── Menu (products by category)
├── Cart (always visible count)
├── Search (icon, expands)
└── Account (dropdown)
    ├── Profile
    ├── Orders
    └── Settings
```

**IA validation:**
- Product → Cart: 1 click ✓
- Cart → Checkout: 1 click ✓
- Find past order: 2 clicks ✓
```

## Pass 3: Affordances - Deep Dive

### Affordance Audit Checklist

For each interactive element:
- [ ] Visual distinction from non-interactive elements
- [ ] Cursor change on hover (web)
- [ ] Touch target size (min 44x44px mobile)
- [ ] State changes visible (hover, active, disabled)
- [ ] Action predictable from appearance

### Signal-Action Mapping

| Visual Signal | Expected Action | Platform |
|---------------|-----------------|----------|
| Filled button | Primary action | All |
| Outlined button | Secondary action | All |
| Underlined text | Navigation link | Web |
| Chevron (>) | Expand/navigate | All |
| X icon | Close/dismiss | All |
| Drag handle (⋮⋮) | Reorderable | All |

### Affordance Conflicts to Avoid

| Conflict | Problem | Solution |
|----------|---------|----------|
| Link looks like button | Unclear if navigation or action | Consistent styling |
| Disabled looks clickable | Frustrating failed clicks | Obvious disabled state |
| Read-only looks editable | Users try to edit | Input field styling differs |
| Clickable looks static | Features undiscovered | Hover states, icons |

### Example Output (Enhanced)

```markdown
## Pass 3: Affordances

| Element | Action | Visual Signal | Touch Target |
|---------|--------|---------------|--------------|
| Product card | Open details | Card lift on hover, pointer cursor | Full card 100% |
| Add to cart | Add item | Filled button, + icon | 44x44px min |
| Quantity stepper | Adjust amount | +/- buttons, number display | Each button 44px |
| Cart icon | Open cart | Badge with count, pointer | 48x48px |
| Category tab | Filter products | Underline active, pointer | Full tab width |

**Affordance rules:**
- If element has hover state → it's clickable
- If element shows count badge → tapping shows list
- If element has chevron → it expands or navigates
- If input has border → it's editable
- If input has no border, gray bg → it's read-only

**State indicators:**
| State | Visual Treatment |
|-------|------------------|
| Clickable | Cursor pointer, slight lift on hover |
| Disabled | 50% opacity, cursor not-allowed |
| Loading | Spinner replaces action icon |
| Selected | Filled background, checkmark |
```

## Pass 4: Cognitive Load - Deep Dive

### Friction Point Classification

| Type | Symptom | Reduction Strategy |
|------|---------|-------------------|
| Choice overload | Too many options | Progressive disclosure, smart defaults |
| Information overload | Too much text | Chunking, visual hierarchy |
| Memory burden | Must remember from prev screen | Persistent context, summaries |
| Process uncertainty | Don't know how many steps | Progress indicators |
| Error anxiety | Fear of mistakes | Undo support, confirmations |

### Decision Reduction Techniques

1. **Smart defaults**: Pre-select most common choice
2. **Recommendations**: Suggest based on context
3. **Elimination**: Remove rarely-used options
4. **Chunking**: Break into smaller decisions
5. **Comparison tools**: Help evaluate options

### Waiting Anxiety Management

| Wait Duration | User Expectation | Feedback Strategy |
|---------------|------------------|-------------------|
| < 100ms | Instant | None needed |
| 100-1000ms | Brief delay | Subtle indicator |
| 1-5 seconds | Noticeable | Spinner or skeleton |
| 5-30 seconds | Long | Progress bar + context |
| > 30 seconds | Very long | Estimated time + background option |

### Example Output (Enhanced)

```markdown
## Pass 4: Cognitive Load

**Friction points:**

| Moment | Type | Current Friction | Simplification |
|--------|------|------------------|----------------|
| Category selection | Choice | 8 categories visible | Show 4 + "More" |
| Address entry | Information | Full form visible | Autocomplete first |
| Payment selection | Choice | All cards shown | Default selected |
| Checkout review | Memory | Must recall items | Show mini-cart |
| Order placement | Anxiety | Fear of mistake | Show confirmation |

**Defaults introduced:**
- Default address: Most recently used
- Default payment: Last successful card
- Default category: "Popular" or last browsed
- Default quantity: 1

**Progressive disclosure:**
| Initially Hidden | Shown When |
|------------------|------------|
| Delivery instructions | Address selected |
| Promo code field | Tap "Have a code?" |
| Item customization | Tap "Customize" |
| Order history details | Tap order card |

**Memory aids:**
- Persistent cart icon with count
- "Continue where you left off" banner
- Recently viewed items section
```

## Pass 5: State Design - Deep Dive

### State Matrix Template

For critical screens, use the full matrix:

```markdown
| State | Visual | Message | Primary Action | Secondary Action |
|-------|--------|---------|----------------|------------------|
| Empty | Illustration | "No items yet" | "Browse Menu" | - |
| Loading | Skeleton | - | - | - |
| Partial | List + skeleton | "Loading more..." | Scroll | - |
| Success | Full list | - | Interact with items | Refresh |
| Error | Error icon | "Couldn't load" | "Try Again" | "Contact Support" |
| Offline | Offline icon | "No connection" | - | "Retry when online" |
```

### Transition Design

| From State | To State | Transition | Duration |
|------------|----------|------------|----------|
| Empty → Loading | Fade in skeleton | 150ms |
| Loading → Success | Crossfade | 300ms |
| Loading → Error | Slide + shake | 200ms |
| Success → Updating | Pulse overlay | Ongoing |
| Any → Empty | Fade + collapse | 200ms |

### Success Feedback Patterns

**The 300ms rule:** Users must SEE success before UI transitions.

```
Action → Success indicator (300-500ms) → Next state
```

| Action Type | Success Feedback |
|-------------|------------------|
| Add to cart | Checkmark animation + count update |
| Remove item | Slide out + count update |
| Save changes | "Saved" toast or inline checkmark |
| Submit form | Success screen or redirect |
| Delete | Confirmation + item removal |

### Example Output (Enhanced)

```markdown
## Pass 5: State Design

### Cart

| State | User Sees | User Understands | User Can Do |
|-------|-----------|------------------|-------------|
| Empty | Illustration + "Your cart is empty" | No items selected | Browse menu |
| Loading | Skeleton cards | Cart is loading | Wait |
| Items | Product cards with qty/price | What's in cart, total | Adjust qty, remove, checkout |
| Updating | Item + subtle spinner | Change being saved | Wait briefly |
| Error | Error banner | Something failed | Retry or contact support |

### Add to Cart Action

| Stage | Visual | Duration | Next |
|-------|--------|----------|------|
| Tap | Button depresses | 50ms | Processing |
| Processing | Spinner in button | 200-500ms | Success/Error |
| Success | Checkmark, cart count bumps | 400ms | Return to idle |
| Error | Shake, error message | 300ms + persist | Show error |

### Order Submission

| Stage | Screen | User Action |
|-------|--------|-------------|
| Review | Order summary | Confirm or edit |
| Processing | Full-screen loader | Wait |
| Success | Confirmation with order ID | View order or return home |
| Payment Failed | Error with retry option | Try different card |
| System Error | Error with support contact | Contact support |
```

## Pass 6: Flow Integrity - Deep Dive

### Risk Identification Framework

| Risk Category | Questions to Ask |
|---------------|------------------|
| Entry | How do users arrive? Is context preserved? |
| Progress | Can users tell where they are? |
| Exit | Can users leave safely? Is data preserved? |
| Recovery | Can users fix mistakes? |
| Edge cases | What if they do something unexpected? |

### Guardrail Patterns

| Risk | Guardrail | Implementation |
|------|-----------|----------------|
| Data loss | Auto-save | Save on blur, periodic save |
| Wrong action | Confirmation | Modal for destructive actions |
| Lost progress | Breadcrumbs | Clickable path history |
| Stuck state | Escape hatch | Always-visible cancel/back |
| Invalid input | Inline validation | Real-time feedback |

### First-Time User Test

Mentally walk through as a new user:
1. What do they see first?
2. What's the obvious action?
3. Can they complete core task without help?
4. What would confuse them?
5. How would they recover from a mistake?

### Example Output (Enhanced)

```markdown
## Pass 6: Flow Integrity

**Flow risks:**

| Risk | Location | Impact | Mitigation |
|------|----------|--------|------------|
| Cart abandonment | Cart → Checkout transition | Lost sale | Persistent cart, "Continue" prompt |
| Address entry friction | Checkout form | Dropout | Autocomplete, save addresses |
| Payment failure | Checkout submit | Frustration | Clear error, easy retry |
| Order status unknown | Post-checkout | Anxiety | Confirmation email + tracking |
| Session timeout | Any long form | Data loss | Auto-save + warning |

**Visibility decisions:**

Must be visible always:
- Cart item count
- Current total
- Navigation to account/help
- Back/cancel options

Can be implied/hidden:
- Detailed nutritional info
- Order history beyond recent
- Advanced account settings
- Promotional content (non-blocking)

**UX constraints for visual phase:**
1. Cart icon must show count badge when items > 0
2. Primary CTA must be visually distinct from secondary
3. Error states must not block all interaction
4. Loading states must not exceed 3 seconds without progress
5. Confirmation screens must have clear next action
```
