# Business Model Design - Validations

## Missing Revenue Model

### **Id**
no-revenue-model
### **Severity**
high
### **Type**
conceptual
### **Check**
Business must have defined revenue model
### **Message**
No clear revenue model defined.
### **Fix Action**
Define how the business will make money

## Negative Unit Economics

### **Id**
bad-unit-economics
### **Severity**
high
### **Type**
conceptual
### **Check**
Unit economics should be positive or have clear path
### **Indicators**
  - LTV:CAC < 2:1
  - No path to profitability
### **Message**
Unit economics are not viable.
### **Fix Action**
Fix CAC, churn, or ARPU before scaling

## Unclear Value Proposition

### **Id**
no-value-proposition
### **Severity**
high
### **Type**
conceptual
### **Check**
Value proposition must be clearly articulated
### **Indicators**
  - Can't explain value in one sentence
  - No differentiation
### **Message**
Value proposition not clear.
### **Fix Action**
Define clear value proposition and differentiation

## Revenue Model Doesn't Fit Market

### **Id**
model-market-mismatch
### **Severity**
medium
### **Type**
conceptual
### **Check**
Revenue model should match how customers want to buy
### **Message**
Revenue model may not fit customer expectations.
### **Fix Action**
Research how customers buy and align model

## Too Complex Business Model

### **Id**
overcomplicated-model
### **Severity**
medium
### **Type**
conceptual
### **Check**
Business model should be simple and understandable
### **Indicators**
  - More than 5 pricing tiers
  - Many add-on options
### **Message**
Business model too complex.
### **Fix Action**
Simplify to 3 tiers maximum

## Cost Structure Not Understood

### **Id**
no-cost-structure
### **Severity**
medium
### **Type**
conceptual
### **Check**
Cost structure should be clearly mapped
### **Message**
Cost structure not well understood.
### **Fix Action**
Map fixed and variable costs clearly