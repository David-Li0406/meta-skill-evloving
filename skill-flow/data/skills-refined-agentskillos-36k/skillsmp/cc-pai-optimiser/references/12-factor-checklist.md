# 12-Factor Agents Compliance Checklist

Based on https://github.com/humanlayer/12-factor-agents

## Factor 1: Natural Language to Tool Calls

### Audit Questions
- [ ] Does the system convert natural language to structured tool calls?
- [ ] Are tool definitions clear with good descriptions?
- [ ] Is there proper schema validation on tool outputs?

### PAI Indicators
```bash
# Check for tool definitions
grep -r "tools\|functions\|schema" "$PAI_PATH" --include="*.json" --include="*.md"
```

### Optimization Signals
- Missing: Add tool schema definitions
- Weak: Improve tool descriptions for better LLM selection

---

## Factor 2: Own Your Prompts

### Audit Questions
- [ ] Are prompts stored in version-controlled files?
- [ ] Can prompts be modified without code changes?
- [ ] Is there prompt versioning/history?

### PAI Indicators
```bash
# Check for prompt files
find "$PAI_PATH" -name "*.prompt" -o -name "*prompt*.md" -o -name "CLAUDE.md"
```

### Optimization Signals
- Prompts hardcoded in code → Move to `context/` files
- No versioning → Add to git with meaningful commits
- Inline instructions → Extract to CLAUDE.md files

---

## Factor 3: Own Your Context Window

### Audit Questions
- [ ] Is context loading explicit and controlled?
- [ ] Is there progressive disclosure (load only what's needed)?
- [ ] Are context files under 500 lines each?
- [ ] Is there a context loading enforcement mechanism?

### PAI Indicators
```bash
# Context file sizes
find "$PAI_PATH" -name "CLAUDE.md" -exec wc -l {} \; | awk '{sum+=$1; if($1>500) print "⚠️  Large:", $2} END {print "Total lines:", sum}'

# Context hierarchy depth
find "$PAI_PATH/.claude/context" -type d | head -20
```

### Optimization Signals
- Files >500 lines → Split into references/
- No enforcement → Add hook-based loading
- Flat structure → Implement UFC hierarchy

---

## Factor 4: Tools Are Structured Outputs

### Audit Questions
- [ ] Are tools defined with proper JSON schemas?
- [ ] Is tool output validated before use?
- [ ] Are tool failures handled gracefully?

### PAI Indicators
```bash
# Check tool definitions
grep -r "tools\|schema" "$PAI_PATH/.claude" --include="*.json"
```

### Optimization Signals
- No schema validation → Add Zod/JSON Schema
- Unhandled errors → Add try-catch wrappers
- Missing descriptions → Enhance tool metadata

---

## Factor 5: Unify Execution State and Business State

### Audit Questions
- [ ] Is agent state stored in a single location?
- [ ] Can state be inspected during execution?
- [ ] Is state serializable for pause/resume?

### PAI Indicators
```bash
# Check for state management
grep -r "state\|context\|memory" "$PAI_PATH/.claude" --include="*.md"
```

### Optimization Signals
- Scattered state → Consolidate to working/ directory
- In-memory only → Persist to files
- Opaque state → Add logging/inspection

---

## Factor 6: Launch/Pause/Resume with Simple APIs

### Audit Questions
- [ ] Can the agent be paused mid-execution?
- [ ] Can sessions be resumed from checkpoints?
- [ ] Is there a clean API for lifecycle management?

### PAI Indicators
```bash
# Check for checkpoint/session handling
grep -r "checkpoint\|resume\|session" "$PAI_PATH" --include="*.md" --include="*.json"
```

### Optimization Signals
- No checkpoints → Enable CC checkpoint feature
- Manual resume → Use /resume command
- Lost context → Implement session persistence

---

## Factor 7: Contact Humans with Tool Calls

### Audit Questions
- [ ] Can the agent request human input when needed?
- [ ] Are human-in-the-loop points clearly defined?
- [ ] Is there approval workflow for sensitive actions?

### PAI Indicators
```bash
# Check for human contact mechanisms
grep -r "human\|approval\|confirm\|ask" "$PAI_PATH/.claude" --include="*.md"
```

### Optimization Signals
- No human contact → Add confirmation prompts
- Implicit approval → Make explicit with tools
- Missing escalation → Define escalation paths

---

## Factor 8: Own Your Control Flow

### Audit Questions
- [ ] Is the agent loop in application code (not framework)?
- [ ] Can control flow be customized per-task?
- [ ] Are decision points explicit and logged?

### PAI Indicators
```bash
# Check for custom control flow
grep -r "loop\|step\|workflow" "$PAI_PATH/.claude/commands" --include="*.md"
```

### Optimization Signals
- Framework-controlled → Extract to custom code
- Implicit flow → Document in commands/
- No logging → Add decision logging

---

## Factor 9: Compact Errors into Context Window

### Audit Questions
- [ ] Are errors summarized before adding to context?
- [ ] Is there error deduplication?
- [ ] Do errors include actionable information?

### PAI Indicators
```bash
# Check for error handling patterns
grep -r "error\|catch\|fail" "$PAI_PATH/.claude" --include="*.md"
```

### Optimization Signals
- Verbose errors → Implement summarization
- Repeated errors → Add deduplication
- Opaque errors → Include resolution hints

---

## Factor 10: Small, Focused Agents

### Audit Questions
- [ ] Is each agent single-purpose?
- [ ] Are agents <500 lines of configuration?
- [ ] Can agents be composed for complex tasks?

### PAI Indicators
```bash
# Check agent sizes and count
ls -la "$PAI_PATH/.claude/agents/" 2>/dev/null
wc -l "$PAI_PATH/.claude/agents/"*.md 2>/dev/null
```

### Optimization Signals
- Monolithic agent → Split by domain
- Overlapping agents → Clarify boundaries
- No composition → Add orchestration layer

---

## Factor 11: Trigger from Anywhere

### Audit Questions
- [ ] Can the agent be triggered via CLI?
- [ ] Can the agent be triggered via API/webhook?
- [ ] Can the agent be triggered from other agents?

### PAI Indicators
```bash
# Check for trigger mechanisms
grep -r "trigger\|webhook\|cron\|event" "$PAI_PATH" --include="*.md" --include="*.json"
```

### Optimization Signals
- CLI only → Add API endpoints
- No scheduling → Add cron triggers
- Isolated agents → Enable inter-agent calls

---

## Factor 12: Make Your Agent a Stateless Reducer

### Audit Questions
- [ ] Is all state external to the agent?
- [ ] Given same input, does agent produce same output?
- [ ] Can agent be horizontally scaled?

### PAI Indicators
```bash
# Check for state externalization
grep -r "database\|storage\|persist\|file" "$PAI_PATH/.claude" --include="*.md"
```

### Optimization Signals
- Internal state → Externalize to files/DB
- Non-deterministic → Add seed/reproducibility
- Singleton → Design for multiple instances

---

## Compliance Score Calculation

```javascript
// Calculate overall compliance
const factors = [
  { name: 'Natural Language to Tools', weight: 1, score: 0 },
  { name: 'Own Your Prompts', weight: 1, score: 0 },
  { name: 'Own Your Context Window', weight: 2, score: 0 },  // High impact
  { name: 'Tools Are Structured Outputs', weight: 1, score: 0 },
  { name: 'Unify Execution State', weight: 1, score: 0 },
  { name: 'Launch/Pause/Resume', weight: 1, score: 0 },
  { name: 'Contact Humans with Tools', weight: 1, score: 0 },
  { name: 'Own Your Control Flow', weight: 2, score: 0 },   // High impact
  { name: 'Compact Errors', weight: 1, score: 0 },
  { name: 'Small Focused Agents', weight: 2, score: 0 },    // High impact
  { name: 'Trigger from Anywhere', weight: 1, score: 0 },
  { name: 'Stateless Reducer', weight: 1, score: 0 }
];

// Score: 0 = Not implemented, 1 = Partial, 2 = Full compliance
// Weighted total / (2 * total weight) * 100 = percentage
```