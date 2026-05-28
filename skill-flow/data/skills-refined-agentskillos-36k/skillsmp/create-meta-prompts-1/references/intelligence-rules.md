<overview>
Guidelines for determining prompt complexity, tool usage, optimization patterns, and context management for long-running workflows.
</overview>

<complexity_assessment>

<simple_prompts>
Single focused task, clear outcome:

**Indicators:**

- Single artifact output
- No dependencies on other files
- Straightforward requirements
- No decision-making needed

**Prompt characteristics:**

- Concise objective
- Minimal context
- Direct requirements
- Simple verification
  </simple_prompts>

<complex_prompts>
Multi-step tasks, multiple considerations:

**Indicators:**

- Multiple artifacts or phases
- Dependencies on research/plan files
- Trade-offs to consider
- Integration with existing code

**Prompt characteristics:**

- Detailed objective with context
- Referenced files
- Explicit implementation guidance
- Comprehensive verification
- Extended thinking triggers
  </complex_prompts>

</complexity_assessment>

<extended_thinking_triggers>

<when_to_include>
Use these phrases to activate deeper reasoning in complex prompts:

- Complex architectural decisions
- Multiple valid approaches to evaluate
- Security-sensitive implementations
- Performance optimization tasks
- Trade-off analysis
  </when_to_include>

<trigger_phrases>

```
"Thoroughly analyze..."
"Consider multiple approaches..."
"Deeply consider the implications..."
"Explore various solutions before..."
"Carefully evaluate trade-offs..."
```

</trigger_phrases>

<example_usage>

```xml
<requirements>
Thoroughly analyze the authentication options and consider multiple
approaches before selecting an implementation. Deeply consider the
security implications of each choice.
</requirements>
```

</example_usage>

<when_not_to_use>

- Simple, straightforward tasks
- Tasks with clear single approach
- Following established patterns
- Basic CRUD operations
  </when_not_to_use>

</extended_thinking_triggers>

<parallel_tool_calling>

<when_to_include>

```xml
<efficiency>
For maximum efficiency, invoke all independent tool operations
simultaneously rather than sequentially. Multiple file reads,
searches, and API calls that don't depend on each other should
run in parallel.
</efficiency>
```

</when_to_include>

<applicable_scenarios>

- Reading multiple files for context
- Running multiple searches
- Fetching from multiple sources
- Creating multiple independent files
  </applicable_scenarios>

</parallel_tool_calling>

<context_loading>

<when_to_load>

- Modifying existing code
- Following established patterns
- Integrating with current systems
- Building on research/plan outputs
  </when_to_load>

<when_not_to_load>

- Greenfield features
- Standalone utilities
- Pure research tasks
- Standard patterns without customization
  </when_not_to_load>

<loading_patterns>

```xml
<context>
<!-- Chained artifacts -->
Research: @.prompts/001-auth-research/auth-research.md
Plan: @.prompts/002-auth-plan/auth-plan.md

<!-- Existing code to modify -->
Current implementation: @src/auth/middleware.ts
Types to extend: @src/types/auth.ts

<!-- Patterns to follow -->
Similar feature: @src/features/payments/
</context>
```

</loading_patterns>

</context_loading>

<output_optimization>

<claude_to_claude>
For Claude-to-Claude consumption:

**Use heavy XML structure:**

```xml
<findings>
  <finding category="security">
    <title>Token Storage</title>
    <recommendation>httpOnly cookies</recommendation>
    <rationale>Prevents XSS access</rationale>
  </finding>
</findings>
```

**Include metadata:**

```xml
<metadata>
  <confidence level="high">Verified in official docs</confidence>
  <dependencies>Cookie parser middleware</dependencies>
  <open_questions>SameSite policy for subdomains</open_questions>
</metadata>
```

**Be explicit about next steps:**

```xml
<next_actions>
  <action priority="high">Create planning prompt using these findings</action>
  <action priority="medium">Validate rate limits in sandbox</action>
</next_actions>
```

</claude_to_claude>

<human_consumption>
For human consumption:

- Clear headings
- Bullet points for scanning
- Code examples with comments
- Summary at top
  </human_consumption>

</output_optimization>

<prompt_depth_guidelines>

<minimal>
Simple Do prompts:
- 20-40 lines
- Basic objective, requirements, output, verification
- No extended thinking
- No parallel tool hints
</minimal>

<standard>
Typical task prompts:
- 40-80 lines
- Full objective with context
- Clear requirements and implementation notes
- Standard verification
</standard>

<comprehensive>
Complex task prompts:
- 80-150 lines
- Extended thinking triggers
- Parallel tool calling hints
- Multiple verification steps
- Detailed success criteria
</comprehensive>

</prompt_depth_guidelines>

<why_explanations>

Always explain why constraints matter:

<bad_example>

```xml
<requirements>
Never store tokens in localStorage.
</requirements>
```

</bad_example>

<good_example>

```xml
<requirements>
Never store tokens in localStorage - it's accessible to any
JavaScript on the page, making it vulnerable to XSS attacks.
Use httpOnly cookies instead.
</requirements>
```

</good_example>

This helps the executing Claude make good decisions when facing edge cases.

</why_explanations>

<verification_patterns>

<for_code>

```xml
<verification>
1. Run test suite: `npm test`
2. Type check: `npx tsc --noEmit`
3. Lint: `bun run lint`
4. Manual test: [specific flow to test]
</verification>
```

</for_code>

<for_documents>

```xml
<verification>
1. Validate structure: [check required sections]
2. Verify links: [check internal references]
3. Review completeness: [check against requirements]
</verification>
```

</for_documents>

<for_research>

```xml
<verification>
1. Sources are current (2024-2025)
2. All scope questions answered
3. Metadata captures uncertainties
4. Actionable recommendations included
</verification>
```

</for_research>

<for_plans>

```xml
<verification>
1. Phases are sequential and logical
2. Tasks are specific and actionable
3. Dependencies are clear
4. Metadata captures assumptions
</verification>
```

</for_plans>

</verification_patterns>

<chain_optimization>

<research_prompts>
Research prompts should:

- Structure findings for easy extraction
- Include code examples for implementation
- Clearly mark confidence levels
- List explicit next actions
  </research_prompts>

<plan_prompts>
Plan prompts should:

- Reference research explicitly
- Break phases into prompt-sized chunks
- Include execution hints per phase
- Capture dependencies between phases
  </plan_prompts>

<do_prompts>
Do prompts should:

- Reference both research and plan
- Follow plan phases explicitly
- Verify against research recommendations
- Update plan status when done
  </do_prompts>

</chain_optimization>

<context_awareness_integration>

<when_to_include>
For prompts targeting Claude Sonnet 4.5 or Haiku 4.5 with long-running tasks:

```xml
<context>
You are working in Claude Code with automatic context management.
Your context window will be compacted as needed, allowing indefinite
work. Focus on systematic progress through all requirements.
</context>
```

**Applicable scenarios:**

- Multi-phase implementations
- Research tasks with multiple areas to investigate
- Tasks likely to use >50% of context window (>100K tokens)
- Work that may span multiple sessions
  </when_to_include>

<when_not_to_include>

- Simple, single-shot tasks
- Tasks completing in <10K tokens
- One-off code generation
- Quick fixes or patches
  </when_not_to_include>

</context_awareness_integration>

<state_tracking_patterns>

<for_do_prompts>
When task has >5 distinct subtasks or may span multiple sessions:

```xml
<requirements>
Track progress systematically:

1. Create progress.json before starting:
{
  "tasks": [
    {"id": 1, "name": "setup", "status": "pending"},
    {"id": 2, "name": "implementation", "status": "pending"},
    {"id": 3, "name": "tests", "status": "pending"}
  ]
}

2. After each task:
   - Update progress.json status to "completed"
   - Append summary to progress.txt
   - Commit changes with descriptive message

3. If context refreshes:
   - Read progress.json to see completed tasks
   - Read progress.txt for context and decisions
   - Check git log for implementation history
   - Continue from first "pending" task
</requirements>
```

</for_do_prompts>

<for_research_prompts>
When research has multiple areas or may need resumption:

```xml
<instructions>
1. Create research-outline.md listing all investigation areas
2. For each area:
   a. Research thoroughly using web search and documentation
   b. Append findings to findings.md with clear section markers
   c. Mark area as [COMPLETE] in research-outline.md
   d. Save work before continuing
3. When all areas complete, synthesize into final output
</instructions>

<output_format>
findings.md should be append-only with status markers:
```

## Authentication Methods [COMPLETE]

...findings...

## Session Management [COMPLETE]

...findings...

## Rate Limiting [IN PROGRESS]

...partial findings...

```
</output_format>
```

</for_research_prompts>

<for_plan_prompts>
When plan has multiple phases requiring sequential execution:

```xml
<requirements>
Create phases that can be executed independently:

Each phase in your plan should:
1. Have clear entry criteria (what must be done first)
2. Have clear exit criteria (definition of done)
3. Be resumable if interrupted
4. Document decisions made during execution
</requirements>

<state_management>
Include in the plan:
- phase-status.json for tracking phase completion
- Checkpoints after each phase for git commits
- Verification steps before moving to next phase
</state_management>
```

</for_plan_prompts>

<test_first_pattern>
For complex implementations requiring high confidence:

```xml
<phase_1_setup>
Before any implementation:

1. Create tests.json with all required tests:
{
  "tests": [
    {"id": 1, "name": "user_auth_flow", "status": "pending"},
    {"id": 2, "name": "token_refresh", "status": "pending"}
  ],
  "total": 0,
  "passing": 0
}

2. Create init.sh for environment setup
3. Commit infrastructure
</phase_1_setup>

<phase_2_implementation>
For each test in tests.json:
1. Implement feature code
2. Run the test
3. If passing: Update tests.json status, increment passing count
4. If failing: Fix code (NEVER edit test to make it pass)
5. Commit when passing
6. Continue to next test
</phase_2_implementation>

<requirements>
It is unacceptable to remove or edit tests to make them pass.
Tests are the source of truth. All tests.json entries must
show "passing" before task is complete.
</requirements>
```

</test_first_pattern>

</state_tracking_patterns>

<multi_context_window_workflows>

<differentiated_first_context>
For prompts that may execute across multiple context windows:

**First context setup:**

```xml
<phase_1_infrastructure>
Set up framework for iterative work:
1. Create test suite in tests.json
2. Create setup scripts (init.sh, dev.sh)
3. Create state tracking files (progress.json, progress.txt)
4. Commit infrastructure
5. Mark setup complete in progress.json
</phase_1_infrastructure>
```

**Subsequent contexts:**

```xml
<context>
Infrastructure is already set up. Review:
- progress.json for task status
- progress.txt for context
- git log for history

Continue from next incomplete task.
</context>
```

</differentiated_first_context>

<fresh_start_advantages>
Rather than trying to preserve all context, design prompts to enable fresh starts:

```xml
<instructions>
If starting a new session:
1. Review progress.txt for completed work and decisions
2. Check tests.json for test status (target: all "passing")
3. Examine git log --oneline -10 for recent commits
4. Read current code to understand implementation state
5. Continue from last checkpoint

This discovery-based approach is more reliable than assuming
context from previous sessions.
</instructions>
```

</fresh_start_advantages>

<verification_mechanisms>
Enable autonomous verification without human feedback:

```xml
<verification>
After each significant change:
1. Run test suite: npm test
2. Run type check: npx tsc --noEmit
3. Run linter: bun run lint
4. Update tests.json with results
5. Only proceed if all checks pass

Self-verification enables autonomous progress across context windows.
</verification>
```

</verification_mechanisms>

</multi_context_window_workflows>

<context_budgeting>

<when_to_warn>
For prompts likely to use significant context (>100K tokens):

```xml
<efficiency>
Use your context budget wisely:
- Read only files directly relevant to the current task
- Use parallel tool calls for independent operations
- Focus on one task at a time rather than exploring broadly
- Save state frequently to enable resumption
</efficiency>
```

</when_to_warn>

<premium_pricing_awareness>
For enterprise usage or prompts targeting >200K tokens:

```xml
<note>
This task may exceed 200K tokens, which incurs premium pricing
(2x input, 1.5x output). Work efficiently and consider breaking
into smaller prompts if possible.
</note>
```

Only include if genuinely likely to exceed 200K.
</premium_pricing_awareness>

</context_budgeting>

<incremental_progress_emphasis>

<systematic_completion>
Encourage complete, autonomous work:

```xml
<objective>
Complete the entire {task} systematically. Work through all
requirements without stopping early. Your context is managed
automatically, so focus on thoroughness.
</objective>

<approach>
Work incrementally:
1. Complete one unit of work fully
2. Verify it works (tests, checks)
3. Commit with descriptive message
4. Document progress
5. Move to next unit

This incremental approach with commits enables recovery at any point.
</approach>
```

</systematic_completion>

<avoid_premature_stopping>
Counter the tendency to ask "should I continue?":

```xml
<requirements>
Do not stop to ask if you should continue. Work systematically
through all tasks in progress.json until all show "completed".
Your context management is automatic - focus on completing work.
</requirements>
```

Use only for long-running tasks where interruptions would be counterproductive.
</avoid_premature_stopping>

</incremental_progress_emphasis>
