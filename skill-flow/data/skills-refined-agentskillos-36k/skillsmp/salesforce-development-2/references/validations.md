# Salesforce Development - Validations

## SOQL Query Inside Loop

### **Id**
soql-in-loop
### **Severity**
error
### **Description**
SOQL in loops causes governor limit exceptions with bulk data
### **Pattern**
  (for|while|do)\s*\([^)]*\)\s*\{[^}]*\[SELECT
  
### **Message**
SOQL query inside loop. Query once outside the loop and use a Map.
### **Autofix**


## DML Operation Inside Loop

### **Id**
dml-in-loop
### **Severity**
error
### **Description**
DML in loops hits 150 statement limit
### **Pattern**
  (for|while)\s*\([^)]*\)\s*\{[^}]*(insert|update|delete|upsert)\s+\w+;
  
### **Message**
DML operation inside loop. Collect records and perform single DML outside loop.
### **Autofix**


## HTTP Callout in Trigger

### **Id**
callout-in-trigger
### **Severity**
error
### **Description**
Synchronous triggers cannot make callouts
### **Pattern**
  trigger\s+\w+.*\{[^}]*(Http|HttpRequest|WebServiceCallout)
  
### **Message**
Callout in trigger. Use @future(callout=true) or Queueable with Database.AllowsCallouts.
### **Autofix**


## Potential SOQL Injection

### **Id**
soql-injection
### **Severity**
error
### **Description**
Dynamic SOQL with string concatenation is vulnerable
### **Pattern**
  Database\.query\s*\([^)]*\+
  
### **Anti Pattern**
  escapeSingleQuotes
  
### **Message**
Dynamic SOQL with concatenation. Use bind variables or String.escapeSingleQuotes().
### **Autofix**


## Missing WITH SECURITY_ENFORCED

### **Id**
missing-security-enforced
### **Severity**
warning
### **Description**
SOQL should enforce FLS/CRUD permissions
### **Pattern**
  \[SELECT[^]]+FROM\s+\w+(?!.*WITH\s+SECURITY_ENFORCED)[^]]*\]
  
### **Message**
SOQL without security enforcement. Add WITH SECURITY_ENFORCED.
### **Autofix**


## Hardcoded Salesforce ID

### **Id**
hardcoded-id
### **Severity**
warning
### **Description**
Record IDs differ between orgs
### **Pattern**
  ['"]0[0-9a-zA-Z]{14,17}['"]
  
### **Message**
Hardcoded Salesforce ID. Query by DeveloperName or ExternalId instead.
### **Autofix**


## Hardcoded Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Description**
Credentials must use Named Credentials or Custom Metadata
### **Pattern**
  (password|secret|apikey|api_key)\s*[:=]\s*['"][^'"]+['"]
  
### **Message**
Hardcoded credentials. Use Named Credentials or Custom Metadata.
### **Autofix**


## Direct DOM Manipulation in LWC

### **Id**
lwc-direct-dom
### **Severity**
warning
### **Description**
LWC uses shadow DOM, direct manipulation breaks encapsulation
### **Pattern**
  document\.(getElementById|querySelector|getElementsBy)
  
### **Message**
Direct DOM access in LWC. Use this.template.querySelector() or data binding.
### **Autofix**


## Reactive Property Without @track

### **Id**
lwc-missing-track
### **Severity**
info
### **Description**
Complex object properties need @track for reactivity
### **Pattern**
  this\.(\w+)\s*=\s*\{[^}]+\}(?!.*@track\s+\1)
  
### **Message**
Object assignment may need @track for reactivity (post-Spring '20 objects are auto-tracked).
### **Autofix**


## Wire Without Refresh After DML

### **Id**
lwc-wire-without-refresh
### **Severity**
warning
### **Description**
Cached wire data becomes stale after updates
### **Pattern**
  @wire.*\n.*await\s+\w+\(.*\)(?!.*refreshApex)
  
### **Message**
DML after @wire without refreshApex. Data may be stale.
### **Autofix**


## Business Logic in Trigger Body

### **Id**
logic-in-trigger
### **Severity**
warning
### **Description**
Triggers should delegate to handler classes
### **Pattern**
  trigger\s+\w+\s+on\s+\w+\s*\([^)]+\)\s*\{[\s\S]{200,}
  
### **Message**
Complex logic in trigger body. Use Trigger Handler pattern.
### **Autofix**


## Missing Recursion Prevention

### **Id**
missing-recursion-guard
### **Severity**
warning
### **Description**
Triggers updating same object can recurse infinitely
### **Pattern**
  trigger\s+(\w+)\s+on\s+(\w+).*after\s+(update|insert)[\s\S]*update\s+
  
### **Anti Pattern**
  (hasExecuted|recursion|static.*Boolean)
  
### **Message**
Trigger may recurse. Add static recursion guard.
### **Autofix**


## Future Method with sObject Parameter

### **Id**
future-with-sObject
### **Severity**
error
### **Description**
Future methods cannot accept sObject parameters
### **Pattern**
  @future[^{]*\([^)]*\b(Account|Contact|Lead|Opportunity|\w+__c)\b
  
### **Message**
Future methods cannot accept sObjects. Pass IDs and re-query.
### **Autofix**


## Multiple Queueable Jobs Chained

### **Id**
queueable-chain-limit
### **Severity**
warning
### **Description**
Only 1 child job allowed when chaining from Queueable
### **Pattern**
  execute\s*\([^)]*QueueableContext[^)]*\)[\s\S]*enqueueJob[\s\S]*enqueueJob
  
### **Message**
Multiple enqueueJob calls in Queueable. Only 1 child job allowed when chaining.
### **Autofix**
