# Marketing Fundamentals - Validations

## Feature-Focused Instead of Benefit-Focused

### **Id**
mkt-feature-focused-copy
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - features?:|our.?features|key.?features|feature.?list
  - we.?offer|we.?provide|we.?have|our.?platform
### **Message**
Feature-focused language detected. Users buy outcomes, not features. Lead with benefits.
### **Fix Action**
Transform: 'AI-powered' → 'Get answers in seconds'. 'Real-time sync' → 'Never lose work'
### **Applies To**
  - *.md
  - *.html
  - *.txt
  - *.json

## Missing Target Audience Definition

### **Id**
mkt-no-target-audience
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - everyone|anyone|all.?users|any.?business|all.?companies
### **Message**
Generic audience detected. If you are marketing to everyone, you are marketing to no one.
### **Fix Action**
Define specific ICP: job title, company size, pain point, current solution, budget
### **Applies To**
  - *.md
  - *.txt

## Marketing Jargon Overload

### **Id**
mkt-jargon-overload
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - synergy|leverage|holistic|paradigm|disrupt|revolutionary|game.?changing
  - best.?in.?class|world.?class|industry.?leading|cutting.?edge
### **Message**
Marketing jargon detected. These words mean nothing. Use specific, concrete language.
### **Fix Action**
Replace with specifics: 'industry-leading' → '2x faster than Competitor' or delete entirely
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Claims Without Social Proof

### **Id**
mkt-no-social-proof
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - trusted|reliable|proven|loved|popular
### **Message**
Trust claim without proof. Saying you are trusted is not the same as proving it.
### **Fix Action**
Add evidence: '10,000 companies' → '10,847 companies including Stripe, Notion, Linear'
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Weak Call to Action

### **Id**
mkt-weak-cta
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - click.?here|learn.?more|submit|send
### **Message**
Weak CTA detected. Specific CTAs convert better than generic ones.
### **Fix Action**
Use outcome-focused CTAs: 'Start free trial' → 'Start building in 2 minutes'
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Differentiation

### **Id**
mkt-no-differentiation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - like.?other|similar.?to|just.?like|also.?offers
### **Message**
Similarity positioning detected. Why should someone choose you over alternatives?
### **Fix Action**
State difference clearly: 'Unlike X which does Y, we do Z because...'
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Vanity Metrics in Marketing

### **Id**
mkt-vanity-metric
### **Severity**
info
### **Type**
regex
### **Pattern**
  - impressions|views|visits|followers|downloads
### **Message**
Vanity metric mentioned. These do not correlate with business outcomes.
### **Fix Action**
Focus on business metrics: revenue, paying customers, retention, NPS
### **Applies To**
  - *.md
  - *.txt

## Missing Urgency or Scarcity

### **Id**
mkt-no-urgency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - whenever|anytime|no.?rush|take.?your.?time
### **Message**
No urgency detected. Without urgency, decisions get delayed indefinitely.
### **Fix Action**
Add genuine urgency: limited seats, price increase, beta access, launch date
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Unclear Value Proposition

### **Id**
mkt-unclear-value-prop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - platform|solution|tool|software|system|application
### **Message**
Generic product descriptor detected. What does it actually DO for the customer?
### **Fix Action**
Lead with outcome: '[Tool] helps [who] [achieve what] by [how]'
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Objection Handling

### **Id**
mkt-no-objection-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pricing|buy|purchase|subscribe|sign.?up
### **Message**
Purchase intent page without objection handling. Address concerns before they become blockers.
### **Fix Action**
Add FAQ, risk reversal (money back guarantee), or comparison chart
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Inside-Out Company Language

### **Id**
mkt-inside-out-language
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - our.?mission|our.?vision|our.?values|we.?believe|our.?story
### **Message**
Company-centric language on customer-facing page. Customers care about their problems, not your mission.
### **Fix Action**
Lead with customer pain, not company story. Save mission for About page.
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Multiple Competing CTAs

### **Id**
mkt-multiple-ctas
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?:button|btn|cta).*(?:button|btn|cta).*(?:button|btn|cta)
### **Message**
Multiple CTAs detected. Too many choices leads to no choice.
### **Fix Action**
One primary CTA per page. Secondary actions should be visually subordinate.
### **Applies To**
  - *.html
  - *.tsx
  - *.jsx