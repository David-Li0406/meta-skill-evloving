---
name: agent-workflow-orchestrator
description: Use this skill to design and implement multi-agent AI workflows that coordinate tasks, manage state, and integrate results for complex problem-solving.
---

# Skill body

The Agent Workflow Orchestrator skill guides you through creating and managing multi-agent AI systems that can plan, reason, use tools, and collaborate to accomplish complex tasks. This skill combines the capabilities of agent design, orchestration, and coordination to ensure robust and efficient workflows.

## Core Workflows

### Workflow 1: Design Agent Architecture
1. **Define** the agent's scope:
   - What tasks should it handle autonomously?
   - What requires human approval?
   - What is explicitly out of scope?
2. **Choose** architecture pattern:
   | Pattern | Description | Use When |
   |---------|-------------|----------|
   | Single Agent | One LLM with tools | Simple tasks, clear scope |
   | Router Agent | Classifies and delegates | Multiple distinct domains |
   | Sequential Chain | Agents in order | Pipeline processing |
   | Hierarchical | Manager + worker agents | Complex, decomposable tasks |
   | Collaborative | Peer agents discussing | Requires diverse expertise |
3. **Design** tool set:
   - What capabilities does the agent need?
   - How are tools defined and documented?
   - What are the safety boundaries?
4. **Plan** state management:
   - Conversation history
   - Task state and progress
   - External system state
5. **Document** architecture decisions

### Workflow 2: Decompose Task & Delegate
1. **Analyze** the complex task:
   - What's the end goal?
   - What are the components?
   - What expertise is needed?
2. **Map** to available agents/skills:
   - Which agents have relevant capabilities?
   - What's each agent's specialty?
   - What tools/MCPs do they access?
3. **Decompose** into subtasks:
   - Break along expertise boundaries
   - Identify dependencies
   - Determine execution order
4. **Delegate** to appropriate agents:
   - Assign subtasks with clear instructions
   - Provide necessary context
   - Set success criteria
   - Specify output format
5. **Monitor** execution:
   - Track progress
   - Identify blockers
   - Handle failures
6. **Integrate** results:
   - Collect agent outputs
   - Resolve conflicts
   - Synthesize into coherent whole
7. **Validate** final result

### Workflow 3: Implement Agent Loop
1. **Build** core agent loop:
   ```python
   class Agent:
       def __init__(self, llm, tools, system_prompt):
           self.llm = llm
           self.tools = {t.name: t for t in tools}
           self.system_prompt = system_prompt

       async def run(self, input_data):
           # Implementation of the agent's core logic
           pass
   ```

### Workflow 4: Parallel Agent Execution
1. **Identify** parallelizable subtasks:
   - Which tasks are independent?
   - Which share no dependencies?
   - Which can run concurrently?
2. **Prepare** parallel execution:
   - Assign subtasks to agents
   - Provide isolated contexts
   - Set timeout limits
3. **Launch** agents in parallel:
   - Initiate all at once
   - Monitor their progress and handle any issues

This skill ensures your multi-agent architecture is well-designed, efficient, and capable of handling real-world complexities while maintaining safety and controllability.