# Context Window Management - Validations

## No Token Counting

### **Id**
no-token-counting
### **Severity**
warning
### **Type**
regex
### **Pattern**
messages\.push|context\s*\+|prompt\s*\+
### **Negative Pattern**
token|Token|tiktoken|count|length
### **Message**
Building context without token counting. May exceed model limits.
### **Fix Action**
Count tokens before sending, implement budget allocation
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Naive Message Truncation

### **Id**
naive-truncation
### **Severity**
warning
### **Type**
regex
### **Pattern**
slice\s*\(\s*-?\d+\s*\)|messages\.shift|messages\.splice
### **Negative Pattern**
summarize|importance|priority
### **Message**
Truncating messages without summarization. Critical context may be lost.
### **Fix Action**
Summarize old messages instead of simply removing them
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Hardcoded Token Limit

### **Id**
hardcoded-token-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
max.*=\s*\d{4,}|limit.*=\s*\d{4,}
### **Message**
Hardcoded token limit. Consider making configurable per model.
### **Fix Action**
Use model-specific limits from configuration
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Context Management Strategy

### **Id**
no-context-strategy
### **Severity**
warning
### **Type**
regex
### **Pattern**
ChatCompletion|messages\.create|complete\(
### **Negative Pattern**
context|strategy|summarize|trim|budget
### **Message**
LLM calls without context management strategy.
### **Fix Action**
Implement context management: budgets, summarization, or RAG
### **Applies To**
  - *.ts
  - *.js
  - *.py