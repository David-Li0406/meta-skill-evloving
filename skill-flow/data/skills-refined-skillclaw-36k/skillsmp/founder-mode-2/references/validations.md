# Founder Mode - Validations

## Avoiding Delegation

### **Id**
founder-delegation-avoidance
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(I'll|I will|I am)\s+(do|handle|take care of|work on)\s+(everything|all|it all)
  - (?i)can't\s+(trust|delegate|hand off)
### **Message**
Avoiding delegation. Identify tasks only you can do vs. tasks others should own.
### **Fix Action**
List: 'Only I can do: X, Y. Should delegate: A, B, C to [person]'
### **Applies To**
  - **/*.md

## Tasks Without Deadlines

### **Id**
founder-no-deadlines
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(TODO|task|action item|next step)\s*:(?!.*by\s+\d|.*deadline|.*due)
### **Message**
Task without deadline. Founder mode means setting aggressive, specific timelines.
### **Fix Action**
Add deadline: 'TODO: [task] by EOD Friday' or 'Ship by Monday 9 AM'
### **Applies To**
  - **/*.md

## Perfectionism Over Shipping

### **Id**
founder-perfectionism
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(perfect|polish|refine|finalize)\s+before\s+(launch|ship|release)
  - (?i)not\s+(ready|good\s+enough|polished)\s+to\s+ship
### **Message**
Perfectionism blocking shipping. Founder mode: ship, learn, iterate.
### **Fix Action**
Set ship date: 'Launch MVP by [date], improve based on user feedback'
### **Applies To**
  - **/*.md

## Seeking Consensus Over Deciding

### **Id**
founder-consensus-seeking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)let's\s+(vote|discuss|see what everyone thinks|get alignment)
  - (?i)waiting\s+for\s+(everyone|team|approval)
### **Message**
Seeking consensus delays decisions. Make the call, explain, move forward.
### **Fix Action**
Decide: 'Decision: X. Rationale: Y. Effective: [date]'
### **Applies To**
  - **/*.md

## Reactive Instead of Proactive

### **Id**
founder-reactive-mode
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?i)(responding to|reacting to|dealing with)\s+(issues|problems|fires)
  - (?i)spent\s+(day|week)\s+on\s+(slack|email|meetings)
### **Message**
Reactive mode detected. Block time for proactive work on strategy/product.
### **Fix Action**
Schedule: 'Mon/Wed 9-12: Deep work on [core priority]. No meetings.'
### **Applies To**
  - **/*.md

## Not Tracking Key Metrics

### **Id**
founder-no-metrics-tracking
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(metrics|kpis?|goals?)(?!.*\d+|.*target|.*baseline|.*current)
### **Message**
Metrics mentioned but not tracked with numbers. Founder mode: measure everything.
### **Fix Action**
Add: 'Current: X, Target: Y by [date], Tracking: [tool/sheet]'
### **Applies To**
  - **/*.md

## Vague Priorities

### **Id**
founder-vague-priorities
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)priority:?\s+(grow|improve|fix|build)(?!.*by\s+\d|.*to\s+\d)
### **Message**
Priority lacks specificity. Define exact outcome and timeline.
### **Fix Action**
Clarify: 'Priority: Grow from X to Y users by [date] via [channel]'
### **Applies To**
  - **/*.md

## Not Talking to Customers

### **Id**
founder-no-customer-contact
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)(week|sprint)(?!.*customer|.*user\s+interview|.*feedback\s+call)
### **Message**
No customer interaction mentioned. Founders must stay close to users weekly.
### **Fix Action**
Schedule: '3 customer calls/week, log insights in [location]'
### **Applies To**
  - **/*.md

## Blaming External Factors

### **Id**
founder-blame-external
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(because|due to)\s+(market|economy|competition|timing)(?!.*but we)
  - (?i)if\s+only\s+(we had|there was)
### **Message**
Blaming external factors. Founder mode: focus on what you can control.
### **Fix Action**
Reframe: 'Given X constraint, we will Y to achieve Z'
### **Applies To**
  - **/*.md

## No Regular Review Cadence

### **Id**
founder-no-review-process
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(week|month|quarter)(?!.*review|.*retro|.*reflection)
### **Message**
No review process. Set weekly/monthly reviews to assess progress.
### **Fix Action**
Add: 'Weekly review: Fri 4pm - metrics, wins, blockers, next week plan'
### **Applies To**
  - **/*.md

## Busy vs Productive

### **Id**
founder-busy-not-productive
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (?i)(busy|swamped|overwhelmed)\s+with\s+(meetings|email|calls)
### **Message**
Busy doesn't mean productive. Audit time: are you working on highest leverage tasks?
### **Fix Action**
Time audit: List tasks by impact. Cut/delegate bottom 50%.
### **Applies To**
  - **/*.md

## No Forcing Function

### **Id**
founder-no-forcing-function
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (?i)(launch|ship|release)(?!.*demo day|.*customer|.*deadline|.*date)
### **Message**
No forcing function for launch. Set external commitment: demo, customer, deadline.
### **Fix Action**
Create forcing function: 'Demo to 10 customers on [date]' or 'Announce publicly [date]'
### **Applies To**
  - **/*.md