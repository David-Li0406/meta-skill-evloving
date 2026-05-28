---
name: conversion-audit
description: |
  Frameworks, heuristics, and checklists for auditing websites and strategy documents for conversion optimization. Provides systematic approaches to finding conversion killers.
  
  USE THIS SKILL WHEN:
  - Auditing strategy documents
  - Reviewing page briefs or wireframes
  - Evaluating existing websites
  - Identifying conversion friction
  - Prioritizing optimization efforts
  
  PROVIDES: Audit frameworks, severity criteria, pattern recognition, prioritization methods
allowed-tools: Read, Grep, Glob
---

# Conversion Audit Skill

## Overview

Conversion auditing is systematic, not subjective. This skill provides frameworks to find issues reliably, assess severity consistently, and prioritize fixes effectively.

---

## Framework 1: The CONVERT Framework

A seven-dimension framework for comprehensive conversion assessment.

### The Dimensions

```
C - CLARITY
    Can visitors understand what you do/offer within 5 seconds?
    
    Questions:
    - Is the value proposition visible above the fold?
    - Does the headline communicate benefit, not just feature?
    - Is the primary action obvious?
    - Would a stranger know what to do?
    
    Scoring:
    5 = Crystal clear, no confusion possible
    4 = Clear to most visitors
    3 = Requires some effort to understand
    2 = Confusing, multiple interpretations
    1 = Completely unclear what this is

O - OBJECTIONS
    Are known customer concerns proactively addressed?
    
    Questions:
    - Are ICP objections identified and mapped?
    - Does content address objections before they become blockers?
    - Is there proof/evidence for each major claim?
    - Are risk-reducers present (guarantees, trials)?
    
    Scoring:
    5 = All major objections addressed with proof
    4 = Most objections addressed
    3 = Some objections addressed, gaps exist
    2 = Few objections addressed
    1 = Objections ignored or avoided

N - NAVIGATION
    Can users find what they need easily?
    
    Questions:
    - Can any page reach conversion in ≤3 clicks?
    - Is the menu intuitive and scannable?
    - Are there dead ends?
    - Is search available (if needed)?
    
    Scoring:
    5 = Effortless navigation, logical structure
    4 = Good navigation with minor issues
    3 = Adequate but some friction
    2 = Confusing, users will get lost
    1 = Broken or highly confusing

V - VALUE
    Is the benefit clear at every touchpoint?
    
    Questions:
    - Are features framed as benefits?
    - Is "what's in it for me" answered throughout?
    - Is there a reason to act now?
    - Does the value justify the ask?
    
    Scoring:
    5 = Compelling value at every step
    4 = Value clear, minor gaps
    3 = Value present but not compelling
    2 = Value unclear or weak
    1 = No clear value communicated

E - EVIDENCE
    Is there sufficient proof for claims?
    
    Questions:
    - Are testimonials present and specific?
    - Is there data/statistics supporting claims?
    - Are case studies or results shown?
    - Are credentials/certifications displayed?
    
    Scoring:
    5 = Overwhelming proof, hard to doubt
    4 = Strong evidence present
    3 = Some evidence, could be stronger
    2 = Weak or generic evidence
    1 = No evidence, just claims

R - RELEVANCE
    Does content match visitor intent and stage?
    
    Questions:
    - Does content match awareness level?
    - Is the language familiar to the ICP?
    - Does it answer what brought them here?
    - Are there paths for different intents?
    
    Scoring:
    5 = Perfectly matched to visitor needs
    4 = Well-matched with minor gaps
    3 = Generally relevant
    2 = Mismatch between content and intent
    1 = Completely irrelevant

T - TRUST
    Are there adequate signals of credibility?
    
    Questions:
    - Are trust signals visible early?
    - Is the company/team humanized?
    - Is contact information accessible?
    - Are security/privacy concerns addressed?
    
    Scoring:
    5 = Trust established at every touchpoint
    4 = Good trust signals present
    3 = Adequate trust, some gaps
    2 = Trust signals weak or missing
    1 = Looks untrustworthy or scammy
```

### Using CONVERT

1. Score each dimension 1-5
2. Note specific evidence for each score
3. Overall score = average (but critical issues override)
4. Priority: Fix lowest scores first (diminishing returns)

---

## Framework 2: Friction Mapping

Identify and categorize conversion barriers.

### Friction Types

```
COGNITIVE FRICTION
Mental effort required to understand or decide

Examples:
- Complex pricing tables
- Jargon-heavy copy
- Too many options
- Unclear next steps
- Information overload

Detection:
- Would a tired user understand this?
- How many decisions are required?
- Is information chunked appropriately?


EMOTIONAL FRICTION
Fear, uncertainty, or discomfort that prevents action

Examples:
- No guarantee or return policy
- Hidden pricing (must contact to learn)
- No social proof
- Impersonal, cold tone
- Asking for too much too soon

Detection:
- What might make someone hesitate?
- Where would skepticism arise?
- What fears go unaddressed?


INTERACTION FRICTION
Physical or technical barriers to completing actions

Examples:
- Too many form fields
- Small tap targets
- Slow load times
- Broken functionality
- No autofill support

Detection:
- How many clicks/taps required?
- Are inputs optimized for device?
- What technical barriers exist?


PROCESS FRICTION
Steps or requirements that feel unnecessary

Examples:
- Mandatory account creation
- Forced verification steps
- Requiring info not needed for the ask
- Multi-page forms for simple actions
- Captcha on every action

Detection:
- What steps could be eliminated?
- What's required vs. nice-to-have?
- Where do users abandon?
```

### Friction Severity Assessment

```
SEVERITY MATRIX

                    Low Frequency    High Frequency
                   (Few users hit)  (Most users hit)
                   ─────────────────────────────────
High Impact        MEDIUM           CRITICAL
(Causes abandon)   
                   
Low Impact         LOW              MEDIUM
(Causes annoyance)

Frequency × Impact = Priority
```

---

## Framework 3: Trust Signal Architecture

Evaluate how trust is built throughout the experience.

### Trust Signal Categories

```
SOCIAL PROOF
- Testimonials (specific > generic)
- Reviews and ratings
- Client/customer logos
- User counts or metrics
- Media mentions

AUTHORITY SIGNALS
- Certifications and credentials
- Awards and recognition
- Expert endorsements
- Industry association membership
- Published thought leadership

CREDIBILITY MARKERS
- Professional design quality
- Clear contact information
- Physical address (if applicable)
- Team/founder photos and bios
- Company history/story

RISK REDUCERS
- Money-back guarantee
- Free trial or sample
- Clear refund policy
- No long-term commitment
- Easy cancellation

SECURITY SIGNALS
- SSL certificate (https)
- Security badges
- Privacy policy
- Secure checkout messaging
- Data protection statements
```

### Trust Timing Audit

Trust signals must appear BEFORE the ask:

```
TRUST TIMING CHECKLIST

Homepage:
□ Trust signal visible above fold
□ Social proof before first CTA
□ Credibility established early

Product/Service Page:
□ Testimonial before "Buy" CTA
□ Guarantee visible near price
□ Credentials shown with claims

Checkout/Signup:
□ Security badges visible
□ Privacy assurance near form
□ Review/testimonial reminder

RULE: If you're asking for something (email, money, time),
      trust must come first.
```

---

## Framework 4: CTA Effectiveness Analysis

Evaluate call-to-action implementation.

### CTA Audit Criteria

```
VISIBILITY
□ Above the fold on key pages
□ Sufficient contrast from surroundings
□ Repeated at logical intervals
□ Not competing with other CTAs
□ Mobile: reachable by thumb

CLARITY  
□ Action is specific (not "Submit")
□ Benefit is implied or stated
□ Commitment level is appropriate
□ What happens next is clear

HIERARCHY
□ Primary CTA is visually dominant
□ Secondary doesn't compete
□ One primary per page section
□ Ghost buttons for secondary actions

PSYCHOLOGY
□ Low-friction language (if appropriate)
□ Urgency (if authentic)
□ Benefit-oriented copy
□ Addresses "why now"

PLACEMENT
□ After value is established
□ Near relevant proof
□ At natural decision points
□ Not buried below fold
```

### CTA Copy Spectrum

```
COMMITMENT LEVEL MATCHING

High Commitment Ask (Buy, Subscribe, Sign Contract)
→ Needs more proof, more trust, more value first
→ CTA copy can be direct: "Start Your Plan", "Buy Now"

Medium Commitment Ask (Free Trial, Demo, Consultation)
→ Reduce friction with "free", "no obligation"
→ CTA copy: "Try Free for 14 Days", "Book Free Demo"

Low Commitment Ask (Email, Download, Learn More)
→ Emphasize value received
→ CTA copy: "Get the Guide", "See How It Works"

RULE: Match CTA commitment to visitor readiness
```

---

## Framework 5: Awareness-Stage Alignment

Ensure content matches where visitors are in their journey.

### Awareness Level Content Mapping

```
UNAWARE
"I don't know I have a problem"

Content Should:
- Educate about the problem
- Create recognition of need
- NOT pitch solution yet

Audit Check:
□ Is there top-of-funnel content?
□ Does it identify with audience pain?
□ Does it avoid premature selling?


PROBLEM-AWARE  
"I know I have a problem, don't know solutions exist"

Content Should:
- Validate the problem
- Introduce solution category
- Begin building trust

Audit Check:
□ Is the problem clearly articulated?
□ Is solution introduced gently?
□ Is there empathy for the situation?


SOLUTION-AWARE
"I know solutions exist, comparing options"

Content Should:
- Differentiate from alternatives
- Prove effectiveness
- Address "why you"

Audit Check:
□ Is differentiation clear?
□ Is there comparison content?
□ Are unique benefits emphasized?


PRODUCT-AWARE
"I know your product, deciding if it's right"

Content Should:
- Handle objections
- Provide detailed proof
- Reduce risk

Audit Check:
□ Are objections addressed?
□ Is there case study depth?
□ Are guarantees visible?


MOST AWARE
"I'm ready, just need the right offer"

Content Should:
- Make purchase easy
- Remove all friction
- Provide urgency if authentic

Audit Check:
□ Is checkout frictionless?
□ Are barriers minimized?
□ Is the offer clear?
```

### Mismatch Detection

```
COMMON MISMATCHES

Selling to Unaware:
- Pitching features before establishing problem
- "Buy now" to someone who doesn't know they need it
→ Feels pushy, creates resistance

Over-explaining to Most Aware:
- Long sales pages to ready buyers
- Too much education when they want to purchase
→ Creates friction, delays conversion

Under-proving to Solution Aware:
- Claims without evidence
- Differentiation without specifics
→ Doesn't overcome comparison shopping
```

---

## Framework 6: Mobile Conversion Audit

Mobile-specific conversion factors.

### Mobile Audit Checklist

```
NAVIGATION
□ Primary CTA reachable by thumb
□ Menu is finger-friendly
□ Back/escape always possible
□ No horizontal scrolling required

CONTENT
□ Headlines readable without zoom
□ Body text 16px minimum
□ Key content not hidden in accordions
□ Images optimized for bandwidth

FORMS
□ Input types correct (tel, email)
□ Labels always visible
□ Keyboard doesn't obscure input
□ Autofill enabled
□ Field number minimized

TAPPABLE ELEMENTS
□ Touch targets 44px minimum
□ Adequate spacing between elements
□ No tiny links in text blocks
□ Buttons full-width where appropriate

PERFORMANCE
□ Page loads in <3 seconds
□ Images lazy-loaded
□ No render-blocking resources
□ Works on slower connections

TRUST
□ Trust signals visible without scroll
□ Testimonials readable on mobile
□ Security badges don't break layout
```

### Mobile-Specific Friction

```
HIGH-FRICTION ON MOBILE

- Long forms (3+ fields feels long)
- Dropdown menus (hard to use)
- Hover-dependent interactions
- Tiny tap targets
- Landscape-only content
- Desktop-focused layouts

MOBILE CONVERSION BOOSTERS

- Click-to-call buttons
- Sticky CTAs on scroll
- Simplified checkout
- Touch-friendly forms
- Fast load times
- Thumb-zone optimization
```

---

## Framework 7: Issue Prioritization Matrix

How to prioritize what to fix first.

### Impact vs. Effort Matrix

```
                    LOW EFFORT           HIGH EFFORT
                    ─────────────────────────────────
HIGH IMPACT        │ QUICK WINS        │ MAJOR PROJECTS
                   │ Do immediately    │ Plan carefully
                   │                   │
                   ├───────────────────┼───────────────
LOW IMPACT         │ FILL-INS          │ AVOID
                   │ Do when time      │ Don't bother
                   │ permits           │ unless required
                   └───────────────────┴───────────────

Classification Questions:
- Impact: How many users affected? How much revenue at stake?
- Effort: Time, cost, complexity, dependencies?
```

### Prioritization Scoring

```
PRIORITY SCORE = (Impact × Confidence) / Effort

Impact (1-5):
5 = Affects primary conversion path
4 = Affects secondary conversion
3 = Affects engagement metrics
2 = Affects satisfaction
1 = Affects edge cases

Confidence (1-5):
5 = Data proves this is an issue
4 = Strong evidence (testing, best practices)
3 = Moderate evidence (heuristics)
2 = Hypothesis based on experience
1 = Gut feeling

Effort (1-5):
1 = Minutes to fix
2 = Hours to fix
3 = Days to fix
4 = Weeks to fix
5 = Months to fix

Example:
- Homepage headline unclear
  Impact: 5 (affects everyone)
  Confidence: 4 (best practice violation)
  Effort: 1 (just copy change)
  Score: (5 × 4) / 1 = 20 → HIGH PRIORITY
```

---

## Common Conversion Killers

### The "Who Are You?" Problem
- No clear value proposition
- Can't tell what you do
- No differentiation
**Fix:** Clarity in headline + subheadline

### The "Why Should I Care?" Problem
- Features without benefits
- No relevance to visitor needs
- Generic messaging
**Fix:** Benefit-focused copy tied to ICP pain

### The "Why Should I Believe You?" Problem
- Claims without proof
- No testimonials or weak ones
- Missing credentials
**Fix:** Strategic social proof placement

### The "What If I'm Wrong?" Problem
- No guarantee or risk reducer
- Commitment feels too high
- No easy out
**Fix:** Risk reversals near CTAs

### The "I'm Not Ready" Problem
- Only hard conversion options
- No nurture path
- Lose non-ready visitors forever
**Fix:** Secondary capture (email, content)

### The "This Is Annoying" Problem
- Too many form fields
- Complicated process
- Technical friction
**Fix:** Ruthless friction reduction

---

## References

For additional patterns and examples, see:
- `references/conversion-patterns.md` - Common patterns and anti-patterns
- `references/page-type-benchmarks.md` - Expected elements by page type
- `references/severity-examples.md` - Calibration for severity levels