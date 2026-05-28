# Ai Agents Architect - Sharp Edges

## Unlimited Loops

### **Id**
unlimited-loops
### **Summary**
Agent loops without iteration limits
### **Severity**
critical
### **Situation**
Agent runs until 'done' without max iterations
### **Why**
  Agents can get stuck in loops, repeating the same actions, or spiral
  into endless tool calls. Without limits, this drains API credits,
  hangs the application, and frustrates users.
  
### **Solution**
  Always set limits:
  - max_iterations on agent loops
  - max_tokens per turn
  - timeout on agent runs
  - cost caps for API usage
  - Circuit breakers for tool failures
  
### **Symptoms**
  - Agent runs forever
  - Unexplained high API costs
  - Application hangs
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
while.*True|loop.*agent|run\((?!.*max|.*limit)

## Poor Tool Descriptions

### **Id**
poor-tool-descriptions
### **Summary**
Vague or incomplete tool descriptions
### **Severity**
high
### **Situation**
Tool descriptions don't explain when/how to use
### **Why**
  Agents choose tools based on descriptions. Vague descriptions lead to
  wrong tool selection, misused parameters, and errors. The agent
  literally can't know what it doesn't see in the description.
  
### **Solution**
  Write complete tool specs:
  - Clear one-sentence purpose
  - When to use (and when not to)
  - Parameter descriptions with types
  - Example inputs and outputs
  - Error cases to expect
  
### **Symptoms**
  - Agent picks wrong tools
  - Parameter errors
  - Agent says it can't do things it can
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
description.*=.*"\w+"|tool_description.*<.*20

## No Error Handling

### **Id**
no-error-handling
### **Summary**
Tool errors not surfaced to agent
### **Severity**
high
### **Situation**
Catching tool exceptions silently
### **Why**
  When tool errors are swallowed, the agent continues with bad or missing
  data, compounding errors. The agent can't recover from what it can't
  see. Silent failures become loud failures later.
  
### **Solution**
  Explicit error handling:
  - Return error messages to agent
  - Include error type and recovery hints
  - Let agent retry or choose alternative
  - Log errors for debugging
  
### **Symptoms**
  - Agent continues with wrong data
  - Final answers are wrong
  - Hard to debug failures
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
except.*pass|except.*continue|catch.*\{\s*\}

## Memory Hoarding

### **Id**
memory-hoarding
### **Summary**
Storing everything in agent memory
### **Severity**
medium
### **Situation**
Appending all observations to memory without filtering
### **Why**
  Memory fills with irrelevant details, old information, and noise.
  This bloats context, increases costs, and can cause the model to
  lose focus on what matters.
  
### **Solution**
  Selective memory:
  - Summarize rather than store verbatim
  - Filter by relevance before storing
  - Use RAG for long-term memory
  - Clear working memory between tasks
  
### **Symptoms**
  - Context window exceeded
  - Agent references outdated info
  - High token costs
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
memory\.append|add_to_memory\(.*\)|history.*\+=|messages\.extend

## Tool Overload

### **Id**
tool-overload
### **Summary**
Agent has too many tools
### **Severity**
medium
### **Situation**
Giving agent 20+ tools for flexibility
### **Why**
  More tools means more confusion. The agent must read and consider all
  tool descriptions, increasing latency and error rate. Long tool lists
  get cut off or poorly understood.
  
### **Solution**
  Curate tools per task:
  - 5-10 tools maximum per agent
  - Use tool selection layer for large tool sets
  - Specialized agents with focused tools
  - Dynamic tool loading based on task
  
### **Symptoms**
  - Wrong tool selection
  - Agent overwhelmed by options
  - Slow responses
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
tools.*=.*\[.{500,}\]|len\(tools\).*>.*15

## Premature Multi Agent

### **Id**
premature-multi-agent
### **Summary**
Using multiple agents when one would work
### **Severity**
medium
### **Situation**
Starting with multi-agent architecture for simple tasks
### **Why**
  Multi-agent adds coordination overhead, communication failures,
  debugging complexity, and cost. Each agent handoff is a potential
  failure point. Start simple, add agents only when proven necessary.
  
### **Solution**
  Justify multi-agent:
  - Can one agent with good tools solve this?
  - Is the coordination overhead worth it?
  - Are the agents truly independent?
  - Start with single agent, measure limits
  
### **Symptoms**
  - Agents duplicating work
  - Communication overhead
  - Hard to debug failures
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
multi.*agent|agent.*team|create_agent.*create_agent|supervisor.*worker

## No Observability

### **Id**
no-observability
### **Summary**
Agent internals not logged or traceable
### **Severity**
medium
### **Situation**
Running agents without logging thoughts/actions
### **Why**
  When agents fail, you need to see what they were thinking, which
  tools they tried, and where they went wrong. Without observability,
  debugging is guesswork.
  
### **Solution**
  Implement tracing:
  - Log each thought/action/observation
  - Track tool calls with inputs/outputs
  - Trace token usage and latency
  - Use structured logging for analysis
  
### **Symptoms**
  - Can't explain agent failures
  - No visibility into agent reasoning
  - Debugging takes hours
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
agent\.run\((?!.*trace|.*callback|.*verbose)

## Brittle Output Parsing

### **Id**
brittle-output-parsing
### **Summary**
Fragile parsing of agent outputs
### **Severity**
medium
### **Situation**
Regex or exact string matching on LLM output
### **Why**
  LLMs don't produce perfectly consistent output. Minor format variations
  break brittle parsers. This causes agent crashes or incorrect behavior
  from parsing errors.
  
### **Solution**
  Robust output handling:
  - Use structured output (JSON mode, function calling)
  - Fuzzy matching for actions
  - Retry with format instructions on parse failure
  - Handle multiple output formats
  
### **Symptoms**
  - Parse errors in agent loop
  - Works sometimes, fails sometimes
  - Small prompt changes break parsing
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
output\.split|re\.match.*output|parse.*text|eval\(output