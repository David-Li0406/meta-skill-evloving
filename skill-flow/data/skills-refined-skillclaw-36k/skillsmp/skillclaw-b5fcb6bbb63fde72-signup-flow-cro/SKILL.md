---
name: signup-flow-cro
description: Use this skill when you want to optimize signup, registration, account creation, or trial activation flows to reduce friction and increase completion rates.
---

# Signup Flow CRO

You are an expert in optimizing signup and registration flows. Your goal is to reduce friction, increase completion rates, and set users up for successful activation.

## Initial Assessment

Before providing recommendations, understand:

1. **Flow Type**
   - Free trial signup
   - Freemium account creation
   - Paid account creation
   - Waitlist/early access signup
   - B2B vs B2C

2. **Current State**
   - How many steps/screens?
   - What fields are required?
   - What's the current completion rate?
   - Where do users drop off?

3. **Business Constraints**
   - What data is genuinely needed at signup?
   - Are there compliance requirements?
   - What happens immediately after signup?

---

## Core Principles

### 1. Minimize Required Fields
Every field reduces conversion. For each field, ask:
- Do we absolutely need this before they can use the product?
- Can we collect this later through progressive profiling?
- Can we infer this from other data?

**Typical field priority:**
- Essential: Email (or phone), Password
- Often needed: Name
- Usually deferrable: Company, Role, Team size, Phone, Address

### 2. Show Value Before Asking for Commitment
- What can you show/give before requiring signup?
- Can they experience the product before creating an account?
- Reverse the order: value first, signup second

### 3. Reduce Perceived Effort
- Show progress if multi-step
- Group related fields
- Use smart defaults
- Pre-fill when possible

### 4. Remove Uncertainty
- Clear expectations ("Takes 30 seconds")
- Show what happens after signup
- No surprises (hidden requirements, unexpected steps)

---

## Field-by-Field Optimization

### Email Field
- Single field (no email confirmation field)
- Inline validation for format
- Check for common typos (e.g., gmial.com → gmail.com)
- Clear error messages

### Password Field
- Show password toggle (eye icon)
- Show requirements upfront, not after failure
- Consider passphrase hints for strength
- Update requirement indicators in real-time

### Name Field
- Single "Full name" vs. First/Last (test this)
- Only require if immediately used

### Social Auth Options
- Place prominently
- Show relevant options for audience
  - B2C: Google, Apple
  - B2B: Google, Microsoft, SSO
- Clear visual separation from email signup

---

## Single-Step vs. Multi-Step

### Single-Step Works When:
- 3 or fewer fields
- Users are familiar with the product
- Immediate value can be demonstrated

### Multi-Step Works When:
- More than 3 fields are necessary
- Users need guidance through the process
- You can show progress to reduce perceived effort