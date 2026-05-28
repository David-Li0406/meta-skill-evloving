# Marketing - Validations

## Focus on Vanity Metrics

### **Id**
marketing-vanity-metrics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?i)(?:page views|impressions|followers|likes)\b(?!.*\b(?:conversion|revenue|ROI|retention|LTV|CAC|engagement rate|qualified leads)\b)
### **Message**
Focusing on vanity metrics without connecting to business outcomes
### **Fix Action**
Tie metrics to business outcomes: conversion rate, customer acquisition cost, lifetime value, or revenue
### **Applies To**
  - *.md
  - *.html
  - *.txt

## No Clear Target Audience

### **Id**
marketing-unclear-audience
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:for|targeting|audience|customer|user|designed for|built for|ideal for|perfect for|helps? \w+ who)).*$
### **Message**
No clear target audience identified - message may be too generic
### **Fix Action**
Explicitly define who this is for: 'For [specific audience] who [specific problem/goal]'
### **Applies To**
  - *.md
  - *.html

## Feature-Focused Instead of Benefit-Driven

### **Id**
marketing-feature-over-benefit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)\b(?:we offer|we provide|includes|comes with|features)\b(?!.*\b(?:so you can|helps? you|enables? you|get|achieve|save|increase|reduce)\b)
### **Message**
Leading with features instead of benefits and outcomes
### **Fix Action**
Lead with benefits first, then explain features as supporting proof: 'Save 10 hours/week [benefit] with automated reporting [feature]'
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Competitive Differentiation

### **Id**
marketing-no-differentiation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:unlike|different|only|unique|exclusively|first|fastest|easiest|best|most|never|always|compared to|alternative to)).*$
### **Message**
No clear differentiation from competitors - may blend into market noise
### **Fix Action**
Highlight what makes you unique, different, or better than alternatives
### **Applies To**
  - *.md
  - *.html

## Weak or Missing Call-to-Action

### **Id**
marketing-weak-cta
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)\b(?:click here|submit|learn more|read more)\b
  - ^(?!.*(?i)(?:get|start|try|download|join|register|subscribe|buy|shop|book|request|claim|discover)).*$
### **Message**
CTA is weak, generic, or missing - reduces conversion potential
### **Fix Action**
Use specific, action-oriented CTAs that describe the value: 'Get Your Free Guide', 'Start Your 14-Day Trial'
### **Applies To**
  - *.md
  - *.html

## Missing Urgency or Scarcity Elements

### **Id**
marketing-no-urgency-scarcity
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:limited|deadline|expires|today|now|only \d+|last chance|while supplies|spots? left|ends|hurry|don't miss|running out)).*$
### **Message**
No urgency or scarcity triggers detected - may reduce immediate action
### **Fix Action**
Add time-bound offers or limited availability to motivate immediate action (use ethically)
### **Applies To**
  - *.md
  - *.html

## Missing Credibility Indicators

### **Id**
marketing-no-proof-credibility
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:trusted by|used by|\d+\+? (?:customers|companies|users)|award|certified|featured in|as seen|guarantee|money-back|risk-free|proven|verified)).*$
### **Message**
No trust or credibility indicators detected - may reduce conversion confidence
### **Fix Action**
Add social proof, certifications, guarantees, or media mentions to build trust
### **Applies To**
  - *.md
  - *.html

## Industry Jargon Without Explanation

### **Id**
marketing-industry-jargon
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(?i)(?:API|SDK|SaaS|B2B|B2C|ROI|KPI|CRM|CMS|SEO|PPC|CTR|CPM|CAC|LTV|MRR|ARR)\b(?!.*(?:,|\(|means|is|refers to))
### **Message**
Industry acronyms or jargon used without explanation - may confuse audience
### **Fix Action**
Either explain acronyms on first use or replace with plain language your audience understands
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Missing Problem Statement

### **Id**
marketing-no-problem-statement
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:problem|challenge|struggle|difficult|frustrat|pain|issue|obstacle|tired of|sick of|wish you could|what if you)).*$
### **Message**
No clear problem statement - audience may not understand why they need this
### **Fix Action**
Start by articulating the problem or pain point your audience experiences before presenting the solution
### **Applies To**
  - *.md
  - *.html

## No Objection Handling

### **Id**
marketing-missing-objection-handling
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?i)(?:but|however|worry|concern|question|faq|wonder|think|afraid|hesitat|doubt|risk|guarantee|refund|cancel anytime|no credit card)).*$
### **Message**
No visible objection handling - potential concerns left unaddressed
### **Fix Action**
Anticipate and address common objections: price, time, complexity, risk (e.g., 'No credit card required', 'Cancel anytime')
### **Applies To**
  - *.md
  - *.html

## Generic Non-Personalized Messaging

### **Id**
marketing-no-personalization
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \b(?i)(?:everyone|anyone|all|users?|customers?|people|businesses?)\b(?!.*\b(?:you|your|specifically|particular|certain|individual)\b)
### **Message**
Generic messaging without personalization - may feel mass-produced
### **Fix Action**
Use 'you' language and segment messaging for specific audience personas or use cases
### **Applies To**
  - *.md
  - *.html
  - *.txt

## Single-Benefit Instead of Value Stacking

### **Id**
marketing-missing-value-stack
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:\n[-*+]\s|\n\d+\.\s|<li>)).*$
### **Message**
No value stacking detected - missing opportunity to compound perceived value
### **Fix Action**
List multiple benefits, features, or bonuses to build comprehensive value proposition
### **Applies To**
  - *.md
  - *.html

## Overly Complex Messaging

### **Id**
marketing-complex-messaging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - [^.!?]{100,}[.!?]
  - \b\w{16,}\b
### **Message**
Complex messaging detected - clarity beats cleverness in marketing
### **Fix Action**
Simplify message to pass the 'grandma test' - if grandma wouldn't understand it, rewrite it
### **Applies To**
  - *.md
  - *.html
  - *.txt