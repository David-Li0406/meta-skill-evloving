# Decision Matrix: When to Use Subagents

Comprehensive criteria for evaluating subagent delegation vs direct tool calls.

## Scoring Framework

Evaluate task against all criteria. Each met criterion adds points to delegation score.

### Context Preservation (0-2 points)

**+2 points if ANY of:**
- Main conversation context contains 15,000+ tokens of search results
- Expecting 10+ file reads or grep results in response
- User explicitly mentions context or memory concerns
- Previous similar task caused context overflow

**+1 point if:**
- Main conversation at 8,000-15,000 tokens
- Task will add 3,000+ tokens of tool results
- Multiple iterations of search refinement anticipated

**0 points if:**
- Main conversation under 8,000 tokens
- Task produces minimal output (1-2 file reads)
- Tool results easily summarizable

### Task Complexity (0-2 points)

**+2 points if ANY of:**
- Task requires 10+ tool calls
- Uncertain number of iterations (search until pattern found)
- Multi-phase workflow (search → analyze → search again)
- Task involves conditional logic based on intermediate results

**+1 point if:**
- Task requires 5-9 tool calls
- Two-phase workflow (e.g., search then read matching files)
- Some conditional logic but predictable branches

**0 points if:**
- Task requires 1-4 tool calls
- Linear execution with no conditionals
- All steps known upfront

### Parallelization Opportunity (0-2 points)

**+2 points if:**
- 3+ independent search operations possible
- Each search targets different codebase area
- No data dependencies between searches
- Results can be synthesized after completion

**+1 point if:**
- 2 independent operations possible
- Partial data dependencies (some sequential, some parallel)
- Moderate benefit from parallelization

**0 points if:**
- All operations sequential
- Strong data dependencies
- Single search operation

### Focus Requirement (0-2 points)

**+2 points if ANY of:**
- Task needs specialized system prompt (specific analysis lens)
- Task requires behavior modification (different communication style)
- Task needs tool restrictions (security or focus)
- Task domain-specific enough to benefit from focused instructions

**+1 point if:**
- Task would benefit from slight prompt adjustment
- Some tool restrictions helpful but not essential
- Minor focus benefit from isolation

**0 points if:**
- No specialized prompt needed
- Main conversation context already has right focus
- Tool restrictions unnecessary

### Iteration Depth (0-2 points)

**+2 points if:**
- Task requires retry loops (search, evaluate, retry with refinement)
- Progressive refinement strategy (narrow down search space)
- Multiple rounds of hypothesis testing
- Uncertain end condition (search until criteria met)

**+1 point if:**
- 2-3 iterations expected
- Somewhat predictable iteration pattern
- Moderate refinement needed

**0 points if:**
- Single execution pass
- No retry logic needed
- Clear completion criteria from start

## Score Interpretation

### 0-3 Points: Direct Tool Calls
Use direct tool calls in main conversation.

**Rationale:** Task simple enough that delegation overhead (agent initialization, context building) exceeds benefit. Main conversation has sufficient context.

**Example patterns:**
- Read specific known file
- Single grep for known pattern
- Simple 2-3 step workflow
- Quick verification task

### 4-6 Points: Conditional Delegation
Consider subagent based on additional factors.

**Consider subagent if:**
- User has expressed preference for agent usage
- Main conversation already complex (easier to track in separate agent)
- Task forms logical boundary (clean separation of concerns)
- Similar tasks previously used agents successfully

**Use direct calls if:**
- User prefers seeing tool usage directly
- Main conversation benefits from seeing intermediate results
- Interactive refinement needed
- Task closely tied to ongoing conversation

**Example patterns:**
- Moderate codebase exploration (4-6 file searches)
- Two-phase workflow with some complexity
- Parallel searches but only 2 operations
- Tasks on boundary of simple/complex

### 7-10 Points: Strong Subagent Candidate
Use Task tool for delegation.

**Rationale:** Benefits clearly outweigh overhead. Context preservation, parallelization, or complexity justify delegation.

**Example patterns:**
- Comprehensive codebase exploration (many searches)
- Complex multi-phase workflows
- 3+ parallel operations
- Uncertain iteration count
- Specialized focus requirement

## Edge Cases and Special Considerations

### User Interaction Requirements

**Never use subagent if:**
- Task requires asking user followup questions during execution
- User needs to see intermediate results for decision-making
- Interactive refinement based on partial results
- User explicitly requests direct execution

**Subagents cannot:**
- Pause execution to ask questions
- Present options for user selection
- Get user approval mid-task
- React to user interruptions

### Tool Availability

**Verify tool access before delegation:**
- Check if agent has necessary tools (if tools field restricts access)
- MCP tools inherited only if tools field omitted
- Some agents restrict to subset (Plan agent: Read, Glob, Grep, Bash)

**If required tool not available:**
- Use direct tool calls OR
- Use general-purpose agent (has all tools) OR
- Recommend creating custom agent with right tools

### Context Handoff

**Use subagent only if:**
- All necessary context can be provided in task prompt
- Task self-contained enough to execute autonomously
- Output format clearly specifiable upfront

**Use direct calls if:**
- Task needs ongoing conversation context
- Many references to "the previous file" or "earlier discussion"
- Context too complex to summarize in prompt

## Built-in Agent Selection

After deciding to use subagent, select appropriate type:

### Explore Agent
**Use when:**
- Primary goal: find files or code patterns
- Codebase exploration or search task
- Answering "how does X work" about code
- Finding implementation of feature
- Searching for API usage patterns

**Thoroughness levels:**
- `quick`: Basic search, 1-2 locations, common naming patterns (use for: 0-3 complexity points)
- `medium`: Moderate exploration, multiple locations, some variant patterns (use for: 4-6 complexity points)
- `very thorough`: Comprehensive analysis, all locations, all naming conventions (use for: 7+ complexity points)

**Tool access:** All tools available

**Model:** Sonnet

### General-Purpose Agent
**Use when:**
- Task doesn't fit Explore pattern
- Mix of tool types needed (not just search)
- Complex multi-step workflow beyond exploration
- Autonomous task with uncertain execution path

**Tool access:** All tools available

**Model:** Inherits from configuration (usually Sonnet)

### Plan Agent
**Never manually invoke.**

Automatically activates during plan mode for research.

## Custom Agent Evaluation

If no built-in agent matches, evaluate custom agent need:

### Search for Existing Custom Agents
1. Use Glob: `~/.claude/agents/**/*.md`
2. Use Glob: `.claude/agents/**/*.md`
3. Use Grep to search descriptions for trigger keywords
4. Read candidate agents to verify match

### Criteria for Recommending New Custom Agent
Need 4+ of these for strong recommendation:
- [ ] Task pattern repeats across conversations
- [ ] Specialized system prompt provides value
- [ ] Isolated context beneficial
- [ ] Parallelization useful
- [ ] Specific tool restrictions needed
- [ ] Clear completion criteria
- [ ] Domain-specific enough for focused instructions

If 0-3 criteria: Use general-purpose agent instead

## Practical Examples with Scoring

### Example 1: "Find all API endpoints"
- Context preservation: +1 (will generate moderate results)
- Task complexity: +2 (many searches, iterative refinement)
- Parallelization: +2 (can search multiple directories)
- Focus requirement: +1 (API-specific focus helpful)
- Iteration depth: +2 (progressive refinement likely)
- **Total: 8 points → Use Explore agent with "very thorough"**

### Example 2: "Read config.json"
- Context preservation: 0 (single small file)
- Task complexity: 0 (single read)
- Parallelization: 0 (single operation)
- Focus requirement: 0 (no special focus)
- Iteration depth: 0 (one pass)
- **Total: 0 points → Use direct Read tool**

### Example 3: "Search for error handling patterns in 3 specific modules"
- Context preservation: +1 (moderate results)
- Task complexity: +1 (6-9 greps likely)
- Parallelization: +2 (3 independent searches)
- Focus requirement: +1 (error handling focus)
- Iteration depth: 0 (single pass per module)
- **Total: 5 points → Conditional - consider Explore agent if main conversation already complex, otherwise direct calls**

### Example 4: "Analyze this file for security issues"
- Context preservation: 0 (single file analysis)
- Task complexity: +1 (analysis workflow)
- Parallelization: 0 (single file)
- Focus requirement: +2 (security-specific lens)
- Iteration depth: 0 (single pass)
- **Total: 3 points → Direct analysis, but check for existing security-review custom agent**

## Decision Tree Summary

```
Is task self-contained? NO → Direct calls
  ↓ YES
Calculate delegation score (0-10)
  ↓
Score 0-3? YES → Direct calls
  ↓ NO
Score 4-6? YES → Evaluate context factors
  ↓          ↓
  ↓        Factor favor agent? YES → Proceed to agent selection
  ↓          ↓ NO
  ↓        Direct calls
  ↓
Score 7-10? YES → Proceed to agent selection
  ↓
Agent selection:
  ↓
Is primary goal codebase search/exploration? YES → Explore agent (set thoroughness by complexity)
  ↓ NO
Is there matching custom agent? YES → Use custom agent
  ↓ NO
Use general-purpose agent
```
