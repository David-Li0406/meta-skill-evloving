# Micro Saas Launcher - Validations

## No Payment Integration

### **Id**
no-payment-integration
### **Severity**
high
### **Type**
conceptual
### **Check**
SaaS should have payment integration
### **Indicators**
  - No Stripe/payment provider
  - Manual invoicing only
  - Free with no upgrade path
### **Message**
No payment integration - can't collect revenue.
### **Fix Action**
Integrate Stripe or Lemon Squeezy for payments

## No User Authentication

### **Id**
no-auth-system
### **Severity**
high
### **Type**
conceptual
### **Check**
SaaS should have user authentication
### **Indicators**
  - No login/signup
  - Rolling your own auth
  - Password stored in plaintext
### **Message**
No proper authentication system.
### **Fix Action**
Use Supabase Auth, Clerk, or Auth0 - don't build auth yourself

## No User Onboarding

### **Id**
no-onboarding
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have onboarding flow for new users
### **Indicators**
  - Users dropped into empty dashboard
  - No welcome email
  - No first-action guidance
### **Message**
No user onboarding - will hurt activation.
### **Fix Action**
Add welcome flow, first-action prompt, and onboarding emails

## No Product Analytics

### **Id**
no-analytics
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should track user behavior and metrics
### **Indicators**
  - No analytics integration
  - Can't see what users do
  - No conversion tracking
### **Message**
No product analytics - flying blind.
### **Fix Action**
Add Posthog, Mixpanel, or simple event tracking

## Missing Legal Pages

### **Id**
no-legal-pages
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have privacy policy and terms
### **Indicators**
  - No privacy policy
  - No terms of service
  - Required for Stripe
### **Message**
Missing legal pages - required for payments.
### **Fix Action**
Add privacy policy and terms of service (use templates)