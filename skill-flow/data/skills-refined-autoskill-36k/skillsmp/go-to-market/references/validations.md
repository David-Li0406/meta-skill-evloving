# Go To Market - Validations

## Launch Without Analytics

### **Id**
missing-analytics-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - launch|Launch|release|Release
  - production|Production
  - deploy|Deploy
### **Message**
Launch/deployment code without visible analytics setup.
### **Fix Action**
Ensure analytics tracking (Mixpanel, Amplitude, GA) is set up before launch
### **Applies To**
  - **/index.tsx
  - **/app.tsx
  - **/main.tsx
### **Exceptions**
  - analytics|Analytics|mixpanel|amplitude|segment|gtag|track

## Signup Without Conversion Tracking

### **Id**
no-conversion-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createAccount
  - onSubmit.*form|handleSubmit
### **Message**
User signup without conversion tracking.
### **Fix Action**
Add conversion event tracking for signup funnel analysis
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - track|conversion|event|analytics|gtag

## Signup Without Referral Attribution

### **Id**
no-referral-attribution
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createUser
### **Message**
User signup without referral attribution tracking.
### **Fix Action**
Track utm_source, referral codes, and attribution for channel analysis
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - utm|referral|source|attribution|ref=|campaign

## Onboarding Without Tracking

### **Id**
missing-onboarding-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - onboarding|Onboarding|welcome|Welcome
  - getStarted|getting-started
### **Message**
Onboarding flow without step completion tracking.
### **Fix Action**
Track each onboarding step for funnel analysis and drop-off identification
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - track|step|progress|complete|analytics

## User Creation Without Activation Tracking

### **Id**
no-activation-metric
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createUser|newUser|registerUser
  - first.*login|firstLogin
### **Message**
User creation without activation metric tracking.
### **Fix Action**
Define and track activation metric (key value moment)
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - activated|activation|milestone|valueRealized

## Team Feature Without Invite Flow

### **Id**
no-invite-mechanism
### **Severity**
info
### **Type**
regex
### **Pattern**
  - team|Team|workspace|Workspace
  - organization|Organization|org
### **Message**
Team/workspace feature without visible invite mechanism.
### **Fix Action**
Add team invite flow for product-led expansion
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - invite|Invite|addMember|joinTeam

## Trial Without Usage Tracking

### **Id**
no-trial-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - trial|Trial|freeTrial
  - trialEnd|trialExpir
### **Message**
Trial functionality without usage tracking.
### **Fix Action**
Track trial engagement to identify conversion likelihood
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - track|usage|engaged|activity

## Upgrade CTA Without Trigger Context

### **Id**
upgrade-without-trigger
### **Severity**
info
### **Type**
regex
### **Pattern**
  - upgrade|Upgrade|premium|Premium
  - pricing|Pricing|plans|Plans
### **Message**
Upgrade prompts without contextual trigger tracking.
### **Fix Action**
Track what triggered upgrade interest for PQL analysis
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - track|trigger|source|reason|context

## Feature Without Feature Flag

### **Id**
no-feature-flag-for-launch
### **Severity**
info
### **Type**
regex
### **Pattern**
  - newFeature|NewFeature|feature.*launch
  - experimentalFeature|betaFeature
### **Message**
New feature without feature flag for controlled rollout.
### **Fix Action**
Use feature flags for gradual rollout and easy rollback
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - featureFlag|launchDarkly|unleash|flagsmith|growthbook

## Product Without Self-Serve Path

### **Id**
no-self-serve-path
### **Severity**
info
### **Type**
regex
### **Pattern**
  - demo|Demo|contact.*sales
  - scheduleCall|bookDemo
### **Message**
Demo/sales path without visible self-serve alternative.
### **Fix Action**
Offer self-serve option for PLG alongside sales path
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - freeTrial|selfServe|tryFree|getStarted

## Pricing Display Without Clear CTA

### **Id**
pricing-page-no-cta
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pricing|Pricing|price|Price
  - plan|Plan|tier|Tier
### **Message**
Pricing display without clear call-to-action.
### **Fix Action**
Add clear CTA buttons for each pricing tier
### **Applies To**
  - **/pricing*.tsx
  - **/plans*.tsx
### **Exceptions**
  - button|Button|cta|CTA|onClick|subscribe

## Coming Soon Without Waitlist

### **Id**
no-waitlist-mechanism
### **Severity**
info
### **Type**
regex
### **Pattern**
  - comingSoon|coming-soon|launching.*soon
  - notYetAvailable|underConstruction
### **Message**
Coming soon page without email capture.
### **Fix Action**
Add waitlist signup to capture interested users for launch
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - waitlist|email|subscribe|notify|signup

## Landing Page Without Social Proof

### **Id**
no-social-proof
### **Severity**
info
### **Type**
regex
### **Pattern**
  - hero|Hero|landing|Landing
  - homepage|HomePage
### **Message**
Landing/hero section without social proof elements.
### **Fix Action**
Add testimonials, logos, or user count for credibility
### **Applies To**
  - **/hero*.tsx
  - **/landing*.tsx
  - **/home*.tsx
### **Exceptions**
  - testimonial|logo|users|customers|trusted

## CTA Without Urgency

### **Id**
no-urgency-element
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signUp|getStarted|startTrial
  - subscribe|Subscribe
### **Message**
Sign up CTA without urgency or value reinforcement.
### **Fix Action**
Add value proposition or urgency near CTAs
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - free|instant|today|now|immediately|trial

## Checkout Without Trust Elements

### **Id**
checkout-no-guarantee
### **Severity**
info
### **Type**
regex
### **Pattern**
  - checkout|Checkout|payment|Payment
  - purchase|Purchase|buy|Buy
### **Message**
Checkout flow without trust/guarantee elements.
### **Fix Action**
Add money-back guarantee, security badges, or support info
### **Applies To**
  - **/checkout*.tsx
  - **/payment*.tsx
### **Exceptions**
  - guarantee|refund|secure|ssl|support|help

## Cancellation Without Reason Tracking

### **Id**
no-churn-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - cancel|Cancel|unsubscribe|Unsubscribe
  - deleteAccount|closeAccount
### **Message**
Cancellation flow without churn reason tracking.
### **Fix Action**
Add exit survey to understand churn reasons
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - reason|survey|feedback|why|churnReason