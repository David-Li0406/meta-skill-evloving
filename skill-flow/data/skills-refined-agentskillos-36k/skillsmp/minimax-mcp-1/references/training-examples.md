# MiniMax Delegation Training Examples

Real-world examples showing correct vs incorrect delegation patterns for Godot game development.

## Example 1: Research Task

**User Request:** "How do I implement authentication in Godot?"

### ❌ Wrong Approach (High Token Usage)
```
Agent uses Glob to search for "auth*" files in codebase
Agent reads game/auth.gd (if exists)
Agent reads game/network.gd looking for auth code
Agent uses WebSearch tool
Agent synthesizes from local files + web results
Result: 1500+ tokens, may miss official best practices
```

### ✅ Correct Approach (Token-Efficient)
```bash
# Agent calls MiniMax immediately with trusted domain
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"site:godotengine.org authentication implementation patterns best practices"}'

# MiniMax returns comprehensive official docs
# Agent reviews results (100 tokens)
# Agent provides summary to user
Result: 85% token savings, official best practices
```

---

## Example 2: Image Analysis

**User Request:** "What's wrong with this game UI screenshot?"

### ❌ Wrong Approach (Task Fails)
```
Agent: "I can't analyze images directly, please describe what you see"
Or: Agent tries to use local screenshot analysis tools
Or: Agent asks user to manually describe UI elements
Result: User frustrated, task incomplete or requires manual work
```

### ✅ Correct Approach (Task Completed)
```bash
# Agent uses MiniMax VLM API
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt":"Analyze this Godot game UI screenshot for bugs, alignment issues, spacing problems, or visual hierarchy issues","image_url":"https://example.com/ui-screenshot.png"}'

# MiniMax provides detailed analysis:
# - Button overlapping text
# - Inconsistent spacing in dialogue box
# - Health bar alignment issue
# Agent presents findings to user with actionable fixes
Result: Task completed, token-efficient, actionable insights
```

---

## Example 3: Multi-Step Planning

**User Request:** "Create a plan to add dark mode to Hera's Garden"

### ❌ Wrong Approach (Inefficient)
```
Agent reads game/ui/theme.gd
Agent reads game/ui/settings.gd
Agent reads game/ui/main_menu.gd
Agent reads game/ui/dialogue_box.gd
Agent reads game/ui/inventory.gd
Agent synthesizes approach from 5+ files
Result: 2000+ tokens, may miss current best practices
```

### ✅ Correct Approach (Efficient)
```bash
# Step 1: Research current best practices via MiniMax
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -d '{"q":"site:godotengine.org dark mode theme implementation UI 2026"}'

# MiniMax returns: Theme resource pattern, Color override approach, etc.

# Step 2: Read only critical files identified from research
# Agent reads game/ui/theme.gd (targeted)
# Agent reads game/ui/settings.gd (targeted)

# Step 3: Create plan based on research + targeted code review
Result: Comprehensive plan, 80% token savings, modern best practices
```

---

## Example 4: Comparison Tasks

**User Request:** "Should I use signals or direct function calls for player-NPC interaction?"

### ❌ Wrong Approach (Token-Heavy)
```
Agent reads Godot docs about signals (local or web)
Agent reads docs about direct function calls
Agent reads examples in codebase
Agent compares and contrasts manually
Agent synthesizes recommendation
Result: 1000+ tokens
```

### ✅ Correct Approach (Efficient)
```bash
# Delegate comparison research to MiniMax
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -d '{"q":"site:godotengine.org signals vs direct function calls when to use decoupling performance"}'

# MiniMax provides comprehensive comparison:
# - Signals: Better for decoupling, event-driven, multiple listeners
# - Direct calls: Simpler, slightly faster, tight coupling
# - Use signals for UI events, gameplay events
# - Use direct calls for internal state changes

# Agent reviews and applies to user's specific context (200 tokens):
# "For player-NPC interaction, signals are better because..."
Result: 75% token savings, informed recommendation with context
```

---

## Example 5: Documentation Check

**User Request:** "Does Claude Code support MCP tools in plan mode?"

### ❌ Wrong Approach (Wrong Tool)
```
Agent uses Grep to search local .claude/ directory
Agent reads multiple local .md files
Agent tries to infer from codebase
Result: May miss official guidance, 800+ tokens
```

### ✅ Correct Approach (Authoritative Source)
```bash
# Search official Claude docs via MiniMax
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -d '{"q":"site:docs.anthropic.com OR site:platform.claude.com plan mode MCP tools bash API calls"}'

# MiniMax returns official docs confirming:
# - Plan mode supports read-only operations
# - Bash/curl for API calls is allowed
# - MCP tools are supported

# Agent reviews and answers with authority (100 tokens)
Result: 80% token savings, authoritative answer
```

---

## Example 6: Current Framework Comparison

**User Request:** "Compare GDUnit4 vs Gut for Godot testing in 2026"

### ❌ Wrong Approach (Outdated Info)
```
Agent reads local test files
Agent tries to infer from codebase structure
Agent may use outdated information
Result: May recommend outdated approach, 1000+ tokens
```

### ✅ Correct Approach (Current Best Practices)
```bash
# Get current 2026 information via MiniMax
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMyK6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -d '{"q":"GDUnit4 vs Gut Godot 4 testing framework comparison 2026"}'

# MiniMax returns current consensus:
# - GDUnit4: Active development, Godot 4 native, better tooling
# - Gut: Legacy option, less active
# - Recommendation: GDUnit4 for new projects

# Agent reviews and contextualizes for Hera's Garden
Result: Current best practices, 85% token savings
```

---

## Token Savings Summary

| Example | Without MiniMax | With MiniMax | Savings |
|---------|----------------|--------------|---------|
| Example 1: Research | 1500 tokens | 250 tokens | 83% |
| Example 2: Image Analysis | Task fails | 300 tokens | Task enabled |
| Example 3: Planning | 2000 tokens | 400 tokens | 80% |
| Example 4: Comparison | 1000 tokens | 250 tokens | 75% |
| Example 5: Documentation | 800 tokens | 150 tokens | 81% |
| Example 6: Framework Comparison | 1000 tokens | 200 tokens | 80% |

**Average savings: 80-85% on research tasks**

---

## Key Patterns to Remember

### ✅ Use MiniMax For:
- External documentation research (Godot, Claude, Cursor docs)
- Framework/library comparisons
- Best practices for current year (2024-2026)
- Image/screenshot analysis
- Multi-source information gathering

### ✅ Use Local Tools For:
- Finding specific code definitions (`player_health`)
- Reading specific known files
- Searching within the codebase
- File operations (list, glob, find files)

### Decision Rule:
**Before using Grep/Glob for research, ask:**
> "Would a MiniMax search to trusted docs handle this better?"

If researching external docs/practices → Use MiniMax
If searching known local code → Use local tools
