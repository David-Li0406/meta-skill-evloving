# Conversion Patterns and Anti-Patterns

## How to Use This Reference

These are documented patterns from thousands of conversion tests. Patterns = things that consistently work. Anti-patterns = things that consistently fail. Use these to quickly identify issues during audits.

---

## Homepage Patterns

### Pattern: Clear Value Proposition Above Fold

**What Works:**
```
[Logo]                                    [Nav]

   THE HEADLINE STATES THE BENEFIT
   Subheadline explains who it's for and what they get
   
   [Primary CTA]  [Secondary CTA]
   
   Trust signal (logos, review stars, "Trusted by X")
```

**Why It Works:**
- Visitor knows what you do in <5 seconds
- Clear action to take
- Trust established immediately
- Works for all awareness levels

**Anti-Pattern: The Mystery Homepage**
```
[Logo]                                    [Nav]

   Welcome to Our Company
   We're passionate about excellence
   
   [Learn More]
   
   [Giant image with no context]
```

**Why It Fails:**
- No clarity about what you do
- No benefit communicated
- "Learn More" is weak CTA
- Trust not established

---

### Pattern: Segmented Entry Points

**What Works:**
```
Homepage Hero:
"[Main Value Prop]"

    I'm looking for:
    
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Option A   │  │  Option B   │  │  Option C   │
    │  (Segment)  │  │  (Segment)  │  │  (Segment)  │
    └─────────────┘  └─────────────┘  └─────────────┘
```

**Why It Works:**
- Self-segmentation = relevance
- Reduces cognitive load
- Visitors feel understood
- Enables personalized paths

**When to Use:**
- Multiple distinct audiences
- Different use cases
- Complex product with multiple entry points

---

### Pattern: Social Proof Cascade

**What Works:**
```
Above Fold:
- Quick trust indicator (★★★★★ from 500 reviews)

After Value Prop:
- Logo bar ("Trusted by...")

Mid-Page:
- Specific testimonial with photo, name, title

Before CTA:
- Results-focused case study snippet

Near Pricing:
- ROI or value testimonial
```

**Why It Works:**
- Trust builds progressively
- Different proof types serve different needs
- Objections answered as they arise
- Proof appears before asks

**Anti-Pattern: Proof Desert**
```
Hero with claims
↓
Features section with claims
↓
More features with claims
↓
"Contact Us"

(No testimonials, no logos, no data)
```

**Why It Fails:**
- Claims without evidence
- Trust never established
- Why should anyone believe you?

---

## Product/Service Page Patterns

### Pattern: Benefit-Feature-Proof Stack

**What Works:**
```
┌────────────────────────────────────────────────────┐
│ BENEFIT (What they get)                             │
│ "Save 10 hours per week on reporting"              │
│                                                     │
│ Feature (How it works)                              │
│ "Automated data aggregation from 50+ sources"      │
│                                                     │
│ Proof (Evidence it works)                          │
│ "Acme Corp reduced reporting time by 73%"          │
└────────────────────────────────────────────────────┘
```

**Why It Works:**
- Leads with value (what's in it for me?)
- Explains mechanism (how?)
- Proves it's real (show me)

**Anti-Pattern: Feature Dump**
```
FEATURES:
• Feature A
• Feature B  
• Feature C
• Feature D
• Feature E
(No benefits, no proof, no hierarchy)
```

**Why It Fails:**
- User has to translate features → benefits
- Most won't bother
- Nothing stands out
- No evidence anything works

---

### Pattern: Objection Inoculation

**What Works:**
```
[Main content establishing value]

───────────────────────────────────
You might be wondering...

"Is this hard to set up?"
→ Most customers are live in under 24 hours.
   [Testimonial: "Easier setup than I expected"]

"What if it doesn't work for us?"
→ 30-day money-back guarantee, no questions asked.

"Is my data secure?"
→ SOC2 compliant, bank-level encryption.
   [Security badge]
───────────────────────────────────

[CTA with objections handled]
```

**Why It Works:**
- Addresses objections before they become blockers
- Shows you understand their concerns
- Provides immediate relief
- Makes CTA feel safer

**When to Use:**
- High-consideration purchases
- Skeptical audiences
- Common objections identified in research
- Before major conversion points

---

### Pattern: The Comparison Table

**What Works:**
```
Why [Your Brand] vs. Alternatives

                    You    Alt A   Alt B
Feature 1           ✓      ✓       ✗
Feature 2           ✓      ✗       ✓  
Unique Benefit      ✓      ✗       ✗
Price              $$$     $$$$    $$

"See why 5,000+ customers switched"
[View Case Studies]
```

**Why It Works:**
- Helps solution-aware visitors compare
- Controls the narrative
- Highlights your differentiators
- Serves comparison shoppers

**Rules:**
- Be honest (credibility matters)
- Compare on factors you win
- Include unique benefits
- Don't trash competitors

---

## Pricing Page Patterns

### Pattern: Clear Recommendation

**What Works:**
```
Choose Your Plan

┌─────────────┐  ┌─────────────────┐  ┌─────────────┐
│    Basic    │  │   ★ POPULAR ★   │  │  Enterprise │
│             │  │                 │  │             │
│   $9/mo     │  │    $29/mo       │  │   Custom    │
│             │  │                 │  │             │
│  Best for   │  │   Best for      │  │  Best for   │
│  individuals│  │   small teams   │  │  large orgs │
│             │  │                 │  │             │
│  [Start]    │  │  [Start Free]   │  │  [Contact]  │
└─────────────┘  └─────────────────┘  └─────────────┘

               Most customers choose Popular
```

**Why It Works:**
- Decision is made easier
- Social proof for the choice
- "Most popular" anchors decision
- Clear who each is for

**Anti-Pattern: The Paradox of Choice**
```
5 plans with 40 features each
No recommendation
Identical visual weight
No guidance on who should pick what
```

**Why It Fails:**
- Overwhelming
- Analysis paralysis
- Visitors leave without deciding

---

### Pattern: Price Anchoring

**What Works:**
```
Option 1: Value anchor (makes middle look reasonable)
├── Show highest tier first
├── Or show comparable competitor pricing
├── Or show "cost of doing nothing"

Option 2: Savings anchor
├── Show annual savings vs monthly
├── "Save $120/year" (not just "20% off")

Option 3: ROI anchor
├── "Pays for itself in 2 weeks"
├── Show customer savings/gains
├── Calculate value relative to cost
```

**Why It Works:**
- Price is relative, not absolute
- Context shapes perception
- Right anchor makes price feel reasonable

---

## Form Patterns

### Pattern: Minimal Viable Fields

**What Works:**
```
Goal: Newsletter signup
Fields: Email only (maybe first name)

Goal: Lead gen (initial)
Fields: Email, Name, Company

Goal: Demo request
Fields: Email, Name, Company, Company Size, 
        "What are you looking to solve?"

Goal: Checkout
Fields: Only what's needed for transaction
```

**Rules:**
- Ask only what's necessary for the ask
- Every field reduces completion ~7%
- You can always ask more later
- Progressive profiling > big forms

**Anti-Pattern: The Interrogation Form**
```
Newsletter Signup:
• First Name
• Last Name  
• Email
• Phone
• Company
• Title
• Company Size
• Industry
• How did you hear about us?
• What topics interest you?

[Too much for too little value]
```

---

### Pattern: Smart Form UX

**What Works:**
```
Label (always visible)
┌─────────────────────────────────────────┐
│ Value                                    │
└─────────────────────────────────────────┘
Helper text or validation (below)

✓ Labels above or beside inputs (not placeholder-only)
✓ Inline validation (not just on submit)
✓ Error messages specific and helpful
✓ Autofill enabled
✓ Correct input types (tel, email, etc.)
✓ Progress indicator for multi-step
```

**Anti-Pattern: Placeholder-Only Labels**
```
┌─────────────────────────────────────────┐
│ Enter your email                         │  ← Disappears on focus
└─────────────────────────────────────────┘
```

**Why It Fails:**
- User forgets what field is for
- No reference while typing
- Accessibility issues

---

## CTA Patterns

### Pattern: Benefit-Focused Copy

**What Works:**
```
Instead of:          Use:
─────────────────────────────────────────
Submit            → Get My Free Quote
Sign Up           → Start Saving Time
Download          → Get the Checklist
Learn More        → See How It Works
Contact Us        → Talk to an Expert
Buy Now           → Add to My Routine
```

**Why It Works:**
- Communicates value
- Reminds of benefit
- Feels less transactional
- Creates positive anticipation

---

### Pattern: CTA Rhythm

**What Works:**
```
Hero Section:
→ Primary CTA (visible without scroll)

After Value Explanation:
→ CTA (now they understand the value)

After Social Proof:
→ CTA (now they believe it)

After Objection Handling:
→ CTA (concerns addressed)

Bottom of Page:
→ Final CTA (one more chance)
```

**Why It Works:**
- Multiple opportunities to convert
- Different people ready at different points
- Doesn't require scrolling back up
- Not overwhelming (one per section)

**Anti-Pattern: CTA Desert**
```
[Long content section]
[More content]
[More content]
[Even more content]
[Scroll scroll scroll]
...
[Finally a CTA way at the bottom]
```

---

## Trust Patterns

### Pattern: Testimonial That Converts

**What Works:**
```
"I was skeptical about [exact objection your ICP has].
 But after [specific usage], we saw [specific result].
 Now I can't imagine going back."

 — Jane Smith, VP Marketing at RealCompany
   [Photo] [Company logo]
```

**Why It Works:**
- Addresses specific objection
- Shows transformation
- Specific result (not vague)
- Real person, verifiable

**Anti-Pattern: Generic Testimonial**
```
"Great product! Love it!"
 — J.S.
```

**Why It Fails:**
- Says nothing specific
- Could be fake
- Doesn't address objections
- No identification

---

### Pattern: Trust Signal Placement

**What Works:**
```
Above Fold: Quick trust hit
→ "Trusted by 10,000+ teams" or star rating

Near Claims: Proof of claim
→ Testimonial or data supporting the claim

Before CTAs: Risk reduction
→ Guarantee, security badge, "no commitment"

Near Forms: Privacy assurance
→ "We'll never share your email"

Checkout: Security signals
→ SSL badge, secure checkout, payment logos
```

**Why It Works:**
- Trust appears when doubt arises
- Addresses concerns contextually
- Reduces friction at decision points

---

## Mobile Patterns

### Pattern: Thumb-Zone CTAs

**What Works:**
```
Mobile screen:
┌─────────────────────┐
│                     │  ← Hard to reach
│                     │
│    Primary CTA      │  ← Natural thumb zone
│    here             │
│                     │
│  ┌───────────────┐  │
│  │   Action      │  │  ← Sticky CTA
│  └───────────────┘  │
└─────────────────────┘
```

**Why It Works:**
- Easy to tap without adjusting grip
- Sticky CTA always accessible
- Reduces friction on mobile

---

### Pattern: Mobile-First Forms

**What Works:**
```
✓ Large touch targets (44px+ height)
✓ Full-width inputs
✓ Correct keyboard types (email, tel, number)
✓ Single column layout
✓ Inline validation
✓ Labels above inputs
✓ Big, tappable submit button
```

**Anti-Pattern: Desktop Form on Mobile**
```
✗ Tiny inputs
✗ Multi-column layout
✗ Dropdown for everything
✗ Placeholder-only labels
✗ Submit button same size as inputs
```

---

## Navigation Patterns

### Pattern: 7±2 Rule for Nav

**What Works:**
```
Primary Nav: 5-7 items maximum
├── Most important = leftmost
├── CTA = rightmost
├── Logical grouping
└── Mega-menu for overflow (if needed)
```

**Why It Works:**
- Cognitive load manageable
- Clear priority
- Quick scanning
- Less decision fatigue

**Anti-Pattern: The Nav Dump**
```
[15 nav items][Login][Signup][Search][Contact][Cart]
[Then another row of secondary nav]
[And maybe some promotional links too]
```

---

## Error Handling Patterns

### Pattern: Helpful Error States

**What Works:**
```
When form error:

Email Address
┌─────────────────────────────────────────┐
│ john.smith@                              │
└─────────────────────────────────────────┘
⚠ Please enter a complete email address 
  (example: name@company.com)

[↑ Specific, helpful, example given]
```

**Anti-Pattern: Unhelpful Errors**
```
"Invalid input"
"Error"
"Please fix the errors below" [but doesn't say which]
Red fields with no explanation
```

---

## Urgency and Scarcity Patterns

### Pattern: Authentic Urgency

**What Works:**
```
✓ Real deadline: "Sale ends Sunday at midnight"
✓ Real scarcity: "3 spots left in the workshop"
✓ Real consequence: "Lock in 2024 pricing before Jan 1"

Shown with:
- Countdown timer (if real)
- Inventory count (if real)
- Clear deadline explanation
```

**Anti-Pattern: Fake Urgency**
```
✗ Countdown timer that resets on refresh
✗ "Only 2 left!" for digital products
✗ "This offer expires soon" (never does)
✗ Fake "limited time" that's always running
```

**Why Fake Fails:**
- Customers notice
- Destroys trust
- Legal issues in some jurisdictions
- Short-term gain, long-term damage