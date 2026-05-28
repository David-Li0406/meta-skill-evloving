# Execution Algorithms - Validations

## Slippage Modeling Required

### **Id**
check-slippage-modeling
### **Description**
Execution code must include realistic slippage estimates
### **Pattern**
order|execute|trade|fill
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
slippage|impact|cost
### **Message**
Include realistic slippage/impact modeling in execution logic
### **Severity**
error
### **Autofix**


## Market Order Size Check

### **Id**
check-market-order-size
### **Description**
Large market orders should be flagged
### **Pattern**
market.*order|marketOrder|type.*market
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Message**
Market orders on large sizes cause significant slippage - consider splitting
### **Severity**
warning
### **Autofix**


## Participation Rate Limits

### **Id**
check-participation-rate
### **Description**
Trading should respect volume participation limits
### **Pattern**
volume|adv|participation
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
order|trade|execute
### **Message**
Track participation rate - exceeding 5-10% of volume causes impact
### **Severity**
warning
### **Autofix**


## Timing Randomization

### **Id**
check-order-timing-randomization
### **Description**
Execution timing should be randomized to prevent gaming
### **Pattern**
random|jitter|noise
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
execute|schedule|twap|vwap
### **Message**
Add timing randomization to prevent execution pattern detection
### **Severity**
info
### **Autofix**


## Fill Quality Tracking

### **Id**
check-fill-tracking
### **Description**
Execution should track fill quality metrics
### **Pattern**
fill.*rate|slippage.*track|execution.*quality
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
execute|order
### **Message**
Track fill quality metrics for execution analysis
### **Severity**
info
### **Autofix**


## Multi-Venue Routing

### **Id**
check-venue-selection
### **Description**
Orders should consider multiple venues
### **Pattern**
venue|exchange|route
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
order|execute
### **Message**
Consider smart order routing across multiple venues
### **Severity**
info
### **Autofix**


## Overfill Prevention

### **Id**
check-overfill-prevention
### **Description**
Multi-leg execution needs overfill protection
### **Pattern**
pending|outstanding|overfill
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
slice|child|parent.*order
### **Message**
Implement overfill prevention when splitting orders
### **Severity**
warning
### **Autofix**


## Cancel and Replace Logic

### **Id**
check-cancel-logic
### **Description**
Stale orders should be cancelled
### **Pattern**
cancel|timeout|stale
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
limit.*order|resting
### **Message**
Implement cancel logic for stale limit orders
### **Severity**
info
### **Autofix**


## Latency Over-Optimization Warning

### **Id**
check-latency-not-overoptimized
### **Description**
Non-HFT should not over-optimize for latency
### **Pattern**
microsecond|nanosecond|latency.*critical
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Message**
Unless HFT, focus on algo quality over microsecond latency
### **Severity**
info
### **Autofix**
