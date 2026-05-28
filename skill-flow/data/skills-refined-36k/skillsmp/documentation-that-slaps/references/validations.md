# Documentation That Slaps - Validations

## Missing Quick Start

### **Id**
no-quick-start
### **Severity**
high
### **Type**
conceptual
### **Check**
README should have immediate quick start
### **Indicators**
  - No installation section
  - No getting started
  - Explanation before example
### **Message**
No quick start in documentation.
### **Fix Action**
Add 3-step or less quick start at top

## Missing Code Examples

### **Id**
no-examples
### **Severity**
medium
### **Type**
conceptual
### **Check**
Documentation should show examples
### **Indicators**
  - All prose, no code
  - Describes but doesn't show
  - No copy-pasteable snippets
### **Message**
Missing code examples.
### **Fix Action**
Add working, copy-pasteable examples

## Outdated Documentation

### **Id**
stale-docs
### **Severity**
high
### **Type**
conceptual
### **Check**
Documentation should match current code
### **Indicators**
  - Old version numbers
  - Deprecated APIs documented
  - No last-updated date
### **Message**
Documentation may be outdated.
### **Fix Action**
Verify accuracy, add last-verified date

## Unowned Documentation

### **Id**
no-owner
### **Severity**
medium
### **Type**
conceptual
### **Check**
Documentation should have a maintainer
### **Indicators**
  - No one responsible
  - Unknown who wrote it
  - No review process
### **Message**
Documentation has no owner.
### **Fix Action**
Assign maintainer, add review schedule

## Too Much Jargon

### **Id**
jargon-heavy
### **Severity**
low
### **Type**
conceptual
### **Check**
Documentation should be accessible
### **Indicators**
  - Undefined terms
  - Acronyms not explained
  - Assumes expert knowledge
### **Message**
Documentation may be too technical.
### **Fix Action**
Define terms, add prerequisites section

## Missing Error Documentation

### **Id**
no-error-docs
### **Severity**
medium
### **Type**
conceptual
### **Check**
Errors should be documented with solutions
### **Indicators**
  - Error codes not explained
  - No troubleshooting section
  - Errors not searchable
### **Message**
Error documentation missing.
### **Fix Action**
Document errors with causes and solutions