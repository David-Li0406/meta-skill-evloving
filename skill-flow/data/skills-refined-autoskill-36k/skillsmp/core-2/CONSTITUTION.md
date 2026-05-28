# QARA SYSTEM CONSTITUTION

**The Foundational Philosophy of Jean-Marc Giorgi's Personal AI Infrastructure**

**Last Updated:** 2026-01-02
**Status:** Active - Canonical reference for Qara architectural decisions

---

## Core Philosophy

**Qara is scaffolding for AI, not a replacement for human intelligence.**

The system is designed on the principle that **AI systems need structure to be reliable**. Like physical scaffolding supports construction work, Qara provides the architectural framework that makes AI assistance dependable, maintainable, and effective.

### The Central Insight

**Deterministic systems are more reliable than probabilistic ones.**

When you can predict what will happen, you can:
- Build on it
- Test it
- Trust it
- Scale it
- Fix it when it breaks

This is why Qara emphasizes:
- CLI tools over ad-hoc prompting
- Code before prompts
- Specifications before implementation
- Tests before features

---

## The Eight Founding Principles

### 1. Scaffolding > Model

**The system architecture matters more than the underlying AI model.**

A well-structured system with good scaffolding will outperform a more powerful model with poor structure. Qara's value comes from:

- Organized workflows that guide AI execution
- Routing systems that activate the right context
- Quality gates that verify outputs
- History systems that enable learning

**Key Takeaway:** Build the scaffolding first, then add the AI.

### 2. As Deterministic as Possible

**Favor predictable, repeatable outcomes over flexibility.**

In production systems, consistency beats creativity:

- Same input → Same output (always)
- No reliance on prompt variations
- No dependence on model mood
- Behavior defined by code, not prompts
- Version control tracks explicit changes

**Key Takeaway:** If it can be made deterministic, make it deterministic.

### 3. Code Before Prompts

**Write code to solve problems, use prompts to orchestrate code.**

Prompts should never replicate functionality that code can provide:

❌ **Bad:** Prompt AI to parse JSON, transform data, format output
✅ **Good:** Write TypeScript to parse/transform/format, prompt AI to call it

**Key Takeaway:** Code is cheaper, faster, and more reliable than prompts.

### 4. CLI as Interface

**Every operation should be accessible via command line.**

Command line interfaces provide:
- Discoverability (--help shows all commands)
- Scriptability (commands can be automated)
- Testability (test CLI independently of AI)
- Flexibility (use with or without AI)
- Transparency (see exactly what was executed)

**Key Takeaway:** If there's no CLI command for it, you can't script it or test it reliably.

### 5. Goal → Code → CLI → Prompts

**The proper development pipeline for any new feature.**

```
User Goal
    ↓
Understand Requirements (what needs to happen)
    ↓
Write Deterministic Code (how it happens)
    ↓
Wrap as CLI Tool (make it accessible)
    ↓
Add AI Prompting (make it easy to use)
```

**Key Takeaway:** Each layer builds on the previous. Skip a layer, get a shaky system.

### 6. Spec/Test/Evals First

**Define expected behavior before writing implementation.**

- Write test before implementation
- Test should fail initially
- Implement until test passes
- Refactor while tests pass

**Key Takeaway:** If you can't specify it, you can't test it. If you can't test it, you can't trust it.

### 7. Meta/Self Updates

**The system should be able to improve itself.**

Qara can update its own documentation, modify skill files, add new workflows, create new tools, and deploy changes to itself.

**Key Takeaway:** A system that can't update itself will stagnate. Build the capability to evolve.

### 8. Custom Skill Management

**Skills are the organizational unit for all domain expertise.**

Skills are more than documentation - they are active orchestrators:

- **Self-activating:** Trigger automatically based on user request
- **Self-contained:** Package all context, workflows, and assets
- **Composable:** Can call other skills and agents
- **Evolvable:** Easy to add, modify, or deprecate
- **Discoverable:** Natural language routing to right skill

**Key Takeaway:** Skills are how Qara scales - each new domain gets its own skill, maintaining organization as the system grows.

---

## Architecture Quick Reference

For detailed implementation, see the reference files below. This section provides the conceptual overview.

### The Three Primitives

| Primitive | Purpose | When to Use |
|-----------|---------|-------------|
| **Skills** | Meta-containers for domain expertise | Need competence in topic/domain |
| **Commands** | Discrete task workflows within skills | Repeatable task with clear steps |
| **Agents** | Autonomous task executors | Need specialized expertise or parallel execution |

### Progressive Disclosure (3-Tier Context)

| Tier | Location | When Loaded |
|------|----------|-------------|
| **Tier 1** | Skill `description:` YAML | Always (session start) |
| **Tier 2** | SKILL.md body | When skill activates |
| **Tier 3** | Reference files | Just-in-time when needed |

---

## The Nine Commandments

1. **Command Line First** - Build CLI tools before AI wrappers
2. **Deterministic Code First** - Same input always produces same output
3. **Prompts Wrap Code** - AI orchestrates tools, doesn't replace them
4. **Progressive Disclosure** - Load context only when needed (3 tiers)
5. **Skills-as-Containers** - Package expertise with routing and workflows
6. **System Prompt Routing** - Natural language triggers automatic skill activation
7. **The Three Primitives** - Skills, Commands, Agents work together
8. **Test-Driven Development** - All tools tested independently before AI integration
9. **Quality Gates** - Never skip validation steps before declaring completion

---

## When Building New Qara Systems

**Always ask:**
1. Can this be a CLI tool? (If yes → build CLI first)
2. Will this be called >10 times? (If yes → make it deterministic)
3. Does this need AI? (AI should orchestrate, not implement)
4. What's the routing trigger? (Define in skill description)
5. Where does this fit? (Skill, Command, or Agent?)
6. How do I test this? (Write tests before implementation)
7. What tier is this context? (System prompt, SKILL.md, or reference file?)

---

## Reference Documentation

**For implementation details, see:**

| Topic | Reference File |
|-------|----------------|
| CLI-First implementation | `cli-first-guide.md` |
| Testing guide | `testing-guide.md` |
| Security protocols | `security-protocols.md` |
| Agent system | `agent-guide.md` |
| Delegation patterns | `delegation-guide.md` |
| History system | `history-system.md` |

---

**END OF CONSTITUTION**

**This document defines what Qara is at the most fundamental level. Implementation details live in the reference files above.**
