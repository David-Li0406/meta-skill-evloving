---
name: claudish-usage
description: Use this skill when you need to run Claude Code with OpenRouter models through sub-agents, ensuring context efficiency and proper delegation.
---

# Claudish Usage Skill

**Version:** 2.0.0  
**Purpose:** Guide AI agents on how to use Claudish CLI to run Claude Code with various AI models while maintaining context integrity.  
**Status:** Production Ready

## ⚠️ CRITICAL RULES - READ FIRST

### 🚫 NEVER Run Claudish from Main Context

**Claudish MUST ONLY be run through sub-agents** unless the user **explicitly** requests direct execution.

**Why:**
- Running Claudish directly pollutes main context with 10K+ tokens (full conversation + reasoning).
- Destroys context window efficiency.
- Makes main conversation unmanageable.

### When to Run Claudish Directly:
- ✅ User explicitly says "run claudish directly" or "don't use a sub-agent".
- ✅ User is debugging and wants to see full output.
- ✅ User specifically requests main context execution.

### When to Use Sub-Agent:
- ✅ User says "use Grok to implement X" (delegate to sub-agent).
- ✅ User says "ask GPT-5 to review X" (delegate to sub-agent).
- ✅ User mentions any model name without "directly" (delegate to sub-agent).
- ✅ Any production task (always delegate).

### 📋 Workflow Decision Tree

```
User Request
    ↓
Does it mention Claudish/OpenRouter/model name? → NO → Don't use this skill
    ↓ YES
    ↓
Does user say "directly" or "in main context"? → YES → Run in main context (rare)
    ↓ NO
    ↓
Find appropriate agent or create one → Delegate to sub-agent (default)
```

## 🤖 Agent Selection Guide

### Step 1: Find the Right Agent

**When user requests a Claudish task, follow this process:**

1. **Check for existing agents** that support proxy mode or external model delegation.
2. **If no suitable agent exists:**
   - Suggest creating a new proxy-mode agent for this task type.
   - Offer to proceed with a generic `general-purpose` agent if the user declines.
3. **If user declines agent creation:**
   - Warn about context pollution.
   - Ask if they want to proceed anyway.

### Step 2: Agent Type Selection Matrix

| Task Type | Recommended Agent | Fallback | Notes |
|-----------|------------------|----------|------|
|           |                  |          |      |