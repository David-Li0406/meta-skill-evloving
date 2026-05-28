---
name: agent-workflow-orchestrator
description: Use this skill to coordinate and build complex multi-agent AI workflows that leverage orchestration, tool use, and state management.
---

# Agent Workflow Orchestrator

The Agent Workflow Orchestrator skill enables the design, coordination, and implementation of multi-agent AI systems that can plan, reason, use tools, and collaborate to accomplish complex tasks. This skill acts as a conductor, delegating subtasks to appropriate agents, managing dependencies, integrating results, and ensuring coherent final outputs.

This skill covers agent design patterns, tool integration, state management, error handling, and human-in-the-loop workflows. It helps you build robust agent systems that can handle real-world complexity while maintaining safety and controllability.

Whether you are building autonomous assistants, workflow automation, or complex reasoning systems, this skill ensures your agent architecture is well-designed and production-ready.

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

### Workflow 2: Implement Agent Loop
1. **Build** core agent loop:
   ```python
   class Agent:
       def __init__(self, llm, tools, system_prompt):
           self.llm = llm
           self.tools = {t.name: t for t in tools}
           self.system_prompt = system_prompt

       async def run(self, user_input, max_steps=10):
           messages = [
               {"role": "system", "content": self.system_prompt},
               {"role": "user", "content": user_input}
           ]

           for step in range(max_steps):
               response = await self.llm.chat(messages, tools=self.tools)

               if response.tool_calls:
                   for call in response.tool_calls:
                       result = await self.execute_tool(call)
                       messages.append({"role": "tool", "content": result})
               else:
                   return response.content

           raise MaxStepsExceeded()

       async def execute_tool(self, call):
           tool = self.tools[call.name]
           return await tool.execute(call.arguments)
   ```
2. **Implement** tools with clear interfaces
3. **Add** error handling and retries
4. **Include** logging and observability
5. **Test** with diverse scenarios

### Workflow 3: Decompose Task & Delegate
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
   - Maintain separate contexts
   - Monitor all executions
4. **Coordinate** completion:
   - Wait for all to finish
   - Handle stragglers
   - Manage timeout failures
5. **Aggregate** results:
   - Collect all outputs
   - Merge related findings
   - Resolve inconsistencies
6. **Synthesize** final output

### Workflow 5: Sequential Agent Pipeline
1. **Design** pipeline flow:
   - Order agents by dependencies
   - Define handoff points
   - Specify data transformations
2. **Execute** pipeline sequentially:
   - Agent 1: Process initial input → Output A
   - Validate Output A
   - Agent 2: Process Output A → Output B
   - Validate Output B
   - Agent N: Process Output (N-1) → Final Output
3. **Manage** state between agents:
   - Pass relevant data forward
   - Maintain context where needed
   - Discard temporary artifacts
4. **Handle** pipeline failures:
   - Identify failed stage
   - Retry or use fallback
   - Don't propagate bad data
5. **Validate** end-to-end result

### Workflow 6: Error Recovery & Fallback
1. **Detect** agent failure:
   - Task not completed
   - Output quality insufficient
   - Timeout exceeded
   - Error thrown
2. **Diagnose** failure cause:
   - Was task unclear?
   - Was agent wrong choice?
   - Was input malformed?
   - Was dependency unavailable?
3. **Attempt** recovery:
   - **Retry** with same agent (if transient error)
   - **Retry** with different agent (if capability mismatch)
   - **Simplify** task and retry (if too complex)
   - **Escalate** to human (if unrecoverable)
4. **Log** failure and recovery
5. **Continue** workflow if recovered

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Design agent | "Design an agent for [task]" |
| Add tools | "What tools for [agent type]" |
| Build multi-agent | "Build multi-agent system for [goal]" |
| Handle errors | "Agent error handling patterns" |
| Add human-in-loop | "Add human approval to agent workflow" |
| Debug agent | "Debug agent workflow" |
| Delegate complex task | "Orchestrate agents for [task]" |
| Run agents in parallel | "Run these tasks in parallel: [tasks]" |
| Create agent pipeline | "Create pipeline: [agent1] → [agent2] → [agent3]" |
| Select best agent | "Which agent should handle [task]?" |
| Coordinate workflow | "Coordinate [workflow] across agents" |
| Handle agent failure | "Agent [X] failed on [task], recover" |
| Integrate agent outputs | "Synthesize outputs from [agents]" |

## Best Practices

- **Start Simple**: Begin with a single agent with tools before scaling to multi-agent systems.
- **Match Expertise to Task**: Use specialized agents for specialized work.
- **Provide Clear Context**: Each agent needs to understand its role and the larger goal.
- **Manage Dependencies**: Make execution order explicit to avoid confusion.
- **Validate Handoffs**: Ensure data integrity between agents.
- **Handle Failures Gracefully**: Implement fallback strategies and retry logic.
- **Optimize Communication**: Minimize unnecessary data passing between agents.
- **Monitor Progress**: Keep track of agent activity and workflow status.
- **Synthesize Thoughtfully**: Integrate diverse outputs into a coherent final product.

## Common Pitfalls to Avoid

- Building multi-agent systems when a single agent suffices.
- Giving agents too much autonomy without safety bounds.
- Not handling tool failures and edge cases.
- Forgetting that LLMs can hallucinate tool calls.
- Infinite loops when agents get stuck.
- Not logging enough to debug agent behavior.

## Example Orchestrations

### Feature Development Workflow
```markdown
**Orchestrator**: Coordinate feature development

1. **Requirements Analysis** (Operations Manager)
   - Clarify requirements
   - Define scope
   - Identify constraints

2. **Parallel Design Phase**
   - **UI Builder**: Design components
   - **Database Designer**: Design schema
   - **API Designer**: Design endpoints

3. **Integration Review** (Orchestrator)
   - Ensure designs are compatible
   - Resolve conflicts
   - Approve for implementation

4. **Implementation** (General-Purpose)
   - Build based on approved designs

5. **Quality Assurance** (Testing QA)
   - Generate E2E tests
   - Run test suite
   - Report issues

6. **Fix Issues** (General-Purpose)
   - Address failing tests

7. **Deployment** (Deployment Automation)
   - Deploy to staging
   - Verify deployment
   - Deploy to production
```

### Content Creation Pipeline
```markdown
**Orchestrator**: Create technical blog post

1. **Research** (General-Purpose + Firecrawl)
   - Gather sources
   - Extract key information

2. **Parallel Analysis**
   - **Prompt Engineer**: Analyze for clarity
   - **Workflow Designer**: Identify structure
   - **Output Formatter**: Determine format

3. **Draft** (General-Purpose)
   - Write based on research and analysis

4. **Review & Edit** (Prompt Engineer)
   - Review for quality
   - Suggest improvements

5. **Revise** (General-Purpose)
   - Apply feedback

6. **Format** (Output Formatter)
   - Format for target platform

7. **Generate Metadata** (General-Purpose)
   - SEO metadata
   - Social snippets
```