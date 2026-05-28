# Ai Observability - Validations

## LLM Calls Without Tracing

### **Id**
no-llm-tracing
### **Severity**
warning
### **Description**
LLM calls should be traced for debugging and cost tracking
### **Pattern**
  openai\.chat|anthropic\.messages(?!.*trace|langfuse|helicone)
  
### **Message**
LLM call without tracing. Add Langfuse or Helicone for observability.
### **Autofix**


## Missing Langfuse Flush

### **Id**
langfuse-no-flush
### **Severity**
error
### **Description**
Langfuse requires flush in serverless environments
### **Pattern**
  langfuse\.trace|langfuse\.generation(?!.*flush|shutdown)
  
### **Message**
Langfuse traces may be lost. Call flushAsync() before function returns.
### **Autofix**


## Trace Without User ID

### **Id**
no-trace-user-id
### **Severity**
info
### **Description**
Traces should include userId for user-level analytics
### **Pattern**
  trace\(\{(?!.*userId)
  
### **Message**
Add userId to traces for user-level cost and quality analytics.
### **Autofix**


## Missing Cost Calculation

### **Id**
no-cost-calculation
### **Severity**
warning
### **Description**
Token usage should be converted to cost
### **Pattern**
  usage\..*tokens(?!.*cost|price|calculate)
  
### **Message**
Track token costs, not just counts. Convert to dollars for budgeting.
### **Autofix**


## LLM Call Without Budget Check

### **Id**
no-budget-check
### **Severity**
warning
### **Description**
Check user budget before expensive LLM calls
### **Pattern**
  create\(\{.*model.*gpt-4|claude(?!.*budget|quota|limit)
  
### **Message**
Consider checking user budget before expensive LLM calls.
### **Autofix**


## Hardcoded Token Pricing

### **Id**
hardcoded-pricing
### **Severity**
info
### **Description**
Token prices change; use configurable pricing
### **Pattern**
  input.*0\.\d+.*output.*0\.\d+
  
### **Message**
Token prices are hardcoded. Use config for easier updates.
### **Autofix**


## Caching Small Prompt

### **Id**
cache-small-prompt
### **Severity**
warning
### **Description**
Prompts under 1024 tokens don't benefit from caching
### **Pattern**
  cache_control.*ephemeral(?!.*>.*1024|large|system)
  
### **Message**
Prompt caching requires 1024+ tokens. Small prompts waste cache writes.
### **Autofix**


## No Cache Hit Tracking

### **Id**
no-cache-stats
### **Severity**
info
### **Description**
Track cache hit rate to verify caching value
### **Pattern**
  cache_control(?!.*cache.*read|hit|stats)
  
### **Message**
Track cache hit rate to verify caching is cost-effective.
### **Autofix**


## Evaluation on Hot Path

### **Id**
eval-on-hot-path
### **Severity**
warning
### **Description**
RAG evaluation should be sampled, not on every request
### **Pattern**
  app\.(?:get|post).*evaluateRAGAS(?!.*sample|random)
  
### **Message**
Running evals on every request is expensive. Sample 5-10% instead.
### **Autofix**


## Same Model for Generation and Evaluation

### **Id**
same-model-eval
### **Severity**
info
### **Description**
LLMs have self-preference bias
### **Pattern**
  model.*(?:gpt-4o|claude).*evaluate.*model.*\\1
  
### **Message**
Using same model for generation and evaluation may inflate scores.
### **Autofix**


## No Error Handling in Traces

### **Id**
no-trace-error-handling
### **Severity**
warning
### **Description**
Capture errors in traces for debugging
### **Pattern**
  try.*trace(?!.*catch.*level.*ERROR|statusMessage)
  
### **Message**
Capture errors in traces with level: 'ERROR' for debugging.
### **Autofix**


## Streaming Without Usage Tracking

### **Id**
no-streaming-usage
### **Severity**
warning
### **Description**
Streaming responses need stream_options for usage
### **Pattern**
  stream:\s*true(?!.*stream_options.*include_usage|usage)
  
### **Message**
Add stream_options: { include_usage: true } to track streaming costs.
### **Autofix**


## Potential PII in Traces

### **Id**
pii-in-traces
### **Severity**
warning
### **Description**
User inputs may contain PII that shouldn't be logged
### **Pattern**
  trace.*input.*(?:req\.body|userMessage|prompt)(?!.*sanitize|redact)
  
### **Message**
Sanitize user input before tracing to remove PII.
### **Autofix**
