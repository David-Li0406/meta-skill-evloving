# Agentic Sovereignty & NHI Security (2025-2026)
## 1. Non-Human Identity (NHI) Governance
AI agents are "Non-Human Identities" that act on behalf of users. They are the #1 breach vector in late 2025.
### The NHI Lifecycle Audit
- [ ] **Ephemeral Identities:** Are API keys created by agents set with an automatic TTL (Time-to-Live)? (🔴 **Critical:** Ban persistent NHI tokens).
- [ ] **Sovereignty Scoping:** If an agent spawns a sub-agent, does it pass down a *restricted* subset of its own permissions (Recursive Least Privilege)?
- [ ] **Identity Attribution:** Is every action taken by an agent tagged with both the `agent_id` and the `origin_user_id`?
### Tool-Based Identity Risks
- [ ] **SSO for Agents:** Is the agent using OIDC/Workload Identity Federation rather than static secrets to access cloud resources?
- [ ] **Credential Leakage in Memory:** Verify that the agent's long-term memory (Vector DB) doesn't accidentally store API keys or session tokens retrieved during tool execution.
## 2. Agentic "State" Security
- [ ] **Memory Poisoning:** Can an external user "poison" the agent's memory (via chat or indirect injection) to alter its future behavior?
- [ ] **Goal Manipulation:** Review the "Sovereign Constraints" in the system prompt. Is the agent forbidden from modifying its own core safety objectives?
- [ ] **Cascading Hallucinations:** In multi-agent workflows, does Agent B validate the "facts" provided by Agent A before executing a tool?
## 3. Guardrail Implementation
- [ ] **Runtime Enforcement:** Are tools wrapped in a "Policy Proxy" (e.g., an MCP Gateway) that blocks unauthorized actions at the protocol level?
- [ ] **The "Red Button":** Is there a global "Kill Switch" that can instantly revoke all active NHI tokens if an agent begins exhibiting emergent, destructive behavior?
## 4. 2025 Threat Matrix: Agentic AI
| Threat | Root Cause | Mitigation |
| :--- | :--- | :--- |
| **Orphaned NHI** | Task completion without token cleanup. | Automated TTL on all service accounts. |
| **Recursive Injection** | Agent A executes Agent B with a poisoned prompt. | Strict "System Prompt Isolation" between agents. |
| **Tool Hijacking** | Model-invoked tool parameters are manipulated. | Strict Zod schema validation for all tool inputs. |
