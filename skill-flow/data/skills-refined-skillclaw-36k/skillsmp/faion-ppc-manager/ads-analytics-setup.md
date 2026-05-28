---
id: analytics-setup
name: "Analytics Setup"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Analytics Setup

## Metadata

| Field | Value |
|-------|-------|
| **ID** | analytics-setup |
| **Name** | Analytics Setup |
| **Category** | Ads API |
| **Difficulty** | Beginner |
| **Agent** | faion-ads-agent |
| **Related** | conversion-tracking, attribution-models, paid-acquisition |

---

## Problem

You're running ads but can't measure what's working. You rely on platform metrics but don't see the full picture. Without proper analytics, you're flying blind and making decisions based on incomplete data.

Proper analytics setup gives you clarity on ROI across all channels.

---

## Framework

Analytics setup follows a three-layer approach:

```
COLLECT   -> Track events and user actions
ANALYZE   -> Understand user behavior
ATTRIBUTE -> Connect ads to revenue
```

### Step 1: Choose Your Analytics Stack

**Essential tools:**

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **GA4** | Website analytics | All websites |
| **Mixpanel** | Product analytics | SaaS, apps |
| **Amplitude** | Product analytics | SaaS, apps |
| **Plausible** | Privacy-first analytics | GDPR-focused |
| **Segment** | Data routing | Multiple tools |

**Recommended stack:**
- Small: GA4 + ad platform pixels
- Medium: GA4 + Segment + Mixpanel
- Large: Segment + Mixpanel/Amplitude + data warehouse

### Step 2: Install Google Analytics 4

**Setup steps:**

1. Create GA4 property
2. Get Measurement ID (G-XXXXXXXXXX)
3. Install via:
   - Google Tag Manager (recommended)
   - Direct installation
   - Platform integration

**GA4 installation (direct):**
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Enhanced measurement (automatic):**
- Page views
- Scrolls
- Outbound clicks
- Site search
- Video engagement
- File downloads

### Step 3: Configure Events

**Standard events to track:**

| Event | When to Fire | Purpose |
|-------|--------------|---------|
| page_view | Every page load | Traffic |
| sign_up | Account creation | Conversions |
| login | User login | Engagement |
| purchase | Transaction complete | Revenue |
| generate_lead | Form submission | Lead gen |
| begin_checkout | Start checkout | Funnel |
| add_to_cart | Item added | E-commerce |

**Custom events for SaaS:**
```javascript
// Trial started
gtag('event', 'trial_started', {
  'plan_name': 'pro',
  'source': 'website'
});

// Feature used
gtag('event', 'feature_used', {
  'feature_name': 'export',
  'usage_count': 1
});

// Upgrade completed
gtag('event', 'purchase', {
  'value': 99.00,
  'currency': 'USD',
  'plan': 'pro_annual'
});
```

### Step 4: Set Up Conversions

**Mark key events as conversions:**

1. GA4 Admin → Events → Conversions
2. Toggle conversion for important events
3. Set up conversion values

**Conversion events by business type:**

| Business | Key Conversions |
|----------|-----------------|
| E-commerce | purchase, add_to_cart, begin_checkout |
| SaaS | sign_up, trial_started, purchase |
| Lead gen | generate_lead, form_submit |
| Content | newsletter_signup, download |

### Step 5: UTM Tracking

**UTM parameters:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Traffic source | google, facebook |
| utm_medium | Marketing medium | cpc, email, social |
| utm_campaign | Campaign name | spring_sale_2026 |
| utm_content | Ad variation | blue_banner_v2 |
| utm_term | Keyword (search) | project_management |

**URL structure:**
```
https://yoursite.com/page?
utm_source=facebook
&utm_medium=cpc
&utm_campaign=trial_promo
&utm_content=video_ad_1
```

**UTM best practices:**
- Consistent naming conventions
- Lowercase only
- Use underscores, not spaces
- Document your conventions

### Step 6: Dashboard Setup

**Essential GA4 reports:**

| Report | What It Shows |
|--------|---------------|
| Acquisition overview | Traffic sources |
| Traffic acquisition | Campaigns, sources |
| Engagement overview | User behavior |
| Conversions | Conversion events |
| Revenue | E-commerce data |

**Custom reports to create:**
- Conversion by source/medium
- Funnel visualization
- Campaign performance
- Landing page performance

---

## Templates

### Event Tracking Plan

```markdown
## Event Tracking Plan: [Product]

### Page Events (Automatic)
- page_view (all pages)
- scroll (25%, 50%, 75%, 100%)
- outbound_click
- file_download

### User Events
| Event | Trigger | Parameters |
|-------|---------|------------|
| sign_up | Account created | method, plan |
| login | User logged in | method |
| trial_started | Trial begins | plan_name |
| purchase | Subscription/purchase | value, currency, plan |

### Engagement Events
| Event | Trigger | Parameters |
|-------|---------|------------|
| feature_used | Key feature accessed | feature_name |
| content_viewed | Article/doc viewed | content_id, content_type |
| search | Site search | search_term |

### Conversion Events (mark as conversions)
- sign_up
- trial_started
- purchase
- generate_lead
```

### UTM Convention Document

```markdown
## UTM Naming Conventions

### Source (utm_source)
- google (Google Ads)
- meta (Facebook/Instagram)
- linkedin (LinkedIn)
- twitter (Twitter/X)
- email (Email campaigns)
- affiliate (Affiliate traffic)

### Medium (utm_medium)
- cpc (Paid search)
- paid_social (Paid social)
- email (Email)
- organic_social (Organic social)
- referral (Referral)

### Campaign (utm_campaign)
- Format: [initiative]_[description]_[date]
- Example: launch_spring_sale_2026q1

### Content (utm_content)
- Format: [type]_[description]_[version]
- Example: video_testimonial_v2
```

---

## Examples

### SaaS Analytics Setup

**Events tracked:**
```javascript
// Core funnel
gtag('event', 'sign_up', { method: 'email' });
gtag('event', 'trial_started', { plan: 'pro' });
gtag('event', 'onboarding_completed');
gtag('event', 'purchase', { value: 99, currency: 'USD' });

// Engagement
gtag('event', 'feature_used', { feature: 'dashboard' });
gtag('event', 'invite_sent', { count: 1 });
gtag('event', 'integration_connected', { name: 'slack' });
```

**Dashboard metrics:**
- Sign-ups by source
- Trial to paid rate by source
- Revenue by campaign
- Feature adoption

### E-commerce Analytics Setup

**Events tracked:**
```javascript
// Purchase funnel
gtag('event', 'view_item', { items: [...] });
gtag('event', 'add_to_cart', { items: [...] });
gtag('event', 'begin_checkout');
gtag('event', 'purchase', { value: 150, currency: 'USD' });

// Engagement
gtag('event', 'view_item_list', { item_list_name: 'category' });
gtag('event', 'add_to_wishlist');
```

---

## Implementation Checklist

### Foundation
- [ ] Create GA4 property
- [ ] Install GA4 tracking code
- [ ] Verify page views tracking
- [ ] Enable enhanced measurement

### Events
- [ ] Define event tracking plan
- [ ] Implement custom events
- [ ] Test all events firing
- [ ] Mark conversions

### Integrations
- [ ] Link Google Ads
- [ ] Set up other ad platforms
- [ ] Configure UTM tracking
- [ ] Test attribution

### Reporting
- [ ] Set up key reports
- [ ] Create conversion goals
- [ ] Build dashboard
- [ ] Schedule reports

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No event tracking | Only see page views | Define event plan |
| Inconsistent UTMs | Messy data | Document conventions |
| No conversions set | Can't optimize ads | Mark key events |
| Ignoring debug mode | Errors undetected | Test before launch |
| Too many events | Noise | Focus on important actions |

---

## Verification Steps

**Check your setup:**

1. **Real-time report:** Verify events fire
2. **Debug mode:** Use GA4 DebugView
3. **Tag Assistant:** Chrome extension
4. **Ad platform pixels:** Each platform's helper

---

## Tools

| Purpose | Tools |
|---------|-------|
| Analytics | GA4, Mixpanel, Amplitude |
| Tag management | Google Tag Manager |
| Testing | Tag Assistant, DebugView |
| Visualization | Looker Studio |
| Privacy | Plausible, Fathom |

---

## Related Methodologies

- **conversion-tracking:** Conversion Tracking (platform-specific)
- **attribution-models:** Attribution Models
- **budget-optimization:** Budget Optimization
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: analytics-setup | Ads API | faion-ads-agent*
