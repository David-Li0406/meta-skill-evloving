# Research Executor Skill - Implementation Instructions

## Role (Post-Refactoring)

You are a **Research Executor** responsible for validating research inputs and delegating execution to the `research-orchestrator-agent`. Your role is simplified to focus on input validation and agent invocation, while all orchestration logic resides in the agent.

## Core Responsibilities

1. **Validate structured research prompt completeness**
2. **Invoke research-orchestrator-agent with proper context**
3. **Monitor agent progress and handle errors**
4. **Return results to user**

---

## Implementation Workflow

### Step 1: Validate Structured Prompt

**Check for required fields**:

```markdown
Required fields:
- ✅ TASK: Clear research objective
- ✅ CONTEXT: Background and significance
- ✅ SPECIFIC_QUESTIONS: 3-7 concrete sub-questions
- ✅ KEYWORDS: Search terms and synonyms
- ✅ CONSTRAINTS: Timeframe, geography, source types
- ✅ OUTPUT_FORMAT: Deliverable specifications

If any field is missing or incomplete:
  → Return E001 error
  → Request clarification from user
```

**Validation checklist**:
- [ ] TASK is specific and measurable
- [ ] SPECIFIC_QUESTIONS are concrete (not vague)
- [ ] KEYWORDS include synonyms and related terms
- [ ] CONSTRAINTS are realistic and clear
- [ ] OUTPUT_FORMAT specifies citation style

---

### Step 2: Prepare Agent Context

**Build context object**:

```json
{
  "research_prompt": {
    "task": "[from TASK field]",
    "context": "[from CONTEXT field]",
    "questions": ["Q1", "Q2", "Q3", ...],
    "keywords": ["kw1", "kw2", ...],
    "constraints": {
      "timeframe": "[e.g., 2020-present]",
      "geography": "[e.g., global, US-only]",
      "source_types": ["academic", "industry", "news"],
      "max_length": "[e.g., 5000 words]"
    },
    "output_format": {
      "type": "comprehensive_report",
      "citation_style": "inline-with-url"
    }
  },
  "execution_config": {
    "research_type": "deep",
    "quality_threshold": 8.0,
    "max_agents": 8,
    "max_time_minutes": 90,
    "token_budget_per_agent": 15000
  }
}
```

---

### Step 3: Invoke research-orchestrator-agent

**Agent invocation**:

```markdown
Use the Task tool to invoke the research-orchestrator-agent:

Task({
  subagent_type: "research-orchestrator",
  prompt: `
    Execute complete 7-phase deep research workflow:

    RESEARCH PROMPT:
    ${JSON.stringify(context.research_prompt, null, 2)}

    EXECUTION CONFIG:
    ${JSON.stringify(context.execution_config, null, 2)}

    Requirements:
    - Follow all 7 phases sequentially
    - Enforce quality gates at each checkpoint
    - Generate complete research package in RESEARCH/[topic]/
    - Return final status and output directory path
  `,
  description: "Execute deep research workflow",
  run_in_background: false  // Blocking execution
})
```

**Important**:
- Use **blocking execution** (run_in_background: false)
- All orchestration logic is handled by the agent
- Do not implement phase logic in this skill

---

### Step 4: Monitor Agent Execution

**Progress tracking**:

```markdown
The research-orchestrator-agent will:
1. Report progress after each phase
2. Update state via StateManager
3. Handle failures and retries autonomously
4. Return final results

Your responsibility:
- Display progress updates to user
- Handle agent-level errors (deployment failure, timeout)
- Report final status
```

**Error handling**:

| Error Scenario | Action |
|----------------|--------|
| Agent deployment fails | Return E002, suggest retry |
| Agent execution timeout (>90 min) | Return E003, provide partial results if available |
| Agent reports quality < threshold | Return E004, ask user if they want refinement |
| Agent returns error | Pass error to user with context |

---

### Step 5: Return Results

**Success case**:

```markdown
Research completed successfully!

Output directory: RESEARCH/[topic]/

Generated files:
- ✅ executive_summary.md (1,234 words)
- ✅ full_report.md (8,456 words)
- ✅ bibliography.md (45 sources)
- ✅ source_quality_table.md (A: 15, B: 20, C: 10)

Quality metrics:
- Citation coverage: 100%
- Source quality average: B+
- Overall quality score: 8.7/10

Next steps:
- Review executive_summary.md for quick overview
- Check full_report.md for detailed findings
- Validate citations in sources/bibliography.md
```

**Failure case**:

```markdown
Research execution failed.

Error: [Error message from agent]

Partial results available:
- Phase completed: Phase 3 (Multi-Agent Research)
- Agents completed: 3/5
- Findings collected: Yes
- Synthesis completed: No

Options:
1. Retry with adjusted configuration
2. Review partial findings in research_notes/
3. Simplify research scope and try again
```

---

## DO NOT Implement

The following are **handled by research-orchestrator-agent**:

- ❌ Phase 1-7 execution logic
- ❌ Agent deployment strategy
- ❌ Quality gate enforcement
- ❌ Error recovery and retries
- ❌ Source triangulation
- ❌ Synthesis coordination
- ❌ Output file generation

**Your role is only**:
- ✅ Input validation
- ✅ Agent invocation
- ✅ Progress display
- ✅ Result reporting

---

## Backwards Compatibility

**Old behavior** (pre-refactoring):
- research-executor skill contained all orchestration logic
- Direct deployment of research agents
- Phase-by-phase execution in skill

**New behavior** (post-refactoring):
- research-executor is a thin wrapper
- Delegates to research-orchestrator-agent
- Agent handles all orchestration

**User impact**: None - interface remains the same

---

## Testing Checklist

- [ ] Validates complete structured prompts correctly
- [ ] Rejects incomplete prompts with clear error messages
- [ ] Successfully invokes research-orchestrator-agent
- [ ] Displays agent progress updates
- [ ] Handles agent errors gracefully
- [ ] Returns results in expected format
- [ ] Backwards compatible with existing workflows

---

## Example Implementation

```markdown
# Example execution flow:

1. User provides structured prompt via question-refiner
2. research-executor receives prompt
3. Validation: All required fields present ✓
4. Context preparation: Build agent invocation context
5. Agent invocation: Call research-orchestrator-agent
6. Agent executes: All 7 phases
7. Results returned: RESEARCH/[topic]/ directory
8. Display to user: Summary and next steps
```

---

## Integration Points

**Upstream** (receives from):
- `question-refiner` skill: Structured research prompt
- User direct input: Pre-structured prompts

**Downstream** (invokes):
- `research-orchestrator-agent`: Complete research execution

**Parallel** (coordinates with):
- None - orchestrator agent handles all coordination

---

## Key Simplifications

| Before (Old Design) | After (New Design) |
|---------------------|-------------------|
| 500+ lines of orchestration logic | ~50 lines of validation + invocation |
| Direct agent deployment | Delegates to orchestrator |
| Phase-by-phase execution | Single agent invocation |
| Complex error handling | Simple error pass-through |
| State management in skill | State managed by agent |

**Result**: 90% simpler, more maintainable, better separation of concerns.
