---
name: analytics-tracking
description: Use this skill when you want to set up, improve, or audit analytics tracking and measurement, including tools like GA4, Google Analytics, and tag managers.
---

# Analytics Tracking

You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions.

## Initial Assessment

Before implementing tracking, understand:

1. **Business Context**
   - What decisions will this data inform?
   - What are the key conversion actions?
   - What questions need answering?

2. **Current State**
   - What tracking exists?
   - What tools are in use (GA4, Mixpanel, Amplitude, etc.)?
   - What's working/not working?

3. **Technical Context**
   - What's the tech stack?
   - Who will implement and maintain?
   - Any privacy/compliance requirements?

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every event should inform a decision.
- Avoid vanity metrics.
- Quality > quantity of events.

### 2. Start with the Questions
- What do you need to know?
- What actions will you take based on this data?
- Work backwards to what you need to track.

### 3. Name Things Consistently
- Naming conventions matter.
- Establish patterns before implementing.
- Document everything.

### 4. Maintain Data Quality
- Validate implementation.
- Monitor for issues.
- Clean data > more data.

---

## Tracking Plan Framework

### Structure

```
Event Name | Event Category | Properties | Trigger | Notes
---------- | ------------- | ---------- | ------- | -----
```

### Event Types

**Pageviews**
- Automatic in most tools.
- Enhanced with page metadata.

**User Actions**
- Button clicks.
- Form submissions.
- Feature usage.
- Content interactions.

**System Events**
- Signup completed.
- Purchase completed.
- Subscription changed.
- Errors occurred.

**Custom Conversions**
- Goal completions.
- Funnel stages.
- Business-specific milestones.

---

## Event Naming Conventions

### Format Options

**Object-Action (Recommended)**
```
signup_completed
button_clicked
form_submitted
article_read
```

**Action-Object**
```
click_button
submit_form
complete_signup
```

**Category_Object_Action**
```
checkout_payment_completed
blog_article_viewed
onboarding_step_completed
```

### Best Practices

- Ensure consistency in naming across all events.
- Regularly review and update the tracking plan as business needs evolve.