# Idea Maze - Validations

## No Market Analysis

### **Id**
idea-maze-no-market
### **Severity**
error
### **Type**
regex
### **Pattern**
  - idea|concept|startup|business|product
### **Message**
Idea without market analysis. Who is this for? How big is that market? Are they spending money on this problem?
### **Fix Action**
Research market: size, growth, existing spend, customer segments. Is this a vitamin or painkiller?
### **Applies To**
  - *.md
  - *.txt
  - README*

## No Competitor Research

### **Id**
idea-maze-no-competitors
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new|novel|first|unique|no.?one.?else
### **Message**
Claiming uniqueness without competitor research. 'No competition' usually means no market or you didn't look hard enough.
### **Fix Action**
Map competitors: direct, indirect, substitute solutions. Why did previous attempts fail? What changed now?
### **Applies To**
  - *.md
  - *.txt

## No Customer Validation

### **Id**
idea-maze-no-customer-validation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - people.?would|customers.?will|users.?want|market.?needs
### **Message**
Customer needs assumed, not validated. Talking to customers is not optional. Do it before building.
### **Fix Action**
Talk to 20+ potential customers. Ask about their problem, not your solution. What do they pay for today?
### **Applies To**
  - *.md
  - *.txt

## Solution Before Problem

### **Id**
idea-maze-solution-first
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - using|built.?with|powered.?by|leveraging|blockchain|ai
### **Message**
Leading with solution/technology. Start with problem. Technology is how you solve it, not why.
### **Fix Action**
Flip it: What's the painful problem? Who has it? How do they cope now? Then: how might we solve it?
### **Applies To**
  - *.md
  - *.txt

## No Defensibility Analysis

### **Id**
idea-maze-no-moat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - idea|concept|business
### **Message**
No defensibility mentioned. What stops someone with more resources from copying you and winning?
### **Fix Action**
Define moat: network effects, data advantage, brand, regulation, switching costs? Pick one to build.
### **Applies To**
  - *.md
  - *.txt

## No Timing Thesis

### **Id**
idea-maze-no-timing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - now|today|currently|market|opportunity
### **Message**
No explanation of why now. Every successful startup has a timing thesis. What changed to make this possible?
### **Fix Action**
Why now thesis: new technology, regulation, behavior shift, cost reduction? What's the unlock?
### **Applies To**
  - *.md
  - *.txt

## No Business Model

### **Id**
idea-maze-no-business-model
### **Severity**
error
### **Type**
regex
### **Pattern**
  - monetize|revenue|make.?money|business.?model
### **Message**
Unclear how you'll make money. 'We'll figure it out later' is not a plan. How do customers pay you?
### **Fix Action**
Define model: subscription, transaction fee, ads, enterprise? What's the unit of value? Price point?
### **Applies To**
  - *.md
  - *.txt

## No Go-To-Market Strategy

### **Id**
idea-maze-no-go-to-market
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - launch|customers|users|growth
### **Message**
No GTM strategy. How will first 100 customers find you? Be specific. 'Marketing' is not an answer.
### **Fix Action**
Map first customers: Where do they hang out? What do they read? Who do they trust? Start there.
### **Applies To**
  - *.md
  - *.txt

## Assuming Viral Growth

### **Id**
idea-maze-viral-assumption
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - viral|word.?of.?mouth|organic|naturally|spread
### **Message**
Assuming viral growth. Products don't go viral by accident. What's the sharing mechanic? Why would users share?
### **Fix Action**
Design sharing: What value does sharer get? What value does recipient get? Test this explicitly.
### **Applies To**
  - *.md
  - *.txt

## Pursuing Multiple Ideas Simultaneously

### **Id**
idea-maze-multiple-ideas
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - or|alternatively|could.?also|another.?idea|different.?approach
### **Message**
Multiple ideas in parallel. Splitting focus kills execution. Pick one, go deep, learn fast.
### **Fix Action**
Choose ONE idea to validate first. Set timeline (e.g., 6 weeks). Then evaluate: continue, pivot, or new idea.
### **Applies To**
  - *.md
  - *.txt

## No Unfair Advantage Identified

### **Id**
idea-maze-no-unfair-advantage
### **Severity**
info
### **Type**
regex
### **Pattern**
  - advantage|edge|differentiation|unique
### **Message**
No unfair advantage mentioned. What do you have that others don't? Domain expertise, network, insight, access?
### **Fix Action**
Identify advantage: unique insight, technical skill, industry access, personal brand? Lean into it.
### **Applies To**
  - *.md
  - *.txt

## Pivoting Too Quickly

### **Id**
idea-maze-pivot-too-fast
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new.?idea|different.?direction|try.?something.?else|pivot
### **Message**
Pivoting before learning. How long did you try? What did you learn? Persistence vs. stubbornness line is thin.
### **Fix Action**
Document learnings: What worked? What didn't? Why? What would you change? Learn, then pivot with evidence.
### **Applies To**
  - *.md
  - *.txt