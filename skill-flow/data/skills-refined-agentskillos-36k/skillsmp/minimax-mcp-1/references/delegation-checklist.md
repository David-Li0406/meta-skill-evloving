# MiniMax Delegation Checklist

Before starting ANY task, ask yourself:

## ☑️ Pre-Task Checklist
- [ ] Does this involve web research? → Consider MiniMax
- [ ] Does this require image analysis? → Use MiniMax
- [ ] Will this use >500 tokens without delegation? → Consider MiniMax
- [ ] Am I about to read multiple documentation files? → Consider MiniMax first
- [ ] Is there current/recent information I need (2024-2026)? → Use MiniMax

## ☑️ During Task Checklist
- [ ] Am I manually synthesizing info from multiple sources? → Should have considered MiniMax
- [ ] Am I comparing approaches/libraries from docs? → Should have considered MiniMax
- [ ] Am I grepping through many files for research? → Should have considered MiniMax
- [ ] Has my token usage exceeded 500 tokens on research? → Should have considered MiniMax

## ☑️ Correct Delegation Flow
1. **Identify** token-intensive work (research, web search, image analysis)
2. **Check** if task involves trusted domains (see SKILL.md)
3. **Formulate** clear query for MiniMax
4. **Execute** via curl to MiniMax API
5. **Review** results (minimal tokens)
6. **Synthesize** findings for user

## ☑️ Trusted Domains (Auto-Approved)
- docs.anthropic.com
- platform.claude.com
- docs.cursor.com
- cursor.com
- cookbook.openai.com
- godotengine.org
- api.minimax.io

**For other domains**: Ask Sam for permission before searching

## ☑️ MiniMax API Quick Reference

**Web Search:**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"your query"}'
```

**Web Search (Trusted Domain):**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"site:godotengine.org your query"}'
```

**Image Analysis:**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt":"analysis prompt","image_url":"https://..."}'
```

## Decision Tree

```
Task assigned
     ↓
Is it research/web search/image analysis?
     ↓
   Yes → Check if trusted domains involved
           ↓
         Yes → Use MiniMax (auto-approved)
           ↓
         No → Ask Sam for permission
     ↓
   No → Is it local codebase search?
           ↓
         Yes → Use Grep/Glob/Read
           ↓
         No → Use appropriate tool
```

## Token Efficiency Guide

| Task Type | Without MiniMax | With MiniMax | Savings |
|-----------|----------------|--------------|---------|
| Web research | 1500-3000 tokens | 200-500 tokens | 85-90% |
| Image analysis | N/A (can't do) | 200-400 tokens | Task enabled |
| Multi-doc research | 2000+ tokens | 300-600 tokens | 75-85% |
| Code comparison | 1000-2000 tokens | 200-400 tokens | 80-90% |

## Quick Examples

**✅ Good - Delegate to MiniMax:**
- "How does Godot 4.5 handle signals?" → Search godotengine.org
- "Analyze this screenshot for bugs" → Use VLM API
- "What are Claude Code best practices?" → Search docs.anthropic.com

**✅ Good - Use Local Tools:**
- "Find where player_health is defined" → Grep codebase
- "Read game/player.gd" → Read tool
- "List all .gd files in game/" → Glob tool

**❌ Avoid - Manual research:**
- Reading 10+ documentation files manually
- Using WebSearch when MiniMax handles trusted domains
- Trying to "describe" images instead of using VLM API
