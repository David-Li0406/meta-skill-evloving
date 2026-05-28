---
id: conversion-tracking
name: "Conversion Tracking"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Conversion Tracking

## Metadata

| Field | Value |
|-------|-------|
| **ID** | conversion-tracking |
| **Name** | Conversion Tracking |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | analytics-setup, attribution-models, paid-acquisition |

---

## Problem

Your ads are running but you can't tell which ones drive sales. Platform reporting says one thing, your revenue says another. Without accurate conversion tracking, you're optimizing based on clicks, not customers.

Conversion tracking connects ad spend to revenue. Get it wrong, and every decision is flawed.

---

## Framework

Conversion tracking requires multiple layers:

```
CLIENT-SIDE  -> Browser pixels (standard)
SERVER-SIDE  -> API conversions (enhanced)
OFFLINE      -> CRM data import
```

### Step 1: Define Your Conversions

**Conversion types:**

| Type | Description | Example |
|------|-------------|---------|
| **Macro** | Primary business goal | Purchase, signup |
| **Micro** | Steps toward macro | Add to cart, view pricing |

**Common conversions by business:**

| Business | Macro | Micro |
|----------|-------|-------|
| E-commerce | Purchase | Add to cart, begin checkout |
| SaaS | Trial, Purchase | Signup, pricing view |
| Lead gen | Form submit | Content download |
| App | Install | Registration, purchase |

**Define values:**
- Fixed value: Lead = $50
- Dynamic value: Purchase = actual amount
- Estimated value: Trial = $100 (LTV estimate)

### Step 2: Install Tracking Pixels

**Platform pixels:**

| Platform | Pixel Name | Installation |
|----------|------------|--------------|
| Meta | Meta Pixel | JavaScript + CAPI |
| Google | Google Tag | gtag.js or GTM |
| LinkedIn | Insight Tag | JavaScript |
| Twitter | Twitter Pixel | JavaScript |
| TikTok | TikTok Pixel | JavaScript |

**Meta Pixel installation:**
```html
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');
</script>
```

**Google Ads conversion:**
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXXX');
</script>
```

### Step 3: Track Standard Events

**Event mapping across platforms:**

| Action | Meta | Google | LinkedIn |
|--------|------|--------|----------|
| Page view | PageView | page_view | pageLoad |
| Sign up | CompleteRegistration | sign_up | signUp |
| Lead | Lead | generate_lead | lead |
| Add to cart | AddToCart | add_to_cart | - |
| Purchase | Purchase | purchase | conversion |
| Start trial | StartTrial | trial_started | - |

**Meta event tracking:**
```javascript
// Lead
fbq('track', 'Lead', {
  value: 50.00,
  currency: 'USD'
});

// Purchase
fbq('track', 'Purchase', {
  value: 99.00,
  currency: 'USD',
  content_ids: ['prod_123'],
  content_type: 'product'
});
```

**Google Ads conversion:**
```javascript
// Send conversion
gtag('event', 'conversion', {
  'send_to': 'AW-XXXXXXXXXX/YYYYYYYYY',
  'value': 99.00,
  'currency': 'USD',
  'transaction_id': 'txn_123'
});
```

### Step 4: Implement Server-Side Tracking

**Why server-side (CAPI/API):**
- Browser tracking blocked by privacy features
- More accurate data
- Captures offline conversions
- Better data quality signals

**Meta Conversions API:**
```javascript
// Server-side (Node.js example)
const bizSdk = require('facebook-nodejs-business-sdk');
const EventRequest = bizSdk.EventRequest;
const UserData = bizSdk.UserData;
const ServerEvent = bizSdk.ServerEvent;

const userData = (new UserData())
  .setEmail('sha256_email')
  .setPhone('sha256_phone');

const serverEvent = (new ServerEvent())
  .setEventName('Purchase')
  .setEventTime(Math.floor(Date.now() / 1000))
  .setUserData(userData)
  .setCustomData({ value: 99, currency: 'USD' })
  .setEventSourceUrl('https://yoursite.com/thank-you');

const eventsData = [serverEvent];
const eventRequest = (new EventRequest(pixelId))
  .setEvents(eventsData);

eventRequest.execute();
```

### Step 5: Verify Tracking

**Verification checklist:**

| Platform | Verification Tool |
|----------|-------------------|
| Meta | Test Events, Events Manager |
| Google | Tag Assistant, Ads preview |
| LinkedIn | Insight Tag Helper |
| General | Browser DevTools |

**Testing process:**
1. Install browser extensions (Meta Pixel Helper, etc.)
2. Complete a test conversion
3. Check Events Manager/platform reports
4. Verify data matches expected values
5. Check server-side events if applicable

### Step 6: Attribution Windows

**Attribution settings:**

| Platform | Default Click | Default View |
|----------|---------------|--------------|
| Meta | 7 days | 1 day |
| Google | 30 days | - |
| LinkedIn | 30 days | 7 days |

**Setting considerations:**
- Longer windows = more conversions attributed
- Shorter windows = more conservative
- Match to your sales cycle

---

## Templates

### Conversion Tracking Plan

```markdown
## Conversion Tracking: [Site/App]

### Macro Conversions (Goals)
| Conversion | Value | Event Name | Platforms |
|------------|-------|------------|-----------|
| Purchase | Dynamic | purchase | All |
| Trial | $50 | trial_started | All |
| Lead | $25 | lead | All |

### Micro Conversions (Signals)
| Conversion | Event Name | Platforms |
|------------|------------|-----------|
| Pricing view | view_pricing | GA4, Meta |
| Add to cart | add_to_cart | All |
| Begin checkout | begin_checkout | All |

### Implementation
- [ ] Meta Pixel installed
- [ ] Meta CAPI configured
- [ ] Google Tag installed
- [ ] Google Ads conversions set
- [ ] LinkedIn Insight Tag installed
- [ ] All events tested
```

### Verification Checklist

```markdown
## Conversion Tracking Verification

### Meta
- [ ] Pixel installed (Pixel Helper shows green)
- [ ] PageView fires on all pages
- [ ] Conversion events fire on correct pages
- [ ] Event values passing correctly
- [ ] Events Manager shows recent events
- [ ] CAPI events showing (if applicable)

### Google
- [ ] gtag installed
- [ ] Conversions configured in Ads
- [ ] Test conversion tracked
- [ ] Values passing correctly

### LinkedIn
- [ ] Insight Tag installed
- [ ] Conversions configured
- [ ] Events firing correctly
```

---

## Examples

### SaaS Conversion Setup

**Conversions:**
```javascript
// Trial start
fbq('track', 'StartTrial', { value: 50, currency: 'USD' });
gtag('event', 'conversion', { 'send_to': 'AW-XXX/trial' });

// Subscription
fbq('track', 'Purchase', {
  value: 99,
  currency: 'USD',
  predicted_ltv: 500
});
gtag('event', 'conversion', {
  'send_to': 'AW-XXX/purchase',
  'value': 99,
  'currency': 'USD'
});
```

### E-commerce Setup

**Conversions:**
```javascript
// Add to cart
fbq('track', 'AddToCart', {
  value: 49.99,
  currency: 'USD',
  content_ids: ['SKU123'],
  content_type: 'product'
});

// Purchase
fbq('track', 'Purchase', {
  value: 149.99,
  currency: 'USD',
  content_ids: ['SKU123', 'SKU456'],
  content_type: 'product',
  num_items: 2
});
```

---

## Implementation Checklist

### Planning
- [ ] Define all conversion events
- [ ] Assign values to each conversion
- [ ] Map events to ad platforms
- [ ] Plan server-side implementation

### Implementation
- [ ] Install all pixel codes
- [ ] Implement standard events
- [ ] Add dynamic values
- [ ] Set up server-side tracking

### Testing
- [ ] Test each conversion type
- [ ] Verify values pass correctly
- [ ] Check attribution settings
- [ ] Monitor for 24-48 hours

### Maintenance
- [ ] Monthly accuracy review
- [ ] Check for pixel errors
- [ ] Update with site changes
- [ ] Review attribution settings

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No testing | Events not firing | Always test before launch |
| Wrong values | Bad optimization | Verify value passing |
| Duplicate events | Inflated counts | Ensure single fire |
| No server-side | Missing conversions | Implement CAPI |
| Ignoring errors | Data loss | Monitor Events Manager |
| Wrong attribution | Misleading data | Align with sales cycle |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Pixel installation | GTM, direct code |
| Testing | Pixel helpers, DevTools |
| Server-side | Customer.io, Segment, custom |
| Monitoring | Events Manager, GA4 |
| Debugging | Platform debug modes |

---

## Related Methodologies

- **analytics-setup:** Analytics Setup (analytics foundation)
- **attribution-models:** Attribution Models (understanding attribution)
- **meta-reporting:** Meta Reporting (using conversion data)
- **google-reporting:** Google Reporting (using conversion data)

---

*Methodology: conversion-tracking | Ads API | faion-ads-agent*
