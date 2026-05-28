# Pivot Patterns - Validations

## Pivot Without Success Criteria

### **Id**
pivot-no-success-criteria
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pivot|new.?direction|change.?strategy|shift.?focus
### **Message**
Pivot mentioned but no success criteria defined. How will you know if the pivot worked?
### **Fix Action**
Define measurable criteria: what metrics, what thresholds, what timeframe to evaluate
### **Applies To**
  - *.md
  - *.txt
  - README*

## Pivot Without Evaluation Timeline

### **Id**
pivot-no-timeline
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - try|test|experiment|validate
### **Message**
Experiment mentioned without timeline. Experiments without deadlines become indefinite wandering.
### **Fix Action**
Set kill date: 'We will evaluate on [date] and decide to commit, iterate, or abandon'
### **Applies To**
  - *.md
  - *.txt

## Sunk Cost Reasoning Detected

### **Id**
pivot-sunk-cost-language
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - already.?invested|already.?built|too.?much.?time|come.?this.?far
### **Message**
Sunk cost language detected. Past investment is not a reason to continue. Evaluate future potential only.
### **Fix Action**
Ask: If starting fresh today with current knowledge, would we choose this path?
### **Applies To**
  - *.md
  - *.txt

## Pivot Without Customer Evidence

### **Id**
pivot-no-customer-evidence
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pivot|new.?direction|change.?strategy
### **Message**
Strategic change without customer evidence. Pivots should be driven by data, not intuition.
### **Fix Action**
Document: what customers said, usage data, churn reasons, willingness to pay signals
### **Applies To**
  - *.md
  - *.txt

## Pivot Without Killing Features

### **Id**
pivot-keep-everything
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - add|plus|also|additionally|in.?addition
### **Message**
Adding without removing detected. True pivots require focus. You cannot pivot while keeping everything.
### **Fix Action**
Define what you are stopping: features, segments, channels. Pivoting means choosing.
### **Applies To**
  - *.md
  - *.txt

## Pivot Without Runway Consideration

### **Id**
pivot-no-runway-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - pivot|new.?direction|change.?strategy
### **Message**
Pivot discussed without runway check. Pivots cost time and money. Do you have enough?
### **Fix Action**
Calculate: runway remaining, burn during pivot, time to new revenue. Can you afford this pivot?
### **Applies To**
  - *.md
  - *.txt

## Total Rebuild Pivot Risk

### **Id**
pivot-total-rebuild
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - start.?over|from.?scratch|rebuild|rewrite|complete.?new
### **Message**
Total rebuild language detected. Full rewrites are almost always wrong. Preserve what works.
### **Fix Action**
Identify reusable assets: tech, customers, learnings, relationships. Build on them.
### **Applies To**
  - *.md
  - *.txt

## Pivot Without Team Alignment

### **Id**
pivot-no-team-alignment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - decide|deciding|direction|strategy.?change
### **Message**
Strategic decision without team alignment process. Misaligned teams execute poorly.
### **Fix Action**
Ensure everyone understands: why pivoting, what changing, their new role, success criteria
### **Applies To**
  - *.md
  - *.txt

## Competitor-Driven Pivot

### **Id**
pivot-following-competitor
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - competitor|they.?are.?doing|market.?is.?moving|everyone.?else
### **Message**
Competitor-driven reasoning detected. Pivoting because competitors are doing X is follower strategy.
### **Fix Action**
Ground in your customer evidence. What do YOUR customers need that is unserved?
### **Applies To**
  - *.md
  - *.txt

## Pivot Without Stakeholder Communication

### **Id**
pivot-no-communication-plan
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - pivot|change.?direction|new.?strategy
### **Message**
Pivot without communication plan. Investors, customers, team all need to understand the change.
### **Fix Action**
Define communication: who to tell, what narrative, when to announce, how to handle questions
### **Applies To**
  - *.md
  - *.txt

## Assuming New Market is Easier

### **Id**
pivot-magic-market
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - easier.?market|better.?fit|more.?receptive|bigger.?opportunity
### **Message**
Grass is greener thinking detected. Every market has its own challenges. The new market is not easier, just different.
### **Fix Action**
Research new market deeply: competitors, barriers, customer acquisition cost, sales cycle
### **Applies To**
  - *.md
  - *.txt

## Discarding All Learnings

### **Id**
pivot-no-preservation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - start.?fresh|clean.?slate|forget|abandon.?everything
### **Message**
Discarding learnings language detected. Even failed experiments teach you something valuable.
### **Fix Action**
Document learnings: what worked, what did not, customer insights, technical assets to keep
### **Applies To**
  - *.md
  - *.txt