# Pricing Strategy - Validations

## Hardcoded Prices in Code

### **Id**
hardcoded-prices
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - price\s*[=:]\s*[0-9]+
  - amount\s*[=:]\s*[0-9]+
  - cost\s*[=:]\s*[0-9]+
  - \$[0-9]+\.?[0-9]*
### **Message**
Hardcoded price found. Consider moving to configuration for easy updates.
### **Fix Action**
Move prices to config file or database for easy price changes
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - test|spec|mock|fixture

## Price Without Currency

### **Id**
no-currency-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - price:\s*[0-9]
  - amount:\s*[0-9]
  - \{\s*price:\s*[0-9]
### **Message**
Price without explicit currency. Add currency field to prevent issues.
### **Fix Action**
Add currency field: { amount: 1000, currency: 'USD' }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.json
### **Exceptions**
  - currency|Currency|USD|EUR

## Floating Point for Money

### **Id**
float-money-calculation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - price\s*\*\s*[0-9]+\.[0-9]
  - amount\s*\*\s*[0-9]+\.[0-9]
  - \$[0-9]+\.[0-9]+\s*[\+\-\*\/]
### **Message**
Floating point arithmetic with money causes rounding errors. Use cents.
### **Fix Action**
Store prices in cents (integers) and format for display only
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Monthly Before Annual on Pricing

### **Id**
pricing-page-monthly-first
### **Severity**
info
### **Type**
regex
### **Pattern**
  - monthly.*annual
  - month.*year
  - \$[0-9]+/mo.*\$[0-9]+/yr
### **Message**
Consider showing annual pricing first to anchor on higher value.
### **Fix Action**
Show annual first with 'save X%' messaging, monthly as alternative
### **Applies To**
  - **/*.tsx
  - **/*.jsx
  - **/*.html
  - **/pricing*

## Trial Without Expiration Handling

### **Id**
missing-trial-expiry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - trial\s*[=:]\s*true
  - isTrial
  - trialActive
### **Message**
Trial state found without clear expiration handling.
### **Fix Action**
Add trialEndsAt and handle expiration with conversion prompt
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - trialEnd|expiresAt|endsAt

## Feature Access Without Plan Check

### **Id**
no-subscription-status-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - user\.plan(?!\s*===|\s*!==|\s*==)
  - subscription(?!\.|\[)
### **Message**
Accessing plan without checking status. Verify subscription is active.
### **Fix Action**
Check subscription.status === 'active' before granting access
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Discount Applied Without Limits

### **Id**
discount-without-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - discount\s*=\s*req\.
  - discount\s*=\s*params\.
  - applyDiscount\([^)]*\)
### **Message**
Discount applied from user input. Validate discount codes server-side.
### **Fix Action**
Validate discount code exists and is within allowed percentage limits
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Pricing Page Without Analytics

### **Id**
pricing-no-analytics
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Pricing|pricing
  - PricingPage|pricingPage
### **Message**
Pricing page should have conversion tracking.
### **Fix Action**
Add analytics events: pricing_view, plan_click, checkout_start
### **Applies To**
  - **/pricing*.tsx
  - **/pricing*.jsx
  - **/Pricing*.tsx
### **Exceptions**
  - analytics|track|gtag|segment

## Hardcoded Stripe Price ID

### **Id**
stripe-price-id-hardcoded
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - price_[a-zA-Z0-9]{24}
  - prod_[a-zA-Z0-9]{24}
### **Message**
Hardcoded Stripe Price/Product ID. Use environment variables.
### **Fix Action**
Move to env: STRIPE_PRICE_STARTER=price_xxx
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - .env|config

## Usage Limit Without Upgrade Path

### **Id**
no-upgrade-prompt
### **Severity**
info
### **Type**
regex
### **Pattern**
  - limit\s*reached
  - exceeded\s*quota
  - usage\s*limit
### **Message**
Usage limit shown without upgrade call-to-action.
### **Fix Action**
When showing limits, include clear upgrade CTA with value proposition
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - upgrade|Upgrade|subscribe

## Free Tier Without Clear Limits

### **Id**
free-tier-no-limits
### **Severity**
info
### **Type**
regex
### **Pattern**
  - plan\s*===\s*['"]free['"]
  - tier\s*===\s*['"]free['"]
  - isFree\s*=
### **Message**
Free tier detected. Ensure clear limits to drive conversion.
### **Fix Action**
Free tier should have: usage limits, feature gates, or time limits
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Plan Change Without Proration

### **Id**
missing-proration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - changePlan|updatePlan|upgradePlan
  - switchPlan|changeSubscription
### **Message**
Plan change without clear proration handling.
### **Fix Action**
Handle proration: credit remaining time on old plan toward new plan
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - prorat|credit

## Price Change Without Grandfathering Logic

### **Id**
grandfathering-not-handled
### **Severity**
info
### **Type**
regex
### **Pattern**
  - updatePrice|priceChange|newPricing
  - price.*update|pricing.*change
### **Message**
Price change logic without grandfathering existing customers.
### **Fix Action**
Add grandfathering: existing customers keep old price for X months
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - grandfather|legacy|existing

## Checkout Without Tax Consideration

### **Id**
checkout-no-tax-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - checkout\s*\(
  - createCheckout
  - Checkout.*Session
### **Message**
Checkout without tax handling. Required for many jurisdictions.
### **Fix Action**
Use Stripe Tax or similar for automatic tax calculation
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - tax|Tax|VAT|automatic_tax

## Pricing Config Not Version Controlled

### **Id**
pricing-config-unversioned
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pricing\s*=
  - plans\s*=
  - tiers\s*=
### **Message**
Pricing configuration should be versioned for price change management.
### **Fix Action**
Add version to pricing config and log changes in changelog
### **Applies To**
  - **/pricing*.ts
  - **/config/pricing*
  - **/constants/pricing*
### **Exceptions**
  - version|Version