# Autonomous Agents - Validations

## Agent Loop Without Step Limit

### **Id**
no-step-limit
### **Severity**
error
### **Description**
Autonomous agents must have maximum step limits
### **Pattern**
  (while\s+True|for\s+.*\s+in\s+range\s*\(\s*\d{4,})|agent\.(run|invoke|execute)(?!.*max)
  
### **Anti Pattern**
  (max_steps|max_iterations|step_limit|iteration_limit)
  
### **Message**
Agent loop without step limit. Add max_steps to prevent infinite loops.
### **Autofix**


## No Cost Tracking or Limits

### **Id**
no-cost-limit
### **Severity**
error
### **Description**
Agents should track and limit API costs
### **Pattern**
  (openai|anthropic|ChatOpenAI|ChatAnthropic)
  
### **Anti Pattern**
  (cost|budget|max_tokens|token_limit|spending)
  
### **Message**
Agent uses LLM without cost tracking. Add cost limits to prevent runaway spending.
### **Autofix**


## Agent Without Timeout

### **Id**
no-timeout
### **Severity**
warning
### **Description**
Long-running agents need timeouts
### **Pattern**
  agent\.(run|invoke|execute|stream)
  
### **Anti Pattern**
  (timeout|deadline|max_time|time_limit)
  
### **Message**
Agent invocation without timeout. Add timeout to prevent hung tasks.
### **Autofix**


## MemorySaver Used in Production

### **Id**
memory-saver-in-production
### **Severity**
error
### **Description**
MemorySaver is for development only
### **Pattern**
  MemorySaver\(\)
  
### **Anti Pattern**
  (development|dev|test|local)
  
### **Message**
MemorySaver is not persistent. Use PostgresSaver or SqliteSaver for production.
### **Autofix**


## Long-Running Agent Without Checkpointing

### **Id**
no-checkpointing
### **Severity**
warning
### **Description**
Agents that run multiple steps need checkpointing
### **Pattern**
  (StateGraph|create_react_agent|AgentExecutor)
  
### **Anti Pattern**
  (checkpointer|checkpoint|PostgresSaver|SqliteSaver)
  
### **Message**
Multi-step agent without checkpointing. Add checkpointer for durability.
### **Autofix**


## Agent Without Thread ID

### **Id**
missing-thread-id
### **Severity**
warning
### **Description**
Checkpointed agents need unique thread IDs
### **Pattern**
  agent\.(invoke|run)\s*\(
  
### **Anti Pattern**
  thread_id|session_id|conversation_id
  
### **Message**
Agent invocation without thread_id. State won't persist correctly.
### **Autofix**


## Using Agent Output Without Validation

### **Id**
trusting-agent-output
### **Severity**
warning
### **Description**
Agent outputs should be validated before use
### **Pattern**
  result\s*=\s*agent\.(invoke|run).*\n.*(?!validate|check|verify)
  
### **Message**
Agent output used without validation. Validate before acting on results.
### **Autofix**


## Agent Without Structured Output

### **Id**
no-structured-output
### **Severity**
info
### **Description**
Structured outputs are more reliable
### **Pattern**
  (create_react_agent|AgentExecutor|StateGraph)
  
### **Anti Pattern**
  (BaseModel|TypedDict|dataclass|schema|structured)
  
### **Message**
Consider using structured outputs (Pydantic) for more reliable parsing.
### **Autofix**


## Agent Without Error Recovery

### **Id**
no-error-recovery
### **Severity**
warning
### **Description**
Agents should handle and recover from errors
### **Pattern**
  agent\.(invoke|run|execute)
  
### **Anti Pattern**
  (try|catch|except|on_error|error_handler|fallback)
  
### **Message**
Agent call without error handling. Add try/catch or error handler.
### **Autofix**


## Destructive Actions Without Rollback

### **Id**
no-rollback-capability
### **Severity**
warning
### **Description**
Actions that modify state should be reversible
### **Pattern**
  (delete|remove|update|write|send|transfer)
  
### **Anti Pattern**
  (rollback|undo|revert|checkpoint|backup)
  
### **Message**
Destructive action without rollback capability. Save state before modification.
### **Autofix**


## Critical Actions Without Human Review

### **Id**
no-human-review
### **Severity**
warning
### **Description**
Important actions should have human approval
### **Pattern**
  (send_email|transfer|delete|publish|deploy)
  
### **Anti Pattern**
  (approve|confirm|review|human|manual|interrupt)
  
### **Message**
Critical action without human review. Add approval step for safety.
### **Autofix**


## Agent Without Logging

### **Id**
no-logging
### **Severity**
warning
### **Description**
Agent actions should be logged for debugging
### **Pattern**
  (create_react_agent|AgentExecutor|StateGraph)
  
### **Anti Pattern**
  (logger|logging|log\.|structlog|trace|LangSmith)
  
### **Message**
Agent without logging. Add structured logging for observability.
### **Autofix**
