# Ai Agents Architect - Validations

## No Iteration Limit

### **Id**
no-iteration-limit
### **Severity**
error
### **Type**
regex
### **Pattern**
  - while\s+True
  - while\s+1
  - agent\.run\([^)]*\)(?!.*max)
  - loop(?!.*limit|.*max)
### **Message**
Agent loop without iteration limit can run forever.
### **Fix Action**
Add max_iterations or loop limit
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Silent Tool Error Handling

### **Id**
silent-tool-error
### **Severity**
error
### **Type**
regex
### **Pattern**
  - except.*pass
  - except.*continue
  - catch\s*\([^)]*\)\s*\{\s*\}
  - catch.*return\s+None
### **Message**
Tool errors caught silently - agent won't know about failures.
### **Fix Action**
Return error message to agent for recovery
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Short Tool Description

### **Id**
short-tool-description
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - description\s*[=:]\s*["'][^"']{1,30}["']
  - tool_description\s*[=:]\s*["'][^"']{1,30}["']
### **Message**
Tool description may be too short for agent to understand.
### **Fix Action**
Add detailed description with when to use and examples
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Memory Append All

### **Id**
memory-append-all
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - memory\.append
  - add_to_memory\([^)]+\)
  - history\s*\+=|history\.extend
  - messages\.append(?!.*filter)
### **Message**
Appending to memory without filtering may cause context overflow.
### **Fix Action**
Filter or summarize before adding to memory
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Agent Timeout

### **Id**
no-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - agent\.run\([^)]*\)(?!.*timeout)
  - execute\([^)]*\)(?!.*timeout)
  - invoke\([^)]*\)(?!.*timeout)
### **Message**
Agent execution without timeout can hang indefinitely.
### **Fix Action**
Add timeout parameter to agent execution
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Agent Tracing

### **Id**
no-tracing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - agent\.run\([^)]*\)(?!.*trace|.*callback|.*verbose)
  - AgentExecutor\([^)]*\)(?!.*callbacks)
### **Message**
Agent running without tracing - hard to debug failures.
### **Fix Action**
Add tracing callbacks or verbose mode
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Brittle Output Parsing

### **Id**
brittle-parsing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - output\.split
  - re\.match\([^)]*output
  - parse\([^)]*text
  - eval\(output
### **Message**
Fragile parsing of agent output may break on format changes.
### **Fix Action**
Use structured output (JSON mode) or robust parsing
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Too Many Tools

### **Id**
too-many-tools
### **Severity**
info
### **Type**
regex
### **Pattern**
  - tools\s*=\s*\[[^\]]{500,}\]
  - len\(tools\)\s*>\s*15
  - tools\s*=\s*\[(?:[^,\]]+,){15,}
### **Message**
Agent has many tools - may cause confusion and slow responses.
### **Fix Action**
Curate 5-10 tools per agent or use tool selection layer
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Cost Limit

### **Id**
no-cost-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - agent\.run(?!.*cost|.*budget)
  - max_tokens\s*=\s*None
### **Message**
Agent without cost limits can consume excessive API credits.
### **Fix Action**
Add token or cost limits to agent execution
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js