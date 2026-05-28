# Prompt Caching - Validations

## Caching High Temperature Responses

### **Id**
cache-high-temperature
### **Severity**
warning
### **Type**
regex
### **Pattern**
cache.*temperature.*0\.[6-9]|temperature.*0\.[6-9].*cache
### **Message**
Caching with high temperature. Responses are non-deterministic.
### **Fix Action**
Only cache responses with temperature <= 0.5
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Cache Without TTL

### **Id**
cache-no-ttl
### **Severity**
warning
### **Type**
regex
### **Pattern**
cache\.set|setCache|\.set\s*\(
### **Negative Pattern**
TTL|ttl|expire|EX|ex
### **Message**
Cache without TTL. May serve stale data indefinitely.
### **Fix Action**
Set appropriate TTL based on data freshness requirements
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Dynamic Content in Cached Prefix

### **Id**
cache-dynamic-prefix
### **Severity**
warning
### **Type**
regex
### **Pattern**
cache_control.*ephemeral.*\$\{|cache_control.*ephemeral.*Date|cache_control.*ephemeral.*time
### **Message**
Dynamic content in cached prefix. Will cause cache misses.
### **Fix Action**
Move dynamic content outside of cache_control blocks
### **Applies To**
  - *.ts
  - *.js

## No Cache Metrics

### **Id**
cache-no-metrics
### **Severity**
info
### **Type**
regex
### **Pattern**
cache\.get|getCached
### **Negative Pattern**
hit|miss|metric|log|count
### **Message**
Cache without hit/miss tracking. Can't measure effectiveness.
### **Fix Action**
Add cache hit/miss metrics and logging
### **Applies To**
  - *.ts
  - *.js
  - *.py