---
name: Agent Architecture Patterns
description: Core architectural patterns for local AI agents (Reflection, Planning, Tool Use, Multi-Agent, Memory).
---

This library defines the core architectural patterns for local AI agents. These patterns are designed to be **language-agnostic**, focusing on logic, system prompts, and operational flow rather than specific code.

---

## 1. The Reflection Pattern
**Objective:** Improve accuracy and reduce hallucinations through iterative self-critique.

### 🔄 Operational Flow
1. **Drafting:** The agent generates an initial response.
2. **Critique:** The agent (or a separate instance) evaluates the draft against requirements.
3. **Refinement:** The agent regenerates the response based on the critique.

### 📝 System Prompt Template
> "Follow the **Reflective Protocol**:
> 1. Generate a complete response to the user's request.
> 2. Critically analyze your own response. Look for logic gaps, missing edge cases, or potential errors.
> 3. Provide a 'Revised Response' that addresses those specific issues.
> 4. State clearly what you changed and why."

---

## 2. The Planning Pattern
**Objective:** Decompose complex, multi-step problems into a structured roadmap before execution.

### 🔄 Operational Flow
1. **Decomposition:** Break the goal into a sequence of atomic sub-tasks.
2. **Dependency Mapping:** Determine if any step relies on the output of a previous one.
3. **Step-wise Execution:** Process each task one by one, verifying completion at each stage.

### 📝 System Prompt Template
> "Before attempting the user's request, you must output a **Task Manifest**:
> - **Objective:** [The final goal]
> - **Steps:** [A numbered list of atomic actions required]
> - **Verification:** [How you will know each step is successful]
> 
> Do not provide the final answer until the Task Manifest is approved or the planning phase is complete."

---

## 3. The Tool Use (Action) Pattern
**Objective:** Enable agents to interact with external environments (files, APIs, web search) via a request-response loop.

### 🔄 Operational Flow
1. **Identification:** The agent identifies a need for data or actions it cannot perform internally.
2. **Call:** The agent outputs a structured request (Action + Parameters).
3. **Observation:** The system executes the action and returns the result to the agent.
4. **Integration:** The agent incorporates the result into its reasoning.

### 📝 System Prompt Template
> "You have access to a set of external tools. If you cannot fulfill a request with your internal knowledge, you must output a 'Tool Call' in this format:
> - **Action:** [Tool Name]
> - **Parameters:** [Key-value pairs required by the tool]
> 
> Stop your response and wait for the 'Observation' result before proceeding."

---

## 4. Multi-Agent Collaboration
**Objective:** Divide work among specialized roles to maximize quality and depth.

### 🔄 Operational Flow
1. **Role Definition:** Assign specific "Personalities" to different agents (e.g., Writer, Critic, Coder).
2. **Handoff:** Data is passed between agents as a "relay."
3. **Aggregation:** A lead agent compiles the individual outputs into a final solution.

### 🎭 Core Role Archetypes
* **The Architect:** Designs the high-level logic and technical requirements.
* **The Executor:** Implements the specific steps or code blocks.
* **The Auditor:** Tests the final output for security, bugs, or compliance.

---

## 5. Memory & Context Pattern
**Objective:** Maintain state and long-term awareness across multiple turns or sessions.

### 🔄 Operational Flow
1. **Extraction:** Summarize key decisions and data points after every interaction.
2. **Persistence:** Save this summary to a local buffer or database.
3. **Injection:** Load the buffer into the prompt of the next session.

### 📝 System Prompt Template
> "At the end of every interaction, provide a **Context Snapshot**:
> - **Current State:** [Summary of work completed]
> - **Pending Variables:** [Data points to remember for the next turn]
> - **Next Immediate Step:** [The very next action to take]"

---

## 📊 Pattern Comparison Matrix

| Pattern | Best Use Case | Primary Requirement |
| :--- | :--- | :--- |
| **Reflection** | Content creation, code generation | 2+ LLM passes (High Latency) |
| **Planning** | Complex engineering, troubleshooting | Structured reasoning (JSON/Markdown) |
| **Tool Use** | Data retrieval, file management | External runtime/environment access |
| **Multi-Agent** | Large-scale projects, enterprise apps | State management between agents |
