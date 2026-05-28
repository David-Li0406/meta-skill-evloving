# Conversation Memory - Validations

## No User Isolation in Memory

### **Id**
memory-no-user-isolation
### **Severity**
critical
### **Type**
regex
### **Pattern**
memory\.add|memory\.store|addMemory
### **Negative Pattern**
userId|user_id|ownerId|owner_id
### **Message**
Memory operations without user isolation. Privacy vulnerability.
### **Fix Action**
Add userId to all memory operations, filter by user on retrieval
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Importance Filtering

### **Id**
memory-no-importance-filter
### **Severity**
warning
### **Type**
regex
### **Pattern**
memory\.add|addMemory|store.*memory
### **Negative Pattern**
importance|score|filter|worthy
### **Message**
Storing memories without importance filtering. May cause memory explosion.
### **Fix Action**
Score importance before storing, filter low-importance content
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Memory Storage Without Retrieval

### **Id**
memory-no-retrieval
### **Severity**
warning
### **Type**
regex
### **Pattern**
memory\.add|store.*memory
### **Negative Pattern**
search|retrieve|query|get.*relevant
### **Message**
Storing memories but no retrieval logic. Memories won't be used.
### **Fix Action**
Implement memory retrieval and include in prompts
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Memory Cleanup

### **Id**
memory-no-cleanup
### **Severity**
info
### **Type**
regex
### **Pattern**
memory\.add|addMemory
### **Negative Pattern**
cleanup|consolidate|expire|limit|max
### **Message**
No memory cleanup mechanism. Storage will grow unbounded.
### **Fix Action**
Implement consolidation and cleanup based on age/importance
### **Applies To**
  - *.ts
  - *.js
  - *.py