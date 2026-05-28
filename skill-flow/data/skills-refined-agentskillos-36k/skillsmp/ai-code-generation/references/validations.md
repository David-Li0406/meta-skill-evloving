# Ai Code Generation - Validations

## Missing Schema Validation on Output

### **Id**
no-schema-validation
### **Severity**
warning
### **Description**
Generated code/JSON should be validated against schema
### **Pattern**
  JSON\.parse\(.*response(?!.*Schema\.parse|validate|safeParse)
  
### **Message**
Parsing LLM response without schema validation. Use Zod.
### **Autofix**


## Missing Type Checking on Generated Code

### **Id**
no-type-checking
### **Severity**
warning
### **Description**
Generated code should be type-checked before use
### **Pattern**
  generate.*code.*write.*file(?!.*typecheck|tsc|validate)
  
### **Message**
Writing generated code without type checking.
### **Autofix**


## Missing Security Scan on Generated Code

### **Id**
no-security-scan
### **Severity**
warning
### **Description**
Generated code should be scanned for vulnerabilities
### **Pattern**
  generate.*code(?!.*security|semgrep|snyk|scan)
  
### **Message**
No security scanning on generated code.
### **Autofix**


## Eval on Generated Code

### **Id**
unsafe-eval
### **Severity**
error
### **Description**
Never eval generated code without sandboxing
### **Pattern**
  eval\(.*generate|generate.*eval
  
### **Message**
Never use eval() on AI-generated code. Use sandboxed execution.
### **Autofix**


## Tool Calls Without Validation

### **Id**
unvalidated-tool-calls
### **Severity**
error
### **Description**
Tool/function calls should be validated before execution
### **Pattern**
  toolHandlers\[.*\]\((?!.*validate|check|allowed)
  
### **Message**
Executing tool calls without validation. Check permissions.
### **Autofix**


## Missing Token Budget

### **Id**
no-token-budget
### **Severity**
warning
### **Description**
Code generation should have token/cost limits
### **Pattern**
  while.*generate|for.*agent(?!.*budget|max.*cost|token.*limit)
  
### **Message**
Agent loop without cost limits. Add token budget.
### **Autofix**


## Unbounded Agent Iterations

### **Id**
unbounded-iterations
### **Severity**
error
### **Description**
Agent loops must have maximum iteration limits
### **Pattern**
  while\s*\(\s*true\s*\)|while\s*\(\s*!done\s*\)(?!.*max|limit|i\s*<)
  
### **Message**
Unbounded agent loop. Add maximum iterations.
### **Autofix**


## No Error Handling for JSON Parsing

### **Id**
no-json-error-handling
### **Severity**
warning
### **Description**
JSON parsing should handle malformed responses
### **Pattern**
  JSON\.parse\((?!.*try.*catch)
  
### **Message**
JSON.parse without try/catch. LLMs may return invalid JSON.
### **Autofix**


## Missing Retry for Failed Generations

### **Id**
no-generation-retry
### **Severity**
info
### **Description**
Code generation should retry on failure
### **Pattern**
  await.*generate(?!.*retry|attempt|tries)
  
### **Message**
Consider adding retry logic for transient failures.
### **Autofix**
