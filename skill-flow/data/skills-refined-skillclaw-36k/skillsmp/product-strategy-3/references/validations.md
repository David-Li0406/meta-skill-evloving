# Product Strategy - Validations

## No User Problem Defined

### **Id**
product-no-problem
### **Severity**
error
### **Type**
regex
### **Pattern**
  - feature|build|create|develop|product
### **Message**
Product work without defined user problem. What pain are you solving? For whom? Be specific.
### **Fix Action**
Define the problem: What struggle do users have? How painful? How frequent? How do they cope today?
### **Applies To**
  - *.md
  - *.txt
  - README*

## Feature-Focused Strategy

### **Id**
product-feature-list
### **Severity**
error
### **Type**
regex
### **Pattern**
  - features.?include|will.?have|functionality|capabilities|includes
### **Message**
Feature list as strategy. Features are not strategy. Strategy is choosing what problems to solve and why.
### **Fix Action**
Focus on outcomes: What can users achieve? What jobs does this help them do? Why does it matter?
### **Applies To**
  - *.md
  - *.txt

## No Product Success Criteria

### **Id**
product-no-success-criteria
### **Severity**
error
### **Type**
regex
### **Pattern**
  - launch|ship|release|build
### **Message**
Shipping without success criteria. How will you know if it worked? Define metrics before building.
### **Fix Action**
Set criteria: usage metric, retention target, revenue goal, NPS score? Make success measurable.
### **Applies To**
  - *.md
  - *.txt

## Competitor Feature Copycat

### **Id**
product-competitor-copycat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - competitor.?has|they.?offer|other.?products|everyone.?else|industry.?standard
### **Message**
Building features because competitors have them. Copying is not strategy. It's the opposite of differentiation.
### **Fix Action**
Ask: Does this solve OUR users' problem uniquely? Or are we just following? Lead, don't follow.
### **Applies To**
  - *.md
  - *.txt

## No User Validation Plan

### **Id**
product-no-validation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - idea|concept|hypothesis|assumption
### **Message**
Product idea without validation plan. Ideas are cheap. Evidence is valuable. How will you test this?
### **Fix Action**
Plan validation: Who will you talk to? What will you build to test? What evidence proves/disproves this?
### **Applies To**
  - *.md
  - *.txt

## Kitchen Sink Product

### **Id**
product-kitchen-sink
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - everything|all.?in.?one|complete.?solution|full.?suite|comprehensive|end.?to.?end
### **Message**
Trying to do everything. Products that do everything serve no one well. What is your core value?
### **Fix Action**
Cut ruthlessly: What ONE thing will you be the best at? What will you NOT do? Focus creates value.
### **Applies To**
  - *.md
  - *.txt

## No Product Tradeoffs

### **Id**
product-no-tradeoffs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - and|also|plus|in.?addition|as.?well.?as
### **Message**
No tradeoffs mentioned. Every product decision is a tradeoff. What are you optimizing for? What are you sacrificing?
### **Fix Action**
Be explicit: Fast OR perfect? Simple OR powerful? Cheap OR premium? Choose. Tradeoffs define products.
### **Applies To**
  - *.md
  - *.txt

## No MVP Definition

### **Id**
product-no-mvp
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - minimum|mvp|first.?version|initial|v1
### **Message**
MVP mentioned without clear scope. What's the MINIMUM that proves value? Not minimum everything.
### **Fix Action**
Define MVP: smallest thing that solves core problem for early users. One job, done well. Ship that first.
### **Applies To**
  - *.md
  - *.txt

## Trying to Boil the Ocean

### **Id**
product-boil-ocean
### **Severity**
error
### **Type**
regex
### **Pattern**
  - platform|marketplace|ecosystem|network|infrastructure
### **Message**
Platform/marketplace as V1. These require network effects. Impossible to bootstrap. Start smaller.
### **Fix Action**
Start single-player: What value can one user get alone? Build that first. Layer on network effects later.
### **Applies To**
  - *.md
  - *.txt

## No Delivery Timeline

### **Id**
product-no-timeline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - build|develop|create|ship|launch
### **Message**
Product work without timeline. How long will this take? When will users see value? Be realistic.
### **Fix Action**
Set timeline: What ships in 2 weeks? 1 month? 3 months? Break into phases. Ship early and often.
### **Applies To**
  - *.md
  - *.txt

## Technology-First Strategy

### **Id**
product-technology-first
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - using|powered.?by|built.?with|blockchain|ai|ml|tech.?stack
### **Message**
Technology-first thinking. Users don't care about your tech stack. They care about their problems solved.
### **Fix Action**
Lead with value: What can users do? What outcome do they get? Technology is implementation detail.
### **Applies To**
  - *.md
  - *.txt

## No User Research Evidence

### **Id**
product-no-user-research
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - users.?want|users.?need|customers.?are.?asking|demand.?for
### **Message**
User needs claimed without research evidence. How do you know? Who did you talk to? Show your work.
### **Fix Action**
Add evidence: X users said Y. Usage data shows Z. Support tickets mention A. Real data, not assumptions.
### **Applies To**
  - *.md
  - *.txt