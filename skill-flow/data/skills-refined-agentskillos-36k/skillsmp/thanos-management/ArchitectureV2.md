# Thanos Architecture V2 - Improvement Design

## Current State Analysis

### What Exists
```
~/.claude/
├── State/           # 5 files: Today, CurrentFocus, Commitments, ThisWeek, WaitingFor
├── Skills/          # 8 domain skills + Operator, SleepArchitecture
├── Memory/          # ChromaDB config (unused), retrieval.ts (not connected)
├── Agents/          # 5 agents: Ops, Coach, Health, Strategy, AgentFactory
├── History/         # Structure exists, empty subdirs
├── Inbox/           # Empty - not being used
├── Context/         # Clients, People, CORE.md
└── Config files     # CLAUDE.md, THANOS.md, etc.
```

### Critical Gaps

1. **No Auto-Persistence**: State files require manual updates
2. **No Session Logging**: Conversations not captured to History/Sessions
3. **No Commitment Extraction**: Should auto-pull from conversations
4. **Agent Routing Broken**: Agents defined but never auto-triggered
5. **Memory Not Connected**: Vector DB configured but not queried
6. **No Daily Automation**: Should auto-generate morning brief
7. **No Time Awareness**: Can't proactively remind (fixed with time query)
8. **Cross-Session Context Loss**: Each session starts fresh

---

## V2 Architecture Design

### 1. Session Lifecycle Hooks

**On Session Start:**
```
1. Query system time
2. Read State/Today.md - what's planned?
3. Read State/Commitments.md - what's due?
4. Query Memory/ for recent patterns
5. Check Inbox/ for unprocessed items
6. Generate proactive briefing
```

**On Session End (or /close command):**
```
1. Extract commitments made during session
2. Update State/ files with new info
3. Log session summary to History/Sessions/YYYY-MM-DD-HH.md
4. Store key exchanges in Memory/vectors
5. Update commitment status
```

**Mid-Session Triggers:**
```
- Commitment detected → auto-add to Commitments.md
- Decision made → log to History/Decisions/
- Client mentioned → update Context/Clients/
- Pattern detected → store in Memory/
```

### 2. Memory Integration

**Claude Flow Memory (Active - SQLite)**
- Use `memory_usage` for quick state storage
- Use `memory_search` for pattern retrieval
- Namespaces: `daily-logs`, `commitments`, `patterns`, `sessions`

**Vector Memory (Future - ChromaDB)**
- Semantic search across all conversations
- Pattern detection across time
- "What did I decide about X?" queries

**Implementation Priority:**
1. ✅ Claude Flow memory (already working)
2. 🔄 Session logging to History/
3. 🔄 Auto-commit extraction
4. ⏳ Vector embedding pipeline

### 3. Agent Auto-Routing

**Current Problem:** Agents exist but require manual invocation

**Solution - Trigger Detection in OPERATOR:**

```yaml
routing_rules:
  overwhelm_detected:
    triggers: ["overwhelmed", "too much", "can't focus", "scattered"]
    action: Activate Ops agent protocol

  health_concern:
    triggers: ["tired", "energy", "sleep", "vyvanse", "crash"]
    action: Activate Health agent protocol

  client_context:
    triggers: ["Memphis", "Raleigh", "Orlando", "Nova", "Baptist", "ScottCare"]
    action: Load Context/Clients/{client}.md, activate Epic skill

  family_context:
    triggers: ["Ashley", "Sullivan", "family"]
    action: Load Context/People/, activate Family skill

  accountability_needed:
    triggers: ["I should", "I need to", "I committed", "I promised"]
    action: Activate Coach agent, extract commitment
```

### 4. State File Auto-Updates

**Today.md - Auto-populated fields:**
```markdown
# Today - {auto: YYYY-MM-DD}

## Morning Brief
- Energy: {ask once, persist}
- Sleep: {from previous night log}
- Vyvanse: {ask or track}

## Commitments Due Today
{auto: filter from Commitments.md where deadline = today}

## Carried Over
{auto: incomplete items from yesterday's Today.md}

## Session Log
{auto: append summary of each session}
```

**Commitments.md - Auto-extraction:**
```
Trigger phrases:
- "I'll have that done by..."
- "I committed to..."
- "Tell [person] I'll..."
- "By [time/date] I need to..."

Action: Parse → Create commitment entry → Confirm with user
```

### 5. Proactive Behaviors

**Morning (on first session of day):**
```
1. "Good morning. It's {time}. Here's your day:"
2. Show commitments due today
3. Show top 3 priorities from CurrentFocus
4. Ask for energy level
5. Recommend first action
```

**Evening (after 8 PM or /evening command):**
```
1. Review what got done today
2. Surface any incomplete commitments
3. Capture tomorrow's top 3
4. Trigger evening lockdown protocol
```

**Pattern Alerts:**
```
- "You've mentioned being tired 3 days in a row. Sleep review needed?"
- "You committed to X 5 days ago, no update. Status?"
- "This is the third time you've avoided Y topic."
```

### 6. Inbox Processing Flow

**Capture → Process → Route**

```
Inbox item types:
- task → Commitments.md (with deadline)
- reference → Context/{appropriate folder}
- idea → History/Learnings/ or Memory/
- question → Answer immediately or WaitingFor.md
- commitment_to_me → WaitingFor.md
```

**Auto-capture sources:**
- Email summaries (via GSuite MCP)
- Voice notes transcription
- Quick captures during conversation

### 7. History Logging Structure

```
History/
├── Sessions/
│   └── 2026-01-05-2143.md    # Session summary
├── DailyLogs/
│   └── 2026-01-05.md          # Full day summary
├── Commitments/
│   └── 2026-01-05-commit.md   # Commitments made this day
├── Decisions/
│   └── decision-name.md       # Decision + reasoning
├── Learnings/
│   └── insight-topic.md       # Insights and learnings
└── Inbox/
    └── processed-item.md      # Archived inbox items
```

---

## Implementation Phases

### Phase 1: Foundation (This Week)
- [x] Time awareness at session start
- [x] OPERATOR integration
- [x] Sleep architecture
- [ ] Session end logging
- [ ] Commitment auto-extraction
- [ ] Morning brief automation

### Phase 2: Memory (Next Week)
- [ ] Claude Flow memory for daily state
- [ ] Session summaries to History/
- [ ] Pattern storage and retrieval
- [ ] Cross-session context preservation

### Phase 3: Automation (Week 3)
- [ ] Agent auto-routing
- [ ] Inbox processing workflow
- [ ] Proactive pattern alerts
- [ ] Daily/weekly review automation

### Phase 4: Intelligence (Week 4+)
- [ ] Vector embedding pipeline
- [ ] Semantic search across history
- [ ] Predictive suggestions
- [ ] Behavioral pattern analysis

---

## Quick Wins Available Now

1. **Session Logging**: On `/close` or end of conversation, write summary to History/Sessions/
2. **Commitment Detection**: When phrases like "I'll do X by Y" detected, confirm and add to Commitments.md
3. **Morning Query**: First message of day triggers State/ review
4. **Memory Store**: Use Claude Flow `memory_usage` to persist important context

---

## Integration Points

**Thanos Mode:**
- All improvements active by default
- Silent operations, no permission prompts
- OPERATOR voice for all interactions

**Claude Flow:**
- Swarm for complex analysis (like this task)
- Memory tools for persistence
- Task orchestration for multi-step workflows

**Skills:**
- Auto-load based on context detection
- Combine with agent protocols
- Route to appropriate domain

---

*Architecture designed: 2026-01-05 21:52 EST*
*Status: Phase 1 in progress*
