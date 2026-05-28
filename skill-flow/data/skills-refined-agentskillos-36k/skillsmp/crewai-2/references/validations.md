# Crewai - Validations

## Agent Without Backstory

### **Id**
agent-missing-backstory
### **Severity**
medium
### **Type**
regex
### **Pattern**
Agent\([^)]*role[^)]*goal[^)]*\)
### **Negative Pattern**
backstory
### **Message**
Agent without backstory may lack context for decisions.
### **Fix Action**
Add backstory explaining agent's expertise and approach
### **Applies To**
  - *.py

## Task Without Expected Output

### **Id**
task-missing-expected-output
### **Severity**
high
### **Type**
regex
### **Pattern**
Task\([^)]*description[^)]*\)
### **Negative Pattern**
expected_output
### **Message**
Task without expected_output leads to inconsistent results.
### **Fix Action**
Add expected_output describing the deliverable format
### **Applies To**
  - *.py

## Sequential Tasks Without Context

### **Id**
task-missing-context
### **Severity**
medium
### **Type**
regex
### **Pattern**
Task\([^)]*\)\s*\n\s*Task\(
### **Negative Pattern**
context\s*=
### **Message**
Sequential tasks may need context to pass outputs.
### **Fix Action**
Add context=[previous_task] to chain task outputs
### **Applies To**
  - *.py

## Crew Without Explicit Process

### **Id**
crew-no-process
### **Severity**
low
### **Type**
regex
### **Pattern**
Crew\([^)]*\)
### **Negative Pattern**
process\s*=
### **Message**
Crew without explicit process uses default. Be intentional.
### **Fix Action**
Add process=Process.sequential or Process.hierarchical
### **Applies To**
  - *.py

## Hierarchical Without Manager LLM

### **Id**
hierarchical-no-manager
### **Severity**
high
### **Type**
regex
### **Pattern**
Process\.hierarchical
### **Negative Pattern**
manager_llm
### **Message**
Hierarchical process requires manager_llm.
### **Fix Action**
Add manager_llm=ChatOpenAI(...) to Crew
### **Applies To**
  - *.py

## Vague Agent Role

### **Id**
vague-agent-role
### **Severity**
low
### **Type**
regex
### **Pattern**
role\s*=\s*["'](?:Agent|Assistant|Helper|Worker)["']
### **Message**
Agent role is too generic. Be specific about expertise.
### **Fix Action**
Use specific role like 'Senior Python Developer' or 'Market Research Analyst'
### **Applies To**
  - *.py
  - *.yaml

## Agent Without Iteration Limit

### **Id**
no-max-iterations
### **Severity**
medium
### **Type**
regex
### **Pattern**
Agent\([^)]*\)
### **Negative Pattern**
max_iter|max_iterations
### **Message**
Agent without max_iter may loop excessively.
### **Fix Action**
Add max_iter=15 or appropriate limit
### **Applies To**
  - *.py

## YAML Config Key Style

### **Id**
yaml-key-mismatch
### **Severity**
low
### **Type**
regex
### **Pattern**
^\s+[A-Z][a-zA-Z]+:
### **Message**
YAML keys should be snake_case, not PascalCase.
### **Fix Action**
Use researcher: not Researcher:
### **Applies To**
  - config/agents.yaml
  - config/tasks.yaml