# Computer Use Agents - Validations

## Computer Use Without Sandbox

### **Id**
no-sandboxing
### **Severity**
error
### **Description**
Computer use agents MUST run in sandboxed environments
### **Pattern**
  (pyautogui|xdotool|computer_use|ComputerUse)
  
### **Anti Pattern**
  (docker|container|sandbox|isolated|virtualized)
  
### **Message**
Computer use without sandboxing detected. Use Docker containers with restrictions.
### **Autofix**


## Sandbox With Full Network Access

### **Id**
unrestricted-network
### **Severity**
error
### **Description**
Sandboxed agents should have restricted network access
### **Pattern**
  docker run.*--network\s+host
  
### **Message**
Sandbox has full network access. Use --network=none or specific allowlist.
### **Autofix**


## Running as Root in Container

### **Id**
root-in-container
### **Severity**
error
### **Description**
Container agents should run as non-root user
### **Pattern**
  docker run(?!.*--user).*computer
  
### **Anti Pattern**
  (--user|USER\s+\w+)
  
### **Message**
Container running as root. Add --user flag or USER directive in Dockerfile.
### **Autofix**


## Container Without Capability Drops

### **Id**
no-capability-drops
### **Severity**
warning
### **Description**
Containers should drop unnecessary capabilities
### **Pattern**
  docker run(?!.*--cap-drop).*computer
  
### **Message**
Container has full capabilities. Add --cap-drop ALL.
### **Autofix**


## Container Without Seccomp Profile

### **Id**
no-seccomp
### **Severity**
warning
### **Description**
Containers should use seccomp profiles for syscall filtering
### **Pattern**
  docker run(?!.*--security-opt).*computer
  
### **Message**
No security options set. Consider --security-opt seccomp:profile.json
### **Autofix**


## No Maximum Step Limit

### **Id**
no-step-limit
### **Severity**
warning
### **Description**
Computer use loops should have maximum step limits
### **Pattern**
  while\s+(True|not\s+done)
  
### **Anti Pattern**
  (max_steps|step_limit|step\s*<|step\s*<=)
  
### **Message**
Infinite loop risk. Add max_steps limit (recommended: 50).
### **Autofix**


## No Execution Timeout

### **Id**
no-timeout
### **Severity**
warning
### **Description**
Computer use should have timeout limits
### **Pattern**
  (agent\.run|execute_task|run_task)
  
### **Anti Pattern**
  (timeout|max_runtime|time_limit)
  
### **Message**
No timeout on execution. Add timeout (recommended: 5-10 minutes).
### **Autofix**


## Container Without Memory Limit

### **Id**
no-memory-limit
### **Severity**
warning
### **Description**
Containers should have memory limits to prevent DoS
### **Pattern**
  docker run(?!.*--memory).*computer
  
### **Message**
No memory limit on container. Add --memory 2g or similar.
### **Autofix**


## No Cost Tracking

### **Id**
no-cost-tracking
### **Severity**
warning
### **Description**
Computer use should track API costs
### **Pattern**
  (computer_use|ComputerUse|screenshot)
  
### **Anti Pattern**
  (cost|token|usage|billing|budget)
  
### **Message**
No cost tracking. Monitor token usage to prevent bill surprises.
### **Autofix**


## No Maximum Cost Limit

### **Id**
no-cost-limit
### **Severity**
info
### **Description**
Consider adding cost limits per task
### **Pattern**
  (run_task|execute_task|agent\.run)
  
### **Anti Pattern**
  (max_cost|cost_limit|budget)
  
### **Message**
Consider adding max_cost_per_task to prevent expensive runaway tasks.
### **Autofix**


## No User Confirmation for Sensitive Actions

### **Id**
no-confirmation-gate
### **Severity**
warning
### **Description**
Sensitive actions should require user confirmation
### **Pattern**
  (purchase|payment|login|delete|submit|download)
  
### **Anti Pattern**
  (confirm|approval|user_approve|require_confirmation)
  
### **Message**
Sensitive actions without confirmation. Add confirmation gates.
### **Autofix**


## No Action Logging

### **Id**
no-action-logging
### **Severity**
warning
### **Description**
All agent actions should be logged
### **Pattern**
  (execute_action|perform_action|click|type|key_press)
  
### **Anti Pattern**
  (log|audit|record|track)
  
### **Message**
Actions not logged. Add logging for debugging and auditing.
### **Autofix**


## Dangerous Bash Commands Not Blocked

### **Id**
dangerous-bash-commands
### **Severity**
error
### **Description**
Dangerous shell commands should be blocked
### **Pattern**
  subprocess\.run\(.*shell=True
  
### **Anti Pattern**
  (sanitize|validate|blocklist|dangerous_patterns)
  
### **Message**
Shell execution without command validation. Block dangerous commands.
### **Autofix**


## Full Resolution Screenshots

### **Id**
full-resolution-screenshots
### **Severity**
info
### **Description**
Consider reducing screenshot resolution for token efficiency
### **Pattern**
  screenshot\(\)
  
### **Anti Pattern**
  (resize|scale|thumbnail|resolution|1280|1024)
  
### **Message**
Consider resizing screenshots (1280x800) to reduce token usage.
### **Autofix**


## No Screenshot Pruning in Context

### **Id**
no-screenshot-pruning
### **Severity**
warning
### **Description**
Old screenshots should be pruned to manage context window
### **Pattern**
  messages\.append.*image
  
### **Anti Pattern**
  (prune|trim|limit|max_screenshots|remove_old)
  
### **Message**
Screenshots accumulating in context. Implement pruning strategy.
### **Autofix**


## No Recovery From Failed Actions

### **Id**
no-action-recovery
### **Severity**
warning
### **Description**
Agents should recover from failed UI interactions
### **Pattern**
  (click|type|scroll)
  
### **Anti Pattern**
  (retry|recover|fallback|try.*except|error.*handling)
  
### **Message**
No error recovery for UI actions. Add retry logic and fallbacks.
### **Autofix**


## No Task Failure Handling

### **Id**
no-task-failure-handling
### **Severity**
warning
### **Description**
Tasks should handle overall failure gracefully
### **Pattern**
  (run_task|execute_task)
  
### **Anti Pattern**
  (finally|cleanup|on_failure|error_handler)
  
### **Message**
No failure handling. Add cleanup and error reporting.
### **Autofix**
