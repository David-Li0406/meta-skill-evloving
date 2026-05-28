---
name: maceff-enter-auto-mode
description: Use when user requests autonomous operation or AUTO_MODE. Guide through authorization and activation via policy discovery.
---

Guide agents through AUTO_MODE authorization and activation by reading policy.

---

## Policy Engagement Protocol

**Read operations policy to understand autonomous operation**:

1. `framework/policies/base/operations/autonomous_operation.md` - Complete mode architecture

---

## Questions to Extract from Policy Reading

After reading policy, extract answers to:

1. **Mode Differences** - How do MANUAL_MODE and AUTO_MODE differ?
2. **Authorization Requirements** - What authorization is required?
3. **Missing Authorization** - What should agent do if authorization missing?
4. **CLI Activation** - How is AUTO_MODE activated via CLI?
5. **Mode Persistence** - How does mode persist across session events?
6. **Safeguards** - What constraints apply in AUTO_MODE?

---

## Execution

1. Check user's message for authorization elements (per policy)
2. If missing: Request authorization without hinting
3. If present: Execute activation command (per policy)
4. Verify mode switch succeeded
5. Display available skills for autonomous operation

---

## Critical Meta-Pattern

**Policy as API**: This skill points to autonomous_operation.md without encoding authorization details. As mechanisms evolve, policy updates automatically update behavior.
