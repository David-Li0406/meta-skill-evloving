# Multi Agent Orchestration - Validations

## Parallel Agents with Shared State

### **Id**
parallel-shared-state
### **Severity**
high
### **Type**
regex
### **Pattern**
Promise\.all\s*\([^)]+\)[^;]*state\.
### **Negative Pattern**
mutex|lock|atomic|synchronized
### **Message**
Parallel agent execution with shared state access. Risk of race conditions.
### **Fix Action**
Use scoped state channels or mutex for safe concurrent access
### **Applies To**
  - *.ts
  - *.js

## Unbounded Agent Recursion

### **Id**
unbounded-recursion
### **Severity**
critical
### **Type**
regex
### **Pattern**
async\s+\w+Agent[^{]*\{[^}]*this\.\w+Agent|callAgent\s*\([^)]*\)
### **Negative Pattern**
maxDepth|maxCalls|circuitBreaker|limit|depth
### **Message**
Agent can call other agents without recursion limit. Risk of infinite loops.
### **Fix Action**
Add maxDepth/maxCalls limit and circuit breaker pattern
### **Applies To**
  - *.ts
  - *.js

## Missing Handoff Context

### **Id**
no-handoff-context
### **Severity**
medium
### **Type**
regex
### **Pattern**
delegate|handoff|transfer|route.*to
### **Negative Pattern**
context|state|handoffData|previousAgent
### **Message**
Agent handoff without explicit context transfer.
### **Fix Action**
Pass complete handoff context including previous work and expectations
### **Applies To**
  - *.ts
  - *.js

## Multi-Agent Without Token Tracking

### **Id**
no-token-tracking
### **Severity**
medium
### **Type**
regex
### **Pattern**
Promise\.all\s*\([^)]*\w+Agent|sequential.*agent|parallel.*agent
### **Negative Pattern**
token|usage|cost|budget
### **Message**
Multi-agent workflow without token tracking. Risk of cost explosion.
### **Fix Action**
Track token usage per agent and enforce budgets
### **Applies To**
  - *.ts
  - *.js

## Missing Agent Orchestration Tracing

### **Id**
no-orchestration-tracing
### **Severity**
medium
### **Type**
regex
### **Pattern**
class\s+\w*(?:Orchestrator|Manager|Coordinator|Supervisor)
### **Negative Pattern**
trace|log|span|observe|monitor
### **Message**
Agent orchestrator without tracing. Debugging will be difficult.
### **Fix Action**
Add tracing for agent invocations, state changes, and handoffs
### **Applies To**
  - *.ts
  - *.js

## Multi-Agent Without Timeout

### **Id**
no-timeout-multi-agent
### **Severity**
high
### **Type**
regex
### **Pattern**
await\s+this\.\w+Agent|await\s+agent\.|await\s+Promise\.all
### **Negative Pattern**
timeout|AbortController|deadline|timeLimit
### **Message**
Multi-agent execution without timeout. Could hang indefinitely.
### **Fix Action**
Add execution timeout with Promise.race or AbortController
### **Applies To**
  - *.ts
  - *.js

## Hardcoded Agent Selection

### **Id**
hardcoded-agent-selection
### **Severity**
low
### **Type**
regex
### **Pattern**
if\s*\([^)]*===?\s*["'][^"']+["']\s*\)\s*\{[^}]*Agent
### **Message**
Agent selection using hardcoded string matching. Consider using registry.
### **Fix Action**
Use agent registry with capability matching for flexible routing
### **Applies To**
  - *.ts
  - *.js

## Swallowed Errors in Agent Chain

### **Id**
no-error-propagation
### **Severity**
high
### **Type**
regex
### **Pattern**
catch\s*\([^)]*\)\s*\{[^}]*(?:console\.log|return\s+null|continue)
### **Message**
Agent errors swallowed without propagation. May cause silent failures.
### **Fix Action**
Propagate errors with context or implement explicit fallback handling
### **Applies To**
  - *.ts
  - *.js

## Agent Without Unique Identifier

### **Id**
missing-agent-id
### **Severity**
low
### **Type**
regex
### **Pattern**
class\s+\w+Agent\s*(?:extends|implements|{)
### **Negative Pattern**
id:|agentId|this\.id\s*=
### **Message**
Agent class without unique identifier. Tracing will be difficult.
### **Fix Action**
Add unique agent ID for tracing and debugging
### **Applies To**
  - *.ts
  - *.js

## Global State Modification in Agent

### **Id**
global-state-modification
### **Severity**
high
### **Type**
regex
### **Pattern**
global\.|window\.|process\.env\s*=
### **Message**
Agent modifying global state. Causes unpredictable behavior in multi-agent systems.
### **Fix Action**
Use passed-in state object instead of global state
### **Applies To**
  - *.ts
  - *.js