# AI Agents Architect

## Patterns


---
  #### **Name**
ReAct Loop
  #### **Description**
Reason-Act-Observe cycle for step-by-step execution
  #### **When**
Simple tool use with clear action-observation flow
  #### **Implementation**
    - Thought: reason about what to do next
    - Action: select and invoke a tool
    - Observation: process tool result
    - Repeat until task complete or stuck
    - Include max iteration limits
    

---
  #### **Name**
Plan-and-Execute
  #### **Description**
Plan first, then execute steps
  #### **When**
Complex tasks requiring multi-step planning
  #### **Implementation**
    - Planning phase: decompose task into steps
    - Execution phase: execute each step
    - Replanning: adjust plan based on results
    - Separate planner and executor models possible
    

---
  #### **Name**
Tool Registry
  #### **Description**
Dynamic tool discovery and management
  #### **When**
Many tools or tools that change at runtime
  #### **Implementation**
    - Register tools with schema and examples
    - Tool selector picks relevant tools for task
    - Lazy loading for expensive tools
    - Usage tracking for optimization
    

---
  #### **Name**
Hierarchical Memory
  #### **Description**
Multi-level memory for different purposes
  #### **When**
Long-running agents needing context
  #### **Implementation**
    - Working memory: current task context
    - Episodic memory: past interactions/results
    - Semantic memory: learned facts and patterns
    - Use RAG for retrieval from long-term memory
    

---
  #### **Name**
Supervisor Pattern
  #### **Description**
Supervisor agent orchestrates specialist agents
  #### **When**
Complex tasks requiring multiple skills
  #### **Implementation**
    - Supervisor decomposes and delegates
    - Specialists have focused capabilities
    - Results aggregated by supervisor
    - Error handling at supervisor level
    

---
  #### **Name**
Checkpoint Recovery
  #### **Description**
Save state for resumption after failures
  #### **When**
Long-running tasks that may fail
  #### **Implementation**
    - Checkpoint after each successful step
    - Store task state, memory, and progress
    - Resume from last checkpoint on failure
    - Clean up checkpoints on completion
    

## Anti-Patterns


---
  #### **Name**
Unlimited Autonomy
  #### **Description**
Letting agents run without guardrails
  #### **Problem**
Runaway costs, dangerous actions, infinite loops
  #### **Solution**
Iteration limits, cost caps, action allowlists, human-in-loop

---
  #### **Name**
Tool Overload
  #### **Description**
Giving agent too many tools
  #### **Problem**
Confusion, wrong tool selection, bloated prompts
  #### **Solution**
Curate relevant tools per task, use tool selection layer

---
  #### **Name**
Memory Hoarding
  #### **Description**
Storing everything in agent memory
  #### **Problem**
Context overflow, noise, increased costs
  #### **Solution**
Selective memory, summarization, relevance filtering

---
  #### **Name**
Brittle Tool Definitions
  #### **Description**
Vague or incomplete tool descriptions
  #### **Problem**
Agent misuses tools, wrong parameters, failures
  #### **Solution**
Clear descriptions, parameter docs, usage examples

---
  #### **Name**
Silent Failures
  #### **Description**
Catching errors without surfacing them
  #### **Problem**
Agent continues with bad state, compounds errors
  #### **Solution**
Explicit error handling, failure escalation, retry limits

---
  #### **Name**
Premature Multi-Agent
  #### **Description**
Using multiple agents when one suffices
  #### **Problem**
Coordination overhead, communication failures, complexity
  #### **Solution**
Start with single agent, add agents only when needed