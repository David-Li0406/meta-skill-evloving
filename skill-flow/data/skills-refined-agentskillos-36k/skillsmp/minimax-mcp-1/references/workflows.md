# MiniMax MCP Workflows

Detailed usage patterns, examples, and best practices for MiniMax MCP integration.

## Core Workflow Principles

### Token Efficiency Pattern
The fundamental principle: **Claude plans and reviews, MiniMax executes**

1. **Claude Plans** (~50-100 tokens): Structure approach, define requirements
2. **MiniMax Executes** (~2000 tokens): Heavy computation, research, analysis
3. **Claude Reviews** (~50-100 tokens): Quality control, synthesis, decisions

**Result**: 85-90% token savings

---

## Workflow 1: Research Delegation

### When to Use
- Comprehensive web research required
- Multiple sources need synthesis
- Current information needed
- Extensive reading and analysis

### Pattern
```
Claude: "Research X using MiniMax"
Terminal: Execute search via API
Claude: Review and synthesize results
```

### Example: Godot Features Research

**Step 1: Claude Plans**
```
I'll research Godot 4.5 features using MiniMax for comprehensive web search.
This will gather current information from multiple sources efficiently.
```

**Step 2: MiniMax Executes**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"Godot 4.5 new features 2025"}'
```

**Response**: 7+ search results with titles, links, snippets

**Step 3: Claude Reviews**
```
Based on the MiniMax search results, here are the key Godot 4.5 features:
1. Performance improvements...
2. New rendering features...
3. Enhanced physics...
[Synthesizes findings from all results]
```

### Advanced: Multi-Query Research

```bash
# Query 1: Overview
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -d '{"q":"Godot 4.5 features overview"}'

# Query 2: Performance
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -d '{"q":"Godot 4.5 performance improvements"}'

# Query 3: Rendering
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -d '{"q":"Godot 4.5 rendering new features"}'

# Claude synthesizes all results
```

### Benefits
✅ **85% token reduction**: MiniMax searches 7+ sources
✅ **Current information**: Real-time web data
✅ **Comprehensive**: Multiple perspectives
✅ **Fast**: Parallel searches possible

---

## Workflow 2: Image Analysis

### When to Use
- Screenshot debugging
- UI/UX analysis
- Visual bug identification
- Image understanding tasks

### Pattern
```
Claude: "Analyze this screenshot"
MiniMax: Understand image content
Claude: Interpret analysis, provide insights
```

### Example: Debug Screenshot

**Step 1: Claude Plans**
```
I'll analyze this screenshot for UI bugs using MiniMax vision capabilities.
```

**Step 2: MiniMax Analyzes**

**Option A: Image URL**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt":"What UI bugs or issues do you see?","image_url":"https://example.com/bug-screenshot.png"}'
```

**Option B: Local File**
```bash
IMAGE_B64=$(base64 -w 0 screenshot.png)
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d "{\"prompt\":\"Analyze UI layout\",\"image_base64\":\"$IMAGE_B64\"}"
```

**Response**: Detailed vision analysis

**Step 3: Claude Interprets**
```
Based on MiniMax analysis, I found these issues:
1. Button alignment: Off by 5px in top-right corner
2. Color contrast: Text too light on background
3. Missing tooltip: Hover state not visible
Recommendations: [actionable fixes]
```

### Use Cases

#### Bug Triage
```bash
# Quick bug identification
curl -d '{"prompt":"List all visual bugs","image_url":"screenshot.png"}'
```

#### UI Audit
```bash
# Comprehensive UI review
curl -d '{"prompt":"Audit this interface for accessibility, layout, and usability","image_url":"ui-mockup.png"}'
```

#### Visual Regression
```bash
# Compare with expected
curl -d '{"prompt":"Compare this with a modern design system. What needs updating?","image_url":"old-ui.png"}'
```

### Benefits
✅ **Instant analysis**: No manual inspection needed
✅ **Detailed insights**: Comprehensive visual understanding
✅ **Actionable feedback**: Specific recommendations
✅ **Multiple formats**: Supports URL and local files

---

## Workflow 3: Plan Execution

### When to Use
- Complex multi-step tasks
- Research and development projects
- Comprehensive analysis required
- Delegating heavy work

### Pattern
```
Claude: Create structured plan
MiniMax: Execute comprehensive research
Claude: Review and validate results
```

### Example: Technology Evaluation

**Step 1: Claude Creates Plan**
```
Plan: Evaluate React 18 for our project

Structure:
1. Research React 18 features
2. Analyze performance improvements
3. Review adoption status
4. Compare with alternatives
5. Provide recommendation

Execute via MiniMax for thorough research.
```

**Step 2: MiniMax Executes**
```bash
./scripts/execute-plan.sh "Evaluate React 18 for enterprise project"

# Or manual execution:
curl -d '{"q":"React 18 enterprise features performance adoption"}'
curl -d '{"q":"React 18 vs Vue 3 comparison 2025"}'
curl -d '{"q":"React 18 migration guide best practices"}'
```

**Step 3: Claude Reviews**
```
React 18 Evaluation Summary:

Features:
- Concurrent rendering
- Automatic batching
- Suspense improvements

Performance:
- 30% faster initial render
- Reduced memory usage

Recommendation: Adopt React 18 with 6-month migration plan
```

### Benefits
✅ **Comprehensive**: Covers all aspects
✅ **Structured**: Organized approach
✅ **Validated**: Multiple sources
✅ **Actionable**: Clear recommendations

---

## Workflow 4: Terminal Claude Integration

### Setup for Terminal Claude

**Step 1: Verify Environment**
```bash
./scripts/test-connection.sh
```

**Step 2: Set Up Quick Commands**
```bash
# Create alias
alias minimax-search='curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP"'

# Use it
minimax-search "Godot 4.5" | python3 -m json.tool
```

**Step 3: Create Wrapper Script**
```bash
#!/bin/bash
# minimax-quick.sh
QUERY="$1"
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d "{\"q\":\"$QUERY\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('organic', []):
    print(f'• {r.get(\"title\")}')
    print(f'  {r.get(\"link\")}')
    print()
"
```

### Workflow in Terminal

**Claude**: "I'll search for Docker best practices"
**Terminal**: `./minimax-quick.sh "Docker best practices 2025"`
**Claude**: "Based on results, here are the key practices..."

### Benefits
✅ **Immediate results**: No server startup
✅ **Scriptable**: Integrates with workflows
✅ **Flexible**: Custom queries
✅ **Efficient**: Direct API access

---

## Workflow 5: Desktop Claude with MCP

### Setup for Desktop Claude

**Step 1: Start MCP Server**
```bash
MINIMAX_API_KEY="..." MINIMAX_API_HOST="..." uvx minimax-coding-plan-mcp -y
```

**Step 2: Verify Tools Available**
```bash
# In Claude Desktop, tools should be available:
# - mcp__minimax__web_search
# - mcp__minimax__understand_image
```

**Step 3: Use Native Tools**
```
web_search(query="Godot 4.5 features")
understand_image(prompt="Analyze this UI", image_source="screenshot.png")
```

### Benefits
✅ **Native integration**: Tools built into Claude
✅ **Easy to use**: Simple function calls
✅ **Automatic**: No manual curl commands
✅ **Consistent**: Unified interface

---

## Workflow 6: Cursor IDE Integration

### Using Existing Slash Commands

**Step 1: Check Available Commands**
```bash
ls .cursor/commands/
# minimax-plan.json
# minimax-execute.json
# minimax-analyze.json
# minimax-mcp.json
```

**Step 2: Use Command**
```
/minimax-plan "Research Godot 4.5 features"
/minimax-execute
/minimax-analyze "screenshot.png"
```

**Step 3: Review Generated Plan**
```json
{
  "task": "Research Godot 4.5 features",
  "created_at": "2026-01-19T...",
  "todos": [...]
}
```

### Benefits
✅ **IDE integration**: Native Cursor support
✅ **Structured**: Plans in JSON format
✅ **Collaborative**: Multiple commands work together
✅ **Traceable**: All plans logged

---

## Advanced Patterns

### Pattern 1: Parallel Research

```bash
# Execute multiple queries in parallel
(
  curl -s -d '{"q":"React 18 features"}' &
  curl -s -d '{"q":"React 18 performance"}' &
  curl -s -d '{"q":"React 18 migration"}' &
) | wait

# Claude reviews all results together
```

### Pattern 2: Iterative Refinement

```bash
# Initial broad search
curl -d '{"q":"game engines 2025"}'

# Refine based on results
curl -d '{"q":"Godot vs Unity vs Unreal 2025"}'

# Deep dive
curl -d '{"q":"Godot 4.5 vs Unity 2025 comparison"}'

# Claude synthesizes progressively
```

### Pattern 3: Image + Text Analysis

```bash
# Analyze screenshot
ANALYSIS=$(curl -s -d '{"prompt":"What bugs?","image_url":"bug.png"}')

# Search for solutions
curl -s -d '{"q":"Godot UI button alignment fix"}'

# Claude combines both
```

### Pattern 4: Batch Processing

```bash
# Process multiple images
for img in *.png; do
  echo "Analyzing $img..."
  curl -s -d "{\"prompt\":\"Analyze\",\"image_url\":\"$img\"}"
  sleep 1  # Rate limiting
done
```

---

## Best Practices

### 1. Choose the Right Integration

| Scenario | Method |
|----------|--------|
| Quick research | Direct API (curl) |
| Image analysis | Direct API |
| Complex workflows | MCP server |
| IDE integration | Slash commands |
| Batch processing | Scripts |

### 2. Optimize for Token Efficiency

**❌ Wrong**: Claude does everything
```
Claude: "Search for X, analyze Y, compare Z, summarize..."
Tokens: 3000+
```

**✅ Correct**: Delegate to MiniMax
```
Claude: "Use MiniMax to research X"
MiniMax: Executes search
Claude: "Review these results"
Tokens: 100 (Claude) + 0 (API) vs 3000 (all in Claude)
```

### 3. Handle Errors

```bash
#!/usr/bin/env bash
query="$1"
result=$(curl -s -w "\n%{http_code}" -d "{\"q\":\"$query\"}" ...)

http_code=$(echo "$result" | tail -n1)
if [ "$http_code" != "200" ]; then
    echo "Error: HTTP $http_code"
    exit 1
fi

# Process results
echo "$result" | python3 -c "..."
```

### 4. Rate Limiting

```bash
# Add delays
sleep 1

# Or use token bucket
./scripts/rate-limited-search.sh "query1"
./scripts/rate-limited-search.sh "query2"
```

### 5. Caching Results

```bash
# Cache search results
CACHE_FILE="$HOME/.cache/minimax/$(echo "$query" | md5sum | cut -d' ' -f1).json"

if [ -f "$CACHE_FILE" ] && [ $(($(date +%s) - $(stat -c %Y "$CACHE_FILE"))) -lt 3600 ]; then
    cat "$CACHE_FILE"  # Use cached
else
    curl -s ... | tee "$CACHE_FILE"  # Fetch and cache
fi
```

---

## Workflow Selection Guide

### Quick Decision Tree

**Need web search?**
- Yes → Use direct API or MCP tools

**Need image analysis?**
- Yes → Use direct API or MCP tools

**Complex multi-step task?**
- Yes → Use execute-plan workflow

**Quick one-off query?**
- Yes → Use direct API

**IDE integration needed?**
- Yes → Use slash commands

**High-volume processing?**
- Yes → Use scripts with rate limiting

---

## Example Workflows Repository

### Research Project
```bash
# 1. Plan
echo "Research: AI trends 2025"

# 2. Execute
./scripts/execute-plan.sh "AI trends 2025 comprehensive research"

# 3. Review
# Claude synthesizes findings
```

### Bug Analysis
```bash
# 1. Analyze screenshot
./scripts/analyze-image.sh "What bugs?" "bug.png"

# 2. Search for solutions
./scripts/web-search.sh "Godot UI bug fix button alignment"

# 3. Combine results
# Claude provides solution
```

### Technology Evaluation
```bash
# 1. Create structured plan
# Claude creates evaluation criteria

# 2. Research each criterion
./scripts/web-search.sh "React 18 features"
./scripts/web-search.sh "React 18 performance"
./scripts/web-search.sh "React 18 adoption"

# 3. Analyze results
# Claude provides recommendation
```

---

## Summary

**Key Principle**: Claude plans and reviews, MiniMax executes

**Token Efficiency**: 85-90% savings

**Integration Methods**:
1. Direct API (curl) - Terminal Claude
2. MCP Server - Desktop Claude
3. Slash Commands - Cursor IDE

**Best Practices**:
- Delegate heavy work to MiniMax
- Use appropriate integration method
- Handle errors gracefully
- Implement rate limiting
- Cache results when possible

**Production Ready**: ✅ Verified 2026-01-19
