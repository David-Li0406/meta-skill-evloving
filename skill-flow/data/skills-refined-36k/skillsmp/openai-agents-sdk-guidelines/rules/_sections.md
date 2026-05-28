# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Agent Design (agent)

**Impact:** CRITICAL  
**Description:** Agents are the core building block. Proper configuration of name, instructions, model, tools, and output types is foundational to all agent workflows.

## 2. Multi-Agent Patterns (multi-agent)

**Impact:** CRITICAL  
**Description:** Choosing the right multi-agent pattern (manager/agents-as-tools vs handoffs) determines workflow architecture and control flow.

## 3. Tools (tool)

**Impact:** HIGH  
**Description:** Tools let agents take actions. Proper tool design with clear schemas, docstrings, and error handling is essential for reliable agent behavior.

## 4. Guardrails (guardrail)

**Impact:** MEDIUM-HIGH  
**Description:** Guardrails validate input and output, preventing misuse and ensuring quality. Critical for production deployments.

## 5. Context Management (context)

**Impact:** MEDIUM  
**Description:** Context provides dependency injection and state management. Consistent context types across agents/tools prevent runtime errors.

## 6. Running Agents (runner)

**Impact:** MEDIUM  
**Description:** The Runner orchestrates agent execution. Proper configuration of max_turns, run_config, and exception handling ensures reliable runs.

## 7. Conversation Management (conversation)

**Impact:** MEDIUM  
**Description:** Managing conversation history across turns enables multi-turn interactions. Choose manual, session-based, or server-managed approaches.

## 8. Streaming & Advanced (streaming)

**Impact:** LOW-MEDIUM  
**Description:** Streaming provides real-time updates during agent runs. Advanced patterns for MCP integration and custom event handling.
