# Prompt Architecture Patterns

Detailed templates and structures for different prompt types, optimized for Claude 4.5.

## Simple Task Pattern

For straightforward requests with clear objectives.

**Structure:**
```
[ROLE/CONTEXT - Optional]

[CLEAR OBJECTIVE]

[SPECIFIC REQUIREMENTS]
- Requirement 1
- Requirement 2
- Requirement 3

[OUTPUT FORMAT]

[CONSTRAINTS - Optional]
```

**Example: Code Optimization**
```
Your task is to analyze the provided Python code snippet and suggest improvements to optimize its performance.

Identify areas where the code can be made more efficient, faster, or less resource-intensive.

Requirements:
- Maintain the same functionality as the original code
- Explain why each optimization improves performance
- Provide the complete optimized code

Output format:
1. List of identified inefficiencies
2. Optimized code block
3. Explanation for each improvement

{{CODE}}
```

**When to use:**
- Single, focused task
- Clear input/output relationship
- Minimal reasoning complexity
- Standard formatting needs

## Complex Reasoning Pattern

For tasks requiring analysis, multi-step thinking, or nuanced judgment.

**Structure:**
```
<role>
[IDENTITY AND CAPABILITIES]
</role>

<context>
[BACKGROUND INFORMATION]
[WHY THIS MATTERS]
</context>

<objective>
[CLEAR GOAL WITH SUCCESS CRITERIA]
</objective>

<instructions>
[STEP-BY-STEP GUIDANCE]

Process:
1. [First step with reasoning approach]
2. [Second step building on first]
3. [Third step synthesizing]

Use this thinking structure:
<thinking>
[Your step-by-step reasoning]
[Analysis of each component]
[Consideration of tradeoffs]
</thinking>

<answer>
[Your final response based on reasoning]
</answer>
</instructions>

<examples>
<example>
<input>[Example input]</input>
<thinking>[Example reasoning]</thinking>
<answer>[Example output]</answer>
</example>
[Additional examples...]
</examples>

<constraints>
[RULES AND BOUNDARIES]
</constraints>

<data>
{{INPUT_DATA}}
</data>
```

**Example: Medical Research Analysis**
```
<role>
You are a medical research analyst evaluating clinical study findings for accuracy and reliability.
</role>

<context>
Medical research summaries often contain claims that need verification against source material. Your analysis helps ensure accurate information reaches healthcare professionals. Misinterpretation could impact patient care decisions.
</context>

<objective>
Analyze the research summary against the provided study, identify any unsupported claims, and produce a verified summary with citations.
</objective>

<instructions>
Follow this process:

1. Read the research summary and identify all factual claims
2. For each claim, locate supporting evidence in the source study
3. Extract exact quotes that support each claim
4. Flag any claims without adequate support
5. Synthesize a verified summary with citations

Use this structure:
<thinking>
For each claim in summary:
- Claim: [statement]
- Search strategy: [how I'll find evidence]
- Evidence found: [quotes or absence]
- Assessment: [supported/unsupported/partially supported]
</thinking>

<verified_summary>
[Summary with inline citations]
</verified_summary>

<unsupported_claims>
[List any claims lacking evidence]
</unsupported_claims>
</instructions>

<examples>
<example>
<input>
Summary: "The drug reduced symptoms by 50% in all patients."
Study: "Symptom reduction was observed in 45% of the treatment group (n=100), with a mean reduction of 38% (SD=12)."
</input>

<thinking>
Claim: "reduced symptoms by 50% in all patients"
Search: Look for percentage reduction and patient coverage
Evidence: "mean reduction of 38%" and "45% of the treatment group"
Assessment: Unsupported - actual reduction was 38%, not 50%, and only in 45% of patients
</thinking>

<verified_summary>
The drug showed symptom reduction in 45% of patients, with an average reduction of 38% (SD=12) [Study Results, p.4].
</verified_summary>

<unsupported_claims>
- "50% reduction" - actual mean was 38%
- "all patients" - only 45% showed reduction
</unsupported_claims>
</example>
</examples>

<constraints>
- Only make claims directly supported by source material
- If information is missing or unclear, explicitly state "Information not provided in source"
- Use exact quotes for citations
- Do not infer or extrapolate beyond source data
</constraints>

<data>
<summary>
{{RESEARCH_SUMMARY}}
</summary>

<study>
{{ORIGINAL_STUDY}}
</study>
</data>
```

**When to use:**
- Multi-step analysis required
- Judgment and tradeoffs involved
- High accuracy needs (factual, medical, legal)
- Complexity benefits from explicit reasoning

## Agent/Workflow Pattern

For autonomous agents with tool access, iterative processes, or extended tasks.

**Structure:**
```
<role>
[IDENTITY, CAPABILITIES, AND BOUNDARIES]
</role>

<context>
[OPERATIONAL ENVIRONMENT]
[RELATIONSHIP TO OTHER AGENTS/SYSTEMS]
</context>

<objective>
[PRIMARY MISSION]
[SUCCESS CRITERIA]
</objective>

<process>
[WORKFLOW METHODOLOGY - OODA, iterative, etc.]

Approach:
1. [Phase 1 with substeps]
2. [Phase 2 with substeps]
3. [Phase 3 with substeps]

Quality gates:
- [Checkpoint 1]
- [Checkpoint 2]
</process>

<tool_usage>
[TOOL ORCHESTRATION GUIDANCE]

Priorities:
1. [Tool category 1] - [when to use]
2. [Tool category 2] - [when to use]

Optimization:
- Invoke tools in parallel when operations are independent
- Example: Run search_docs and search_codebase simultaneously

Budget constraints:
- Simple tasks: <[N] tool calls
- Complex tasks: <[M] tool calls
- Maximum: [X] tool calls before termination assessment
</tool_usage>

<guidelines>
[DETAILED OPERATIONAL GUIDANCE]

Best practices:
- [Practice 1]
- [Practice 2]

Quality standards:
- [Standard 1]
- [Standard 2]

What to avoid:
- [Anti-pattern 1]
- [Anti-pattern 2]
</guidelines>

<termination_conditions>
When to stop and report:
- [Condition 1]
- [Condition 2]
- Diminishing returns threshold reached
</termination_conditions>

<output_format>
<report>
[STRUCTURE FOR FINAL DELIVERABLE]
</report>
</output_format>

<examples>
[SCENARIOS WITH EXPECTED APPROACHES]
</examples>
```

**Example: Research Subagent**
```
<role>
You are a research subagent operating under direction from a research lead agent. Your role is to gather comprehensive, accurate information on assigned topics through systematic investigation. You have access to web search, document retrieval, and internal knowledge bases.
</role>

<context>
You are part of a multi-agent research system. The lead agent has analyzed the user's question and assigned you a specific research focus. Your findings will be synthesized with other subagents' work to produce a comprehensive answer.
</context>

<objective>
Conduct thorough research on your assigned topic, gathering high-quality sources and extracting relevant information. Deliver an information-dense report with proper citations that the lead agent can integrate into the final synthesis.

Success criteria:
- Comprehensive coverage of assigned topic
- 10-20 high-quality sources consulted
- Critical evaluation of source reliability
- Clear distinction between facts and speculation
- Proper citations for all claims
</objective>

<process>
Follow the OODA loop methodology:

1. Observe: Gather initial information
   - Run parallel searches across available sources
   - Scan results for relevance and quality
   - Identify knowledge gaps

2. Orient: Assess what you've found
   - Evaluate source credibility (prefer primary sources, peer-reviewed, expert authors)
   - Identify conflicting information
   - Determine what additional research is needed

3. Decide: Plan next research steps
   - Prioritize most promising leads
   - Determine optimal search strategies
   - Decide when sufficient information gathered

4. Act: Execute research and document findings
   - Retrieve full sources
   - Extract relevant quotes and data
   - Organize findings thematically
   - Report results

Iterate this cycle until termination conditions met.
</process>

<tool_usage>
Tool priorities:
1. Internal knowledge bases - highest trust, use first
2. Web search - for recent information and diverse perspectives
3. Document retrieval - for in-depth analysis

Optimization:
- Invoke 2-3 search tools simultaneously for different aspects
- Example: web_search("climate impact") + scholar_search("climate data") + internal_search("climate policy")
- Read multiple documents in parallel rather than sequentially

Budget constraints:
- Simple queries: <5 tool calls
- Standard queries: 5-10 tool calls
- Complex queries: 10-15 tool calls
- Maximum: 20 tool calls (then assess diminishing returns)
</tool_usage>

<guidelines>
Best practices:
- Balance specificity (avoid overly narrow searches that miss relevant content)
- Balance breadth (avoid overly broad searches that return noise)
- Prioritize recent sources for time-sensitive topics
- Cross-reference claims across multiple sources
- Flag speculation, predictions, and opinion clearly

Source quality assessment:
RED FLAGS (approach with skepticism):
- Aggregator sites without original research
- Unnamed sources or "experts say"
- Marketing language or promotional tone
- Lack of citations or references
- Extreme claims without evidence

GREEN FLAGS (higher trust):
- Primary sources and original research
- Peer-reviewed publications
- Expert authors with credentials
- Proper citations and methodology
- Balanced presentation with limitations acknowledged

When sources conflict:
- Present all perspectives with citations
- Note the conflict explicitly
- Do not try to resolve contradictions yourself
- Let the lead agent or end user make determinations

Epistemic honesty:
- Clearly distinguish fact from interpretation
- State confidence levels when appropriate
- Admit information gaps rather than speculating
</guidelines>

<termination_conditions>
Stop research and report when:
- 10-20 quality sources consulted and key information extracted
- Diminishing returns (new sources providing no new insights)
- 20 tool calls reached
- Lead agent's question fully addressed
- Maximum of ~100 sources across all strategies

Do not continue researching indefinitely.
</termination_conditions>

<output_format>
<research_report>
<summary>
2-3 sentence overview of findings
</summary>

<key_findings>
[Information-dense bullet points organized thematically]
- Finding 1 [Source citation]
- Finding 2 [Source citation]
[Use exact quotes for critical facts]
</key_findings>

<source_quality_assessment>
[Brief note on overall source reliability]
</source_quality_assessment>

<conflicting_information>
[Any contradictions found with citations for each perspective]
</conflicting_information>

<gaps>
[Information not found or unclear]
</gaps>

<sources>
[Full bibliography]
</sources>
</research_report>
</output_format>

<task>
Research assigned topic: {{TOPIC}}

Specific focus areas from lead agent:
{{FOCUS_AREAS}}

Context from user's original question:
{{USER_QUESTION_CONTEXT}}
</task>
```

**When to use:**
- Autonomous operation with tool access
- Iterative or exploratory workflows
- Budget constraints needed
- Quality gates and termination conditions required
- Part of multi-agent orchestration

## Multi-Window Pattern

For tasks spanning multiple context windows with state persistence.

**Initial Prompt Structure:**
```
<role>
[IDENTITY AND CAPABILITIES]
[CONTEXT TRACKING RESPONSIBILITIES]
</role>

<objective>
[LONG-TERM GOAL]
[THIS SESSION'S FOCUS]
</objective>

<state_management>
Persistence strategy:
- Create {{STATE_FILE}} after each significant milestone
- Structure: JSON with keys: progress, findings, next_steps, context
- Update incrementally, don't recreate from scratch
- On continuation, load state first before proceeding

State file structure:
{
  "session": "initial|continuation-N",
  "progress": {
    "completed": ["task1", "task2"],
    "in_progress": ["task3"],
    "pending": ["task4", "task5"]
  },
  "findings": {
    "category1": ["finding1", "finding2"],
    "category2": ["finding3"]
  },
  "next_steps": ["step1", "step2"],
  "context": {
    "key_decisions": [],
    "important_observations": []
  }
}
</state_management>

<instructions>
[TASK GUIDANCE FOR INITIAL SESSION]

Before completing this session:
1. Create/update {{STATE_FILE}} with current progress
2. Document key findings and decisions
3. Outline next steps for continuation
4. Summarize what remains to be done
</instructions>

<data>
{{INITIAL_INPUT}}
</data>
```

**Continuation Prompt Structure:**
```
<role>
[SAME AS INITIAL]
</role>

<objective>
[SAME LONG-TERM GOAL]
[THIS SESSION'S FOCUS]
</objective>

<state_restoration>
1. Load {{STATE_FILE}}
2. Review progress, findings, and context
3. Identify where to resume
4. Continue work from last checkpoint
</state_restoration>

<instructions>
[TASK GUIDANCE FOR CONTINUATION]

Pick up where the previous session left off:
- Review state file thoroughly
- Continue with next_steps from previous session
- Update progress as you work
- Save updated state before completing

Before completing this session:
1. Update {{STATE_FILE}} with new progress
2. Document new findings and decisions
3. Outline next steps if work continues
4. Summarize remaining work
</instructions>

<data>
{{CONTINUATION_INPUT}}
</data>
```

**Example: Test Suite Implementation**

Initial prompt:
```
<role>
You are a test engineer implementing comprehensive test coverage for a codebase. You track your progress across multiple sessions, maintaining clear state about what's been tested and what remains.
</role>

<objective>
Long-term: Achieve 90% test coverage for the authentication module.
This session: Analyze the module, create test plan, begin implementation.
</objective>

<state_management>
Persistence strategy:
- Create test-progress.json after analysis and after implementing each test file
- Track which files tested, coverage metrics, issues found
- Document decisions about test strategies

State file structure:
{
  "session": "initial",
  "progress": {
    "analyzed": [],
    "tested": [],
    "coverage_current": 0,
    "coverage_target": 90
  },
  "findings": {
    "edge_cases": [],
    "integration_needs": [],
    "mocking_strategies": {}
  },
  "test_plan": [],
  "next_steps": []
}
</state_management>

<instructions>
1. Analyze authentication module structure
   - Identify all functions and classes
   - Determine critical paths and edge cases
   - Note dependencies requiring mocks

2. Create comprehensive test plan
   - Map functions to test files
   - Identify test categories (unit, integration)
   - Estimate effort for each component

3. Begin implementation with highest priority tests
   - Start with critical authentication paths
   - Write tests until approaching context limit

4. Before completing:
   - Save progress to test-progress.json
   - Document test coverage achieved
   - List next test files to implement
   - Note any blockers or decisions needed

Focus on thoroughness over speed. Each test should cover:
- Happy path
- Error conditions
- Edge cases
- Security considerations
</instructions>

<module_path>
{{MODULE_PATH}}
</module_path>
```

Continuation prompt:
```
<role>
You are a test engineer implementing comprehensive test coverage for a codebase. You track your progress across multiple sessions, maintaining clear state about what's been tested and what remains.
</role>

<objective>
Long-term: Achieve 90% test coverage for the authentication module.
This session: Continue test implementation from previous session.
</objective>

<state_restoration>
1. Read test-progress.json
2. Review what's been tested and current coverage
3. Check next_steps for where to resume
4. Continue with the next test file in plan
</state_restoration>

<instructions>
1. Load and review test-progress.json

2. Continue test implementation:
   - Follow test_plan from state file
   - Implement next priority test files
   - Update coverage metrics as you progress

3. Throughout session:
   - Mark test files as completed in progress
   - Document new findings or edge cases
   - Update coverage_current percentage

4. Before completing:
   - Update test-progress.json with new progress
   - Recalculate coverage percentage
   - Update next_steps for next session
   - Note if approaching 90% target

Continue until context window near capacity, then save state.
</instructions>

<module_path>
{{MODULE_PATH}}
</module_path>
```

**When to use:**
- Tasks requiring >100K tokens to complete
- Extended implementation work
- Iterative refinement across sessions
- Progress tracking essential
- State needs to persist between windows

## Template Variables

For reusable prompt patterns with dynamic inputs.

**Variable Naming:**
- Use {{DOUBLE_BRACES}} in Console and APIs
- Descriptive names in UPPER_CASE
- Document expected type and format

**Common Variable Types:**

1. **User inputs:** {{USER_QUERY}}, {{USER_CODE}}, {{USER_PREFERENCES}}
2. **Retrieved content:** {{SEARCH_RESULTS}}, {{DOCUMENT}}, {{CONTEXT}}
3. **Conversation context:** {{CHAT_HISTORY}}, {{USER_PROFILE}}
4. **System-generated:** {{TIMESTAMP}}, {{SESSION_ID}}, {{TOOL_OUTPUTS}}

**Example: Reusable Translation Template**
```
Translate the following text from {{SOURCE_LANGUAGE}} to {{TARGET_LANGUAGE}}.

Translation requirements:
- Preserve tone: {{TONE}}
- Target audience: {{AUDIENCE}}
- Formality level: {{FORMALITY}}

{{TEXT_TO_TRANSLATE}}

Output format:
<translation>
[Translated text]
</translation>

<notes>
[Any translation decisions or ambiguities]
</notes>
```

**Benefits:**
- Consistency across multiple uses
- Easy testing with different inputs
- Clear separation of static instructions from dynamic data
- Version control for prompt logic
- Reusable across projects

## Pattern Selection Guide

Choose pattern based on task characteristics:

| Task Type | Pattern | Key Indicators |
|-----------|---------|----------------|
| Single focused task | Simple Task | Clear input/output, minimal reasoning |
| Multi-step analysis | Complex Reasoning | Judgment needed, tradeoffs, verification |
| Autonomous agent | Agent/Workflow | Tool access, iterative, budget constraints |
| Long-running work | Multi-Window | >100K tokens, session persistence needed |
| Reusable template | Template Variables | Multiple similar uses, dynamic inputs |

Can combine patterns:
- Agent + Multi-Window: Long-running autonomous work
- Complex Reasoning + Template Variables: Reusable analysis workflows
- Simple Task + Template Variables: Reusable single-step operations

---

## Multi-Context Window Workflows

For Claude 4.5 models with context awareness and capability to manage tokens across extended sessions.

### Pattern Overview

Multi-context workflows enable Claude to work on complex tasks spanning multiple context windows while maintaining state and progress.

**Key capabilities:**
- Context awareness: Claude knows remaining token budget
- Automatic compaction: Context auto-refreshes when limit approaches
- State persistence: Save progress to external files
- Long-horizon reasoning: Think incrementally across windows

### Phase 1: Setup (First Context Window)

**Purpose:** Establish framework and groundwork before implementation.

**Structure:**
```xml
<first_window_instructions>
This task spans multiple context windows. Set up the framework BEFORE implementing:

1. **Create test structure**
   - Define test suite organization
   - Create test template files
   - Commit initial test framework to git

2. **Define architecture**
   - Design component structure
   - Document module responsibilities
   - Create architecture diagram or spec

3. **Plan implementation**
   - Break work into phases
   - List each phase's components
   - Identify dependencies between phases
   - Create TODO list

4. **Set up quality of life tools**
   - Create setup/init scripts
   - Add build/test scripts
   - Document commands needed

5. **Save plan to files**
   - Write plan.md with full roadmap
   - Save test structure to test_structure.json
   - Commit everything to git

DO NOT start implementation in first window. Focus entirely on preparation.
</first_window_instructions>
```

### Phase 2-N: Iteration (Subsequent Context Windows)

**Purpose:** Implement features while maintaining state and quality.

**Structure:**
```xml
<subsequent_window_instructions>
Context window {{N}} - Continue from saved state:

1. **Check state and progress**
   - Read progress.json (see what was completed)
   - Check git log (verify last commits)
   - Review test structure (understand testing strategy)

2. **Verify setup**
   - Run tests to ensure they still pass
   - Verify no breaking changes from last session
   - Quick smoke test of existing functionality

3. **Implement next phase**
   - Reference plan.md for current phase
   - Follow test-driven approach (write tests first)
   - Keep test coverage high
   - Implement incrementally

4. **Update progress tracking**
   ```json
   {
     "phase": 3,
     "completed": ["setup", "auth", "database"],
     "in_progress": "user_management",
     "next_phases": ["api_endpoints", "frontend", "testing"],
     "token_estimate_remaining": 5000,
     "last_commit": "impl: user management endpoints"
   }
   ```

5. **Commit regularly**
   - Commit after each component completes
   - Include test updates in commits
   - Write clear commit messages

6. **Before window ends**
   - Update progress.json with final state
   - Commit all changes
   - Document any blockers or decisions needed
   - Verify tests still pass
</subsequent_window_instructions>
```

### State Management Structure

**Progress tracking file (progress.json):**
```json
{
  "project": "project_name",
  "status": "in_progress|completed",
  "phase": 3,
  "phases": {
    "1_setup": {
      "status": "completed",
      "items": ["architecture_defined", "tests_created", "scripts_ready"]
    },
    "2_auth": {
      "status": "completed",
      "tests_passing": true,
      "coverage": 95
    },
    "3_api": {
      "status": "in_progress",
      "tests_passing": true,
      "coverage": 88,
      "completed_endpoints": ["GET /users", "POST /users"],
      "next": ["PUT /users/:id", "DELETE /users/:id"]
    }
  },
  "completed_count": 2,
  "total_phases": 5,
  "token_estimate_next_window": 4000,
  "last_updated": "2025-11-29T23:00:00Z",
  "last_commit": "impl: GET/POST user endpoints",
  "blockers": [],
  "decisions_needed": []
}
```

**Tests tracking (test_structure.json):**
```json
{
  "test_framework": "pytest",
  "coverage_target": 90,
  "test_suites": {
    "unit": {
      "path": "tests/unit/",
      "status": "passing",
      "count": 24,
      "coverage": 95
    },
    "integration": {
      "path": "tests/integration/",
      "status": "passing",
      "count": 12,
      "coverage": 88
    },
    "e2e": {
      "path": "tests/e2e/",
      "status": "passing",
      "count": 8,
      "coverage": 75
    }
  },
  "commands": {
    "run_all": "pytest tests/",
    "run_unit": "pytest tests/unit/",
    "coverage_report": "pytest --cov=src tests/"
  }
}
```

### Context Awareness Best Practices

**Leverage token budget visibility:**
```xml
<context_awareness>
Claude 4.5 models know their remaining token budget. Use this intelligently:

1. **Monitor budget:** Pay attention to context fill level
2. **Plan phase scope:** Adjust phase scope to fit context window
3. **Save proactively:** Save state before context fills completely
4. **Optimize writing:** Write to files systematically (avoid verbose output)
5. **Use git efficiently:** Commit frequently so state is always saved

Messages approaching context limit:
- Wrap up current phase
- Update progress files
- Commit final changes
- Summarize what's done
- Don't start new complex tasks
</context_awareness>
```

**Starting fresh vs compacting:**
```xml
<window_strategy>
When starting new context window:

Option A: Use automatic compaction
- Claude Code will compact context automatically
- Pros: Seamless, no manual setup
- Cons: Less control over what persists

Option B: Start fresh context
- Read from files (git, progress.json, test results)
- Pros: Full control, clear state
- Cons: Manual setup needed

Recommendation for Claude 4.5: Start fresh
- Claude 4.5 is excellent at discovering state from files
- Cleaner context for new work
- Git provides excellent checkpoint capability
</window_strategy>
```

### Complete Example: Multi-Window Feature Implementation

**Window 1 (Setup):**
```xml
<task>
Build a REST API backend for a notes application.
Estimated time: 3+ context windows.
</task>

<window_1_setup>
1. Create test framework (pytest with fixtures)
2. Define API schema (OpenAPI spec)
3. Plan implementation (5 phases: auth, CRUD, validation, caching, deployment)
4. Create init.sh script for setup
5. Create Makefile with test/build commands
6. Commit framework to git
</window_1_setup>
```

**Window 2 (Auth):**
```
1. Check progress: Read progress.json (phase 1 done)
2. Verify setup: Run make test (all green)
3. Implement: User authentication endpoints
4. Tests: 18 new tests, 92% coverage
5. Update: progress.json shows "auth" complete
6. Commit: "feat: implement JWT authentication"
```

**Window 3 (CRUD):**
```
1. Check progress: Read progress.json (phase 2 done)
2. Verify: Run tests (auth still passing)
3. Implement: Notes CRUD endpoints
4. Tests: 24 new tests, 89% coverage
5. Update: progress.json, mark phase 3 in_progress
6. Commit: "feat: implement notes CRUD endpoints"
```

**Final Window (Polish):**
```
1. Check progress: phase 3 done, 4 phases remaining
2. Run full test suite: 60 tests passing
3. Quick refactoring: Code cleanup, consistency
4. Update: progress.json final status
5. Commit: "refactor: code cleanup and documentation"
6. Summary: "Backend API complete, ready for frontend integration"
```

### Decision Tree: When to Use Multi-Context

```
Is task >100K tokens to complete?
├─ Yes
│  ├─ Does work need to persist between sessions?
│  │  ├─ Yes → Use Multi-Context Workflow
│  │  └─ No → Use Multi-Window (single session, auto-compaction)
│  └─ Does it need iterative refinement?
│     ├─ Yes → Use Multi-Context with state tracking
│     └─ No → Might fit in single window with optimization
│
└─ No
   └─ Use other patterns (Simple Task, Complex Reasoning, Agent)
```
