---
name: claudish-usage
description: CRITICAL - Guide for using Claudish CLI ONLY through sub-agents to run Claude Code with any AI model (OpenRouter, Gemini, OpenAI, local models). NEVER run Claudish directly in main context unless user explicitly requests it. Use when user mentions external AI models, Claudish, OpenRouter, Gemini, OpenAI, Ollama, or alternative models. Includes mandatory sub-agent delegation patterns, agent selection guide, file-based instructions, and strict rules to prevent context window pollution.
---

# Claudish Usage Skill

**Version:** 2.0.0  
**Purpose:** Guide AI agents on how to use Claudish CLI to run Claude Code with any AI model.  
**Status:** Production Ready  

## ⚠️ CRITICAL RULES - READ FIRST

### 🚫 NEVER Run Claudish from Main Context

**Claudish MUST ONLY be run through sub-agents** unless the user **explicitly** requests direct execution.

**Why:**
- Running Claudish directly pollutes main context with 10K+ tokens (full conversation + reasoning)
- Destroys context window efficiency
- Makes main conversation unmanageable

**When you can run Claudish directly:**
- ✅ User explicitly says "run claudish directly" or "don't use a sub-agent"
- ✅ User is debugging and wants to see full output
- ✅ User specifically requests main context execution

**When you MUST use sub-agent:**
- ✅ User says "use Grok to implement X" (delegate to sub-agent)
- ✅ User says "ask GPT-5 to review X" (delegate to sub-agent)
- ✅ User mentions any model name without "directly" (delegate to sub-agent)
- ✅ Any production task (always delegate)

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

**When user requests Claudish task, follow this process:**

1. **Check for existing agents** that support proxy mode or external model delegation
2. **If no suitable agent exists:**
   - Suggest creating a new proxy-mode agent for this task type
   - Offer to proceed with generic `general-purpose` agent if user declines
3. **If user declines agent creation:**
   - Warn about context pollution
   - Ask if they want to proceed anyway

### Step 2: Agent Type Selection Matrix

| Task Type | Recommended Agent | Fallback | Notes |
|-----------|------------------|----------|-------|
| **Code implementation** | Create coding agent with proxy mode | `general-purpose` | Best: custom agent for project-specific patterns |
| **Code review** | Use existing code review agent + proxy | `general-purpose` | Check if plugin has review agent first |
| **Architecture planning** | Use existing architect agent + proxy | `general-purpose` | Look for `architect` or `planner` agents |
| **Testing** | Use existing test agent + proxy | `general-purpose` | Look for `test-architect` or `tester` agents |
| **Refactoring** | Create refactoring agent with proxy | `general-purpose` | Complex refactors benefit from specialized agent |
| **Documentation** | `general-purpose` | - | Simple task, generic agent OK |
| **Analysis** | Use existing analysis agent + proxy | `general-purpose` | Check for `analyzer` or `detective` agents |
| **Other** | `general-purpose` | - | Default for unknown task types |

### Step 3: Agent Creation Offer (When No Agent Exists)

**Template response:**
```
I notice you want to use [Model Name] for [task type].

RECOMMENDATION: Create a specialized [task type] agent with proxy mode support.

This would:
✅ Provide better task-specific guidance
✅ Reusable for future [task type] tasks
✅ Optimized prompting for [Model Name]

Options:
1. Create specialized agent (recommended) - takes 2-3 minutes
2. Use generic general-purpose agent - works but less optimized
3. Run directly in main context (NOT recommended - pollutes context)

Which would you prefer?
```

### Step 4: Common Agents by Plugin

**Frontend Plugin:**
- `typescript-frontend-dev` - Use for UI implementation with external models
- `frontend-architect` - Use for architecture planning with external models
- `senior-code-reviewer` - Use for code review (can delegate to external models)
- `test-architect` - Use for test planning/implementation

**Bun Backend Plugin:**
- `backend-developer` - Use for API implementation with external models
- `api-architect` - Use for API design with external models

**Code Analysis Plugin:**
- `codebase-detective` - Use for investigation tasks with external models

**No Plugin:**
- `general-purpose` - Default fallback for any task

### Step 5: Example Agent Selection

**Example 1: User says "use Grok to implement authentication"**
```
Task: Code implementation (authentication)
Plugin: Bun Backend (if backend) or Frontend (if UI)

Decision:
1. Check for backend-developer or typescript-frontend-dev agent
2. Found backend-developer? → Use it with Grok proxy
3. Not found? → Offer to create custom auth agent
4. User declines? → Use general-purpose with file-based pattern
```

**Example 2: User says "ask GPT-5 to review my API design"**
```
Task: Code review (API design)
Plugin: Bun Backend

Decision:
1. Check for api-architect or senior-code-reviewer agent
2. Found? → Use it with GPT-5 proxy
3. Not found? → Use general-purpose with review instructions
4. Never run directly in main context
```

**Example 3: User says "use Gemini to refactor this component"**
```
Task: Refactoring (component)
Plugin: Frontend

Decision:
1. No specialized refactoring agent exists
2. Offer to create component-refactoring agent
3. User declines? → Use typescript-frontend-dev with proxy
4. Still no agent? → Use general-purpose with file-based pattern
```

## Overview

**Claudish** is a CLI tool that allows running Claude Code with any AI model via prefix-based routing. Supports OpenRouter (100+ models), direct Google Gemini API, direct OpenAI API, and local models (Ollama, LM Studio, vLLM, MLX).

**Key Principle:** **ALWAYS** use Claudish through sub-agents with file-based instructions to avoid context window pollution.

## What is Claudish?

Claudish (Claude-ish) is a proxy tool that:
- ✅ Runs Claude Code with **any AI model** via prefix-based routing
- ✅ Supports OpenRouter, Gemini, OpenAI, and local models
- ✅ Uses local API-compatible proxy server
- ✅ Supports 100% of Claude Code features
- ✅ Provides cost tracking and model selection
- ✅ Enables multi-model workflows

## Model Routing

| Prefix | Backend | Example |
|--------|---------|---------|
| _(none)_ | OpenRouter | `openai/gpt-5.2` |
| `g/` `gemini/` | Google Gemini | `g/gemini-2.0-flash` |
| `oai/` `openai/` | OpenAI | `oai/gpt-4o` |
| `ollama/` | Ollama | `ollama/llama3.2` |
| `lmstudio/` | LM Studio | `lmstudio/model` |
| `http://...` | Custom | `http://localhost:8000/model` |

**Use Cases:**
- Run tasks with different AI models (Grok for speed, GPT-5 for reasoning, Gemini for large context)
- Use direct APIs for lower latency (Gemini, OpenAI)
- Use local models for free, private inference (Ollama, LM Studio)
- Compare model performance on same task
- Reduce costs with cheaper models for simple tasks

## Requirements

### System Requirements
- **Claudish CLI** - Install with: `npm install -g claudish` or `bun install -g claudish`
- **Claude Code** - Must be installed
- **At least one API key** (see below)

### Environment Variables

```bash
# API Keys (at least one required)
export OPENROUTER_API_KEY='sk-or-v1-...'  # OpenRouter (100+ models)
export GEMINI_API_KEY='...'               # Direct Gemini API (g/ prefix)
export OPENAI_API_KEY='sk-...'            # Direct OpenAI API (oai/ prefix)

# Placeholder (required to prevent Claude Code dialog)
export ANTHROPIC_API_KEY='sk-ant-api03-placeholder'

# Custom endpoints (optional)
export GEMINI_BASE_URL='https://...'      # Custom Gemini endpoint
export OPENAI_BASE_URL='https://...'      # Custom OpenAI/Azure endpoint
export OLLAMA_BASE_URL='http://...'       # Custom Ollama server
export LMSTUDIO_BASE_URL='http://...'     # Custom LM Studio server

# Default model (optional)
export CLAUDISH_MODEL='openai/gpt-5.2'    # Default model
```

**Get API Keys:**
- OpenRouter: https://openrouter.ai/keys (free tier available)
- Gemini: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys
- Local models: No API key needed

## Quick Start Guide

### Step 1: Install Claudish

```bash
# With npm (works everywhere)
npm install -g claudish

# With Bun (faster)
bun install -g claudish

# Verify installation
claudish --version
```

### Step 2: Get Available Models

```bash
# List ALL OpenRouter models grouped by provider
claudish --models

# Fuzzy search models by name, ID, or description
claudish --models gemini
claudish --models "grok code"

# Show top recommended programming models (curated list)
claudish --top-models

# JSON output for parsing
claudish --models --json
claudish --top-models --json

# Force update from OpenRouter API
claudish --models --force-update
```

### Step 3: Run Claudish

**Interactive Mode (default):**
```bash
# Shows model selector, persistent session
claudish
```

**Single-shot Mode:**
```bash
# One task and exit (requires --model)
claudish --model x-ai/grok-code-fast-1 "implement user authentication"
```

**With stdin for large prompts:**
```bash
# Read prompt from stdin (useful for git diffs, code review)
git diff | claudish --stdin --model openai/gpt-5-codex "Review these changes"
```

## Recommended Models

**Top Models for Development (v3.1.1):**

| Model | Provider | Best For |
|-------|----------|----------|
| `openai/gpt-5.2` | OpenAI | **Default** - Most advanced reasoning |
| `minimax/minimax-m2.1` | MiniMax | Budget-friendly, fast |
| `z-ai/glm-4.7` | Z.AI | Balanced performance |
| `google/gemini-3-pro-preview` | Google | 1M context window |
| `moonshotai/kimi-k2-thinking` | MoonShot | Extended thinking |
| `deepseek/deepseek-v3.2` | DeepSeek | Code specialist |
| `qwen/qwen3-vl-235b-a22b-thinking` | Alibaba | Vision + reasoning |

**Direct API Options (lower latency):**

| Model | Backend | Best For |
|-------|---------|----------|
| `g/gemini-2.0-flash` | Gemini | Fast tasks, large context |
| `oai/gpt-4o` | OpenAI | General purpose |
| `ollama/llama3.2` | Local | Free, private |

**Get Latest Models:**
```bash
# List all models (auto-updates every 2 days)
claudish --models

# Search for specific models
claudish --models grok
claudish --models "gemini flash"

# Show curated top models
claudish --top-models

# Force immediate update
claudish --models --force-update
```

## NEW: Direct Agent Selection (v2.1.0)

**Use `--agent` flag to invoke agents directly without the file-based pattern:**

```bash
# Use specific agent (prepends @agent- automatically)
claudish --model x-ai/grok-code-fast-1 --agent frontend:developer "implement React component"

# Claude receives: "Use the @agent-frontend:developer agent to: implement React component"

# List available agents in project
claudish --list-agents
```

**When to use `--agent` vs file-based pattern:**

**Use `--agent` when:**
- Single, simple task that needs agent specialization
- Direct conversation with one agent
- Testing agent behavior
- CLI convenience

**Use file-based pattern when:**
- Complex multi-step workflows
- Multiple agents needed
- Large codebases
- Production tasks requiring review
- Need isolation from main conversation

**Example comparisons:**

**Simple task (use `--agent`):**
```bash
claudish --model x-ai/grok-code-fast-1 --agent frontend:developer "create button component"
```

**Complex task (use file-based):**
```typescript
// multi-phase-workflow.md
Phase 1: Use api-architect to design API
Phase 2: Use backend-developer to implement
Phase 3: Use test-architect to add tests
Phase 4: Use senior-code-reviewer to review

then:
claudish --model x-ai/grok-code-fast-1 --stdin < multi-phase-workflow.md
```

## Best Practice: File-Based Sub-Agent Pattern

### ⚠️ CRITICAL: Don't Run Claudish Directly from Main Conversation

**Why:** Running Claudish directly in main conversation pollutes context window with:
- Entire conversation transcript
- All tool outputs
- Model reasoning (can be 10K+ tokens)

**Solution:** Use file-based sub-agent pattern

### File-Based Pattern (Recommended)

**Step 1: Create instruction file**
```markdown
# /tmp/claudish-task-{timestamp}.md

## Task
Implement user authentication with JWT tokens

## Requirements
- Use bcrypt for password hashing
- Generate JWT with 24h expiration
- Add middleware for protected routes

## Deliverables
Write implementation to: /tmp/claudish-result-{timestamp}.md

## Output Format
```markdown
## Implementation

[code here]

## Files Created/Modified
- path/to/file1.ts
- path/to/file2.ts

## Tests
[test code if applicable]

## Notes
[any important notes]
```
```

**Step 2: Run Claudish with file instruction**
```bash
# Read instruction from file, write result to file
claudish --model x-ai/grok-code-fast-1 --stdin < /tmp/claudish-task-{timestamp}.md > /tmp/claudish-result-{timestamp}.md
```

**Step 3: Read result file and provide summary**
```typescript
// In your agent/command:
const result = await Read({ file_path: "/tmp/claudish-result-{timestamp}.md" });

// Parse result
const filesModified = extractFilesModified(result);
const summary = extractSummary(result);

// Provide short feedback to main agent
return `✅ Task completed. Modified ${filesModified.length} files. ${summary}`;
```

### Complete Example: Using Claudish in Sub-Agent

```typescript
/**
 * Example: Run code review with Grok via Claudish sub-agent
 */
async function runCodeReviewWith