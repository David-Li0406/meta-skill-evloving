---
title: "Synthesis: Improvements for Agent Orchestration Skill"
description: "Analysis of orchestration patterns from multiple sources to identify improvements for agent-orchestration SKILL.md"
date: 2025-11-14
sources:
  - "https://anyblockers.com/posts/working-with-coding-agents"
  - "~/.claude/commands/how-to-delegate.md"
  - "~/repos/claude_skills/commands/orchestration-best-practicing.md"
  - "~/.claude/commands/am-i-complete.md"
  - "~/repos/claude_skills/.claude/commands/is-it-done.md"
  - "~/repos/claude_skills/story-based-framing/SKILL.md"
  - "~/repos/claude_skills/python3-development/references/python-development-orchestration.md"
  - "~/repos/claude_skills/research_skills_process.md"
  - "https://claudefa.st"
  - "https://claudefa.st/docs/orchestrating-agents"
---

# Synthesis: Improvements for Agent Orchestration Skill

## Purpose

This document synthesizes orchestration patterns from multiple sources to identify improvements for the agent-orchestration SKILL.md. It will serve as input for a multi-agent analysis experiment where different specialized agents (claude-context-optimizer, subagent-generator, subagent-refactorer, python-cli-architect) will critically analyze using ultrathink and sequential-thinking MCP how they would integrate and revise the agent-orchestration/SKILL.md.

## Current State Analysis

### What agent-orchestration/SKILL.md Currently Has

**Strengths:**

- Clear scientific delegation framework (observations + success criteria - assumptions - prescriptions)
- Comprehensive delegation template with XML structure
- Detailed inclusion/exclusion rules for what to provide agents
- Pre-delegation verification checklist
- Conditional delegation logic for different scenarios
- Anti-patterns section
- Specialized agent assignment rules
- File path reference patterns using @filepath syntax

**Identified Gaps:**

- No explicit self-verification protocol for orchestrator's own work
- No model selection guidance (when to use haiku vs sonnet)
- Limited guidance on parallel delegation (how many agents, scope isolation)
- No formalized root cause vs symptom detection framework
- Missing quality acceptance criteria checklist
- No universal "Definition of Done" applicable to all delegations
- Could benefit from story-based framing for anti-patterns
- No decision trees for common orchestration scenarios

## Patterns from External Sources

### 1. From anyblockers.com Article

**Key Concepts:**

- **Onboarding metaphor**: Treat agents like senior engineers joining the team
- **Formalized recurring rules**: Codify patterns that emerge across tasks
- **Model selection trade-offs**: Speed (haiku) vs intelligence (sonnet)
- **Parallel agents**: Run 1-3 agents concurrently with non-overlapping scope
- **Self-verification**: Agents validate their own work before reporting
- **Context management**: Keep prompts focused, use progressive disclosure

**Impact on SKILL.md:**

- Add "Onboarding Metaphor" section to delegation template
- Add "Model Selection Guidance" for orchestrator decisions
- Add "Parallel Delegation Strategy" with scope isolation rules
- Strengthen self-verification requirements in delegation template

### 2. From how-to-delegate.md (Slash Command)

**Key Concepts:**

- XML-tagged sections for deterministic parsing
- Clear separation of observations, success criteria, context, task
- Emphasis on "Your ROLE_TYPE is sub-agent" as first line
- Verification questions for orchestrator before delegating
- Conditional delegation logic based on scenario type
- Final verification checklist with forbidden phrases

**Impact on SKILL.md:**

- Already well-integrated - SKILL.md uses XML tags extensively
- Could add more explicit "ROLE_TYPE declaration" emphasis
- Could expand verification questions section
- Template structure is already strong

### 3. From orchestration-best-practicing.md

**Key Concepts:**

- Root Cause Analysis First (never accept surface-level descriptions)
- Context Management (treat agents like new engineers)
- Strategic Decomposition (UNDERSTAND → ANALYZE → REASON → SYNTHESIZE → CONCLUDE)
- Quality Assurance Checklist before accepting work
- Anti-patterns to prevent (symptom patching, context overload, micromanagement)
- Escalation criteria (when to involve user)
- Technology-specific adaptations

**Impact on SKILL.md:**

- Add "Root Cause Analysis Protocol" section
- Add "Quality Acceptance Criteria" checklist for orchestrator
- Expand anti-patterns with specific detection criteria
- Add "Escalation Criteria" section
- Consider technology-specific guidance in references/

### 4. From am-i-complete.md and is-it-done.md

**Key Concepts:**

- Systematic verification protocol before marking tasks complete
- Check original request against current state
- Identify missed expected steps (planning, research, validation)
- Verify real-world functionality, not just isolated tests
- Confirm no regressions introduced
- Ensure documentation updated

**Impact on SKILL.md:**

- Add "Orchestrator Self-Verification Protocol"
- Add requirement to use mcp\_\_sequential_thinking before task completion
- Add "Definition of Done" checklist applicable to all delegations
- Strengthen verification requirements in delegation template

### 5. From story-based-framing/SKILL.md

**Key Concepts:**

- Four-act narrative structure (Promise → Betrayal → Consequences → Source)
- Achieves 70% faster pattern identification compared to checklists
- Effective for describing anti-patterns for LLM detection
- Works across any domain (code analysis, business processes, security)

**Impact on SKILL.md:**

- Reframe anti-patterns section using story-based structure
- Add narrative examples for common orchestration failures
- Use Promise/Betrayal/Consequences/Source for anti-pattern descriptions

### 6. From python-development-orchestration.md

**Key Concepts:**

- Specific guidance for Python CLI orchestration workflows
- Modern Python 3.11+ patterns and tooling
- Test-driven development orchestration
- Linting and quality control integration
- Pre-commit hook integration patterns

**Impact on SKILL.md:**

- Consider creating domain-specific orchestration guides in references/
- Add references to technology-specific patterns
- Link to python-development-orchestration.md for Python tasks

### 7. From research_skills_process.md

**Key Concepts:**

- Parallel research pattern with concurrent agents
- Each researcher has specific focus area
- Consolidator synthesizes findings
- Built-in quality checks and cross-verification

**Impact on SKILL.md:**

- Add "Parallel Research Pattern" as orchestration example
- Show concrete multi-agent coordination workflow
- Demonstrate scope isolation and synthesis pattern

### 8. From claudefa.st Documentation

**Key Concepts:**

- Progressive disclosure: Keep SKILL.md lean (~5k words), detailed docs in references/
- Clear trigger descriptions in frontmatter
- Actionable, deterministic instructions
- Verification requirements before completion
- Context window optimization through delegation

**Impact on SKILL.md:**

- Already well-structured for progressive disclosure
- Could move some detailed sections to references/
- Frontmatter description could be more trigger-focused
- Overall structure is sound

## Synthesis of Missing Elements

### 1. Self-Verification Protocol (High Priority)

**What's Missing:** Orchestrator needs explicit self-verification before task completion, similar to what agents are required to do.

**Proposed Addition:**

```markdown
## Orchestrator Self-Verification Protocol

Before marking any task as complete, the orchestrator must:

1. Use mcp**sequential_thinking**sequentialthinking tool to review:
   - Original user request vs current task state
   - Whether all expected steps were completed (planning, research, validation)
   - Whether any requirements were missed or misunderstood

2. Verify deliverables:
   - All code changes compile/run without warnings
   - All tests pass (existing and new)
   - Documentation updated to reflect changes
   - No regressions introduced in related functionality

3. Check delegation quality:
   - Did agents receive clear success criteria?
   - Were observations factual (no assumptions)?
   - Was agent autonomy preserved (no HOW prescriptions)?
   - Did agents complete verification before reporting?

4. Validate real-world functionality:
   - Not just isolated unit tests
   - Actual end-to-end workflow tested
   - Edge cases considered
   - Error handling verified

Only after completing this protocol may the orchestrator report task completion to the user.
```

### 2. Model Selection Guidance (High Priority)

**What's Missing:** When to delegate to haiku (fast) vs sonnet (intelligent) sub-agents.

**Proposed Addition:**

```markdown
## Model Selection Guidance

The orchestrator must select appropriate model for each sub-agent based on task characteristics:

**Use Haiku for:**

- Well-defined tasks with clear examples in codebase
- Straightforward file edits or simple code generation
- Tasks where speed maintains user flow state
- Repetitive tasks following established patterns
- Quick verifications or simple validations

**Use Sonnet for:**

- Complex problem-solving requiring analysis
- Architectural decisions or design work
- Tasks touching multiple interconnected components
- Situations requiring creative solutions
- Root cause investigation
- First-time implementation of new patterns

**Trade-off Analysis:**

- Haiku: ~2-5 seconds response time, maintains user flow state, best for "keep typing" scenarios
- Sonnet: ~10-30 seconds response time, handles complexity better, best for "I need to think" scenarios

**Default:** When uncertain, use Sonnet. The cost of re-doing work from Haiku failure exceeds Sonnet cost.
```

### 3. Parallel Delegation Patterns (High Priority)

**What's Missing:** Concrete guidance on running multiple agents concurrently with proper scope isolation.

**Proposed Addition:**

```markdown
## Parallel Delegation Strategy

The orchestrator can run multiple sub-agents concurrently when tasks are independent.

**Scope Isolation Rules:**

- Maximum 1-3 concurrent agents for complex tasks
- Maximum 5 concurrent agents for simple independent tasks
- Each agent must have non-overlapping file/module scope
- Agents must not depend on each other's outputs
- Each agent reports to orchestrator, never to other agents

**Example: Parallel Feature Implementation**

Three agents working simultaneously:

Agent 1 - Core Logic:

- Scope: src/core/processor.py, src/core/utils.py
- Task: Implement data processing algorithm
- Cannot modify: Tests, documentation, API layer

Agent 2 - API Layer:

- Scope: src/api/endpoints.py, src/api/validators.py
- Task: Add new API endpoints
- Cannot modify: Core logic, tests

Agent 3 - Testing:

- Scope: tests/test_processor.py, tests/test_api.py
- Task: Write comprehensive test coverage
- Cannot modify: Implementation files (only tests)

All three agents receive their own Task prompts with clear scope boundaries. Orchestrator waits for all to complete, then reviews integration.

**When NOT to Parallelize:**

- Tasks have sequential dependencies
- Agents need to coordinate on shared state
- Risk of merge conflicts in same files
- User request is for single coherent feature requiring coordination
```

### 4. Root Cause vs Symptom Detection (High Priority)

**What's Missing:** Framework for ensuring agents address root causes, not symptoms.

**Proposed Addition:**

```markdown
## Root Cause Analysis Protocol

The orchestrator must ensure all delegations explicitly require root cause investigation.

**Delegation Template Addition:**

INVESTIGATION REQUIREMENTS:

- Trace the issue through the complete stack before proposing fixes
- Document discoveries at each layer (e.g., UI → Logic → System → Hardware)
- Identify both the symptom AND the root cause
- Explain why addressing [root] instead of patching [symptom]
- Workarounds should not circumvent expected processes
- If proposing workaround, document why root cause cannot be fixed

**Symptom vs Root Cause Examples:**

Symptom: "Add sleep(1) to fix race condition" Root cause: "Fix synchronization logic using proper locks"

Symptom: "Increase timeout to 30 seconds" Root cause: "Optimize database query causing slow response"

Symptom: "Wrap in try/catch to suppress error" Root cause: "Fix validation logic to prevent invalid state"

**Orchestrator Verification:** Before accepting agent work, verify root cause was addressed:

- [ ] Agent identified and documented the root cause
- [ ] Solution addresses root cause, not just symptom
- [ ] If workaround used, justification provided
- [ ] No new technical debt introduced
```

### 5. Quality Acceptance Criteria (Medium Priority)

**What's Missing:** Checklist for orchestrator to verify before accepting agent work.

**Proposed Addition:**

```markdown
## Quality Acceptance Criteria

Before accepting any specialist agent's work, the orchestrator must verify:

**Functional Requirements:**

- [ ] Specific objective from delegation achieved
- [ ] All acceptance criteria met with evidence
- [ ] Success criteria verified (not just claimed)
- [ ] Real-world functionality tested (not just unit tests)

**Code Quality:**

- [ ] Follows project coding standards and conventions
- [ ] No new linting errors or warnings introduced
- [ ] All existing tests still pass
- [ ] New tests added for new functionality
- [ ] Code is readable and maintainable

**Technical Debt:**

- [ ] No workarounds added without justification
- [ ] Solution simplifies or maintains complexity (doesn't add layers)
- [ ] Follows existing patterns found in codebase
- [ ] Root cause addressed, not just symptoms patched

**Documentation:**

- [ ] Code changes documented (comments, docstrings)
- [ ] Architecture docs updated if applicable
- [ ] README updated if user-facing changes
- [ ] Changelog updated with changes

**Platform/Environment:**

- [ ] Resource usage (CPU/memory) acceptable
- [ ] Error conditions properly handled
- [ ] Platform-specific edge cases considered
- [ ] Dependencies properly specified

If any criterion fails, the orchestrator must request iteration with specific feedback.
```

### 6. Universal Definition of Done (Medium Priority)

**What's Missing:** Standard checklist applicable to all delegations regardless of task type.

**Proposed Addition:**

```markdown
## Universal Definition of Done

Every sub-agent delegation must include this standard completion criteria:

DEFINITION OF SUCCESS:

- [Task-specific measurable outcome]
- [Task-specific acceptance criteria]
- [Task-specific verification method]

UNIVERSAL REQUIREMENTS (apply to all tasks):

- [ ] Objective achieved: Solution works in real-world usage (not just mocked tests)
- [ ] Stability: Existing functionality remains intact, no regressions introduced
- [ ] Root cause addressed: Not just symptom patching
- [ ] Quality: Code follows project conventions, no new warnings/errors
- [ ] Testing: Comprehensive tests added, all tests pass
- [ ] Documentation: All references to this functionality updated
- [ ] Verification: Agent performed self-verification and documented results
- [ ] No technical debt: No workarounds unless justified with explanation

Only when ALL criteria are met may the agent report task completion.
```

### 7. Story-Based Framing for Anti-Patterns (Medium Priority)

**What's Missing:** Narrative structure for anti-patterns to achieve 70% faster pattern identification.

**Proposed Addition:**

```markdown
## Anti-Patterns (Story-Based Framing)

Using Promise → Betrayal → Consequences → Source narrative structure for faster pattern detection.

### The Assumption Cascade

**The Promise:** "I'll quickly analyze this error and tell the agent exactly what to fix."

**The Betrayal:** "I think the issue is X, which probably means Y, so likely Z needs fixing." Creates chain of unverified assumptions. Agent receives fabricated diagnosis instead of factual observations.

**The Consequences:**

- Agent implements fix based on wrong diagnosis
- Real root cause remains unaddressed
- Additional iteration required after agent's work fails
- Wasted context window on both orchestrator and agent
- User loses trust in AI reliability

**The Source:** Orchestrator pattern-matched from training data instead of investigating. Tried to save time by guessing instead of observing. Violated "observations only, no assumptions" principle.

### The Prescription Trap

**The Promise:** "I'll save the agent time by telling them exactly how to implement this."

**The Betrayal:** "Fix this by doing A, then B, then C. Use library X with pattern Y." Orchestrator prescribes implementation sequence and technical decisions.

**The Consequences:**

- Agent cannot leverage their specialized expertise
- Misses better solutions agent would have discovered
- Creates dependency on orchestrator making all decisions
- Wastes agent's 200k context window and documentation access
- Solution reflects orchestrator limitations, not agent capabilities

**The Source:** Orchestrator didn't trust agent expertise. Confused "defining WHAT" with "prescribing HOW". Violated agent autonomy principle.

### The Discovery Limiter

**The Promise:** "I'll make this simple for the agent by narrowing their investigation scope."

**The Betrayal:** "Just read these two files and fix the issue." Restricts agent from comprehensive discovery that might reveal root cause.

**The Consequences:**

- Agent fixes symptom instead of root cause
- Misses related issues in other components
- Creates incomplete solution requiring re-work
- Technical debt accumulates from partial fixes

**The Source:** Orchestrator assumed they knew exactly where the problem was. Didn't allow for agent's broader investigation revealing actual root cause. Violated "enable full discovery" principle.

### The Context Withholding

**The Promise:** "I'll keep the prompt concise by filtering what the agent sees."

**The Betrayal:** Orchestrator observes error, investigates related code, finds relevant history, but only passes partial context to agent: "Fix the failing test."

**The Consequences:**

- Agent duplicates discovery work orchestrator already did
- Wastes both orchestrator and agent context windows
- Agent lacks context for understanding broader implications
- Forces agent to make decisions with incomplete information

**The Source:** Orchestrator confused "concise prompts" with "withholding observations". Should pass all observations while omitting orchestrator's interpretations. Violated "you are a context router" principle.

### The Confidence Mask

**The Promise:** "I'll provide clear direction based on my understanding."

**The Betrayal:** "The problem is clearly a race condition in the connection pool." States uncertainty as fact without verification. Agent receives orchestrator's unverified hypothesis as ground truth.

**The Consequences:**

- Agent implements fix based on wrong diagnosis
- Real root cause remains unaddressed
- Propagates errors through agent chain
- Creates false documentation trail
- Rebuilding trust requires additional user interaction

**The Source:** Orchestrator pattern-matched from training data and stated assumption as fact. Didn't distinguish "I observed X" from "I think X". Violated "distinguish facts from assumptions" principle.
```

### 8. Decision Trees (Low Priority)

**What's Missing:** Quick reference flowcharts for common orchestration decisions.

**Proposed Addition:**

```markdown
## Orchestration Decision Trees

### Tree 1: Should I Delegate This Task?

Question: Is this a simple file read or search?

- YES → Use operation-specific tool directly (Read, Grep, Glob)
- NO → Continue

Question: Does this require writing code or making changes?

- YES → Continue
- NO → Continue

Question: Does this require specialized domain knowledge?

- YES → Delegate to appropriate specialist agent
- NO → Continue

Question: Will this pollute orchestrator context with large amounts of data?

- YES → Delegate to context-gathering agent
- NO → Consider doing it directly

### Tree 2: Which Model Should I Use?

Question: Is this a well-defined task with clear examples in codebase?

- YES → Continue
- NO → Use Sonnet

Question: Does this require creative problem-solving or architectural decisions?

- YES → Use Sonnet
- NO → Continue

Question: Is speed critical to maintain user flow state?

- YES → Use Haiku
- NO → Use Sonnet (default)

### Tree 3: Can I Parallelize This Work?

Question: Are there independent sub-tasks with non-overlapping scope?

- NO → Sequential delegation required
- YES → Continue

Question: Do any sub-tasks depend on outputs from others?

- YES → Sequential delegation required
- NO → Continue

Question: Would parallel agents work on same files/modules?

- YES → Sequential delegation required
- NO → Continue

Question: How many independent sub-tasks exist?

- 2-3 → Parallel delegation appropriate
- 4-5 → Parallel delegation for simple tasks only
- 6+ → Consider if this should be broken into phases

### Tree 4: How Much Context Should I Provide?

Question: Is this a focused task (single file, clear test)?

- YES → Minimal context: "Fix [observation] in [file]. Success: [test] passes."
- NO → Continue

Question: Is this an investigative task (unknown cause)?

- YES → Maximum context: All observations, error traces, system state
- NO → Continue

Question: Is this an architectural task (multi-component)?

- YES → Full context: Project structure, all findings, historical context
- NO → Provide moderate context: File paths, scope boundaries, user requirements
```

## Conclusion

This synthesis identifies 8 key improvement areas for agent-orchestration/SKILL.md, prioritized by impact:

**High Priority (Immediate Integration):**

1. Self-Verification Protocol - Ensures orchestrator validates own work before completion
2. Model Selection Guidance - Optimizes speed vs intelligence trade-offs
3. Parallel Delegation Patterns - Enables efficient multi-agent coordination
4. Root Cause Analysis Protocol - Prevents symptom patching

**Medium Priority (Strong Value-Add):** 5. Quality Acceptance Criteria - Standardizes what orchestrator verifies 6. Universal Definition of Done - Ensures consistent completion standards 7. Story-Based Anti-Patterns - Achieves 70% faster pattern identification

**Low Priority (Nice-to-Have):** 8. Decision Trees - Quick reference for common orchestration decisions

The current SKILL.md has a strong foundation with scientific delegation framework, comprehensive template structure, and clear inclusion/exclusion rules. These additions would strengthen the skill by:

- Adding explicit orchestrator self-verification (currently only agents verify)
- Providing concrete guidance for model selection and parallel delegation
- Standardizing quality and completion criteria
- Using story-based framing for faster anti-pattern detection
- Adding decision support for common orchestration scenarios

**Next Steps:** This synthesis will be provided to four specialized agents (claude-context-optimizer, subagent-generator, subagent-refactorer, python-cli-architect) who will critically analyze using ultrathink and sequential-thinking MCP how they would integrate and revise the agent-orchestration/SKILL.md based on these findings.
