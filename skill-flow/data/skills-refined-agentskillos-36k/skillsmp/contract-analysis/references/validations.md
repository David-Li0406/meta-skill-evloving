# Contract Analysis - Validations

## Missing Liability Cap

### **Id**
no-liability-cap
### **Severity**
error
### **Type**
regex
### **Pattern**
  - indemnif.*(?!limit|cap|not exceed|maximum)
  - liable.*(?!limit|cap|exceed)
### **Message**
Indemnification or liability clause may lack cap.
### **Fix Action**
Add liability cap tied to contract value
### **Applies To**
  - **/*contract*.txt
  - **/*agreement*.txt

## Unlimited Liability Language

### **Id**
unlimited-language
### **Severity**
error
### **Type**
regex
### **Pattern**
  - unlimited liability
  - any and all.*damages
  - shall be liable for.*without limit
### **Message**
Contract contains unlimited liability language.
### **Fix Action**
Negotiate for reasonable caps
### **Applies To**
  - **/*contract*.txt

## No Termination for Convenience

### **Id**
no-termination-convenience
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - terminat.*(?!convenience)
### **Message**
Review if termination for convenience is available.
### **Fix Action**
Add termination for convenience with reasonable notice
### **Applies To**
  - **/*contract*.txt

## Automatic Renewal Clause

### **Id**
auto-renewal
### **Severity**
info
### **Type**
regex
### **Pattern**
  - auto.*renew
  - automatically.*extend
  - successive.*term
### **Message**
Contract has auto-renewal. Note cancellation window.
### **Fix Action**
Calendar cancellation deadline
### **Applies To**
  - **/*contract*.txt

## Data Processing Without DPA

### **Id**
no-dpa
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - personal data|customer data(?!.*data processing|.*dpa|.*addendum)
### **Message**
Contract involves data but may lack Data Processing Addendum.
### **Fix Action**
Add DPA with breach notification and security requirements
### **Applies To**
  - **/*contract*.txt

## Broad IP Assignment Language

### **Id**
broad-ip-assignment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - assigns? all.*right.*title.*interest
  - work product.*belongs to
### **Message**
Review IP assignment scope - may include background IP.
### **Fix Action**
Carve out background IP and define work product narrowly
### **Applies To**
  - **/*contract*.txt