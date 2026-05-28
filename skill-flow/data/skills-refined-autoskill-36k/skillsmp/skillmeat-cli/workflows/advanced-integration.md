# Advanced Agent Integration Workflow

Deep integration patterns for skillmeat-cli in advanced agent workflows.

---

## 1. Proactive Suggestions

Agents can suggest artifacts without being asked when capability gaps are detected.

### When to Suggest

**Trigger Conditions**:
- Detected capability gap (missing tool for current task)
- Error pattern matches artifact's specialty
- User expresses frustration or repeatedly tries similar approaches
- Task complexity suggests specialized skill would help

**Example Triggers**:
```
# Capability gap
User: "Can you analyze this CSV and find duplicates?"
→ No csv-processing skill deployed
→ Suggest: "I can help with that. Would you like me to deploy the csv-processing skill for advanced CSV operations?"

# Error pattern
Error: "Command 'jq' not found"
→ User working with JSON
→ Suggest: "I notice you're working with JSON. The json-jq skill provides advanced JSON querying. Deploy it?"

# User frustration
User: "How do I filter these rows again?"
→ Third similar question
→ Suggest: "The data-analysis skill has shortcuts for common operations. Would that help?"
```

### CRITICAL: Permission Required

**NEVER deploy without user permission**, even when proactively suggesting.

**Permission Pattern**:
```
1. Detect gap
2. Present suggestion with:
   - What artifact would help
   - Why it's relevant
   - What it enables
3. Wait for explicit yes/no
4. Track decision for session
```

**Good Suggestion**:
```
"I notice you're working with PDFs. The pdf-processing skill can extract text, split pages, and merge documents. Would you like me to deploy it?

[Details: anthropics/skills/pdf-tools, 4.5★, ~2MB]"
```

**Bad Suggestion**:
```
"Deploying pdf-processing skill..."  ❌ No permission!
```

### Suggestion Frequency Limits

**Per Session**:
- Max 3 unsolicited suggestions per session
- If 2 declined in a row, stop suggesting for this session
- Track declined artifacts, don't re-suggest

**Per Task**:
- Max 1 suggestion at task start
- Max 1 suggestion during task (only if clear gap emerges)
- No suggestions after user says "no thanks" or similar

---

## 2. Cross-Agent Coordination

Agents can recommend artifacts to each other via task delegation.

### Handoff Pattern

**Agent A** (discovers gap) → **Agent B** (implements):

```
Agent A discovers:
"User needs component library, but no design-system skill deployed"

Agent A delegates to Agent B:
Task("ui-engineer", "Create login form component.

     NOTE: Consider deploying frontend-design skill first - has form patterns and validation.
     Check: skillmeat search 'form validation' --type skill
     If found and relevant, suggest to user before starting.")
```

### Coordination Examples

**codebase-explorer → python-backend-engineer**:
```
Explorer finds FastAPI endpoints without OpenAPI docs
→ Adds to summary: "Consider openapi-expert skill for API documentation"
→ Backend engineer sees note
→ Suggests to user if starting documentation task
```

**ultrathink-debugger → codebase-explorer**:
```
Debugger needs to understand codebase structure
→ Checks for architecture-analysis skills
→ If found: "codebase-architecture skill could help map dependencies"
→ Explorer deploys if user agrees
```

**ui-engineer → python-backend-engineer**:
```
Frontend needs API endpoint that doesn't exist
→ UI engineer notes in handoff: "Backend may need api-scaffold skill"
→ Backend engineer evaluates when creating endpoint
```

### Handoff Format

**In Task Delegation**:
```
Task("{agent}", "{primary task}

     ARTIFACT SUGGESTION:
     - Skill: {name}
     - Reason: {why relevant}
     - Usage: {how it helps}
     - Check: skillmeat search '{query}'

     Get user permission before deploying.")
```

---

## 3. Session Context Tracking

Track artifact suggestions and decisions within session.

### What to Track

**Session State**:
- Artifacts suggested this session
- User decisions (accepted/declined)
- Artifacts deployed this session
- Artifacts used successfully
- Artifacts that didn't help

**Anti-Pattern Detection**:
- Don't re-suggest declined artifacts
- Don't suggest if user said "no more suggestions"
- Don't suggest similar artifacts if one declined

### Implementation Pattern

**Start of Session**:
```
session_context = {
  "suggested": [],
  "declined": [],
  "deployed": [],
  "successful": [],
  "failed": []
}
```

**Before Suggesting**:
```
1. Check session_context["declined"]
   → If artifact in list, skip suggestion

2. Check session_context["suggested"]
   → If count >= 3, skip suggestion

3. Check for similar artifacts
   → If similar declined, skip suggestion
```

**After User Decision**:
```
# User accepts
session_context["deployed"].append(artifact_name)

# User declines
session_context["declined"].append(artifact_name)

# User says "no more suggestions"
session_context["stop_suggesting"] = True
```

**Session Handoff**:
```
When passing to next agent:
"Session context: User has declined {declined_artifacts}.
Do not re-suggest these."
```

---

## 4. Batch Deployment

Deploy multiple related artifacts as a bundle.

### When to Batch

**Trigger Conditions**:
- Multiple artifacts from same collection
- Related artifacts for complete workflow
- User starting large project with known requirements

**Example Scenarios**:
```
# Document processing project
User: "I need to process Word docs, PDFs, and spreadsheets"
→ Batch: "Document processing bundle"
  - docx-processing
  - pdf-tools
  - csv-data
→ Single permission: "Deploy all 3 document skills?"

# Full-stack development
User: "Setting up new React + FastAPI project"
→ Batch: "Full-stack bundle"
  - react-patterns
  - api-scaffold
  - openapi-expert
→ Permission: "Deploy 3-skill development bundle?"
```

### Bundle Presentation

**Format**:
```
I've found {N} related artifacts for {task}:

Bundle: "{bundle_name}"
- {artifact1}: {brief description}
- {artifact2}: {brief description}
- {artifact3}: {brief description}

Total size: {size}, avg rating: {rating}

Deploy all? (Or I can deploy individually if you prefer)
```

**Individual Opt-Out**:
```
User: "Deploy all except PDF tools"
→ Deploy artifact1, artifact2
→ Skip artifact3
→ Confirm: "Deployed 2 of 3 artifacts"
```

### Pre-Defined Bundles

**Document Processing**:
- docx-processing
- pdf-tools
- csv-data

**Web Development**:
- react-patterns
- api-scaffold
- frontend-design

**Data Analysis**:
- csv-processing
- json-jq
- data-visualization

**DevOps**:
- docker-compose
- kubernetes-kubectl
- terraform-iac

---

## 5. Pre-Task Analysis

Analyze requirements before starting complex tasks.

### Analysis Workflow

**Step 1: Requirement Extraction**:
```
User: "Build a dashboard with charts showing CSV data"

Extract keywords:
- dashboard → UI components
- charts → data visualization
- CSV → data processing
```

**Step 2: Gap Detection**:
```
skillmeat search "dashboard components" --type skill --json
skillmeat search "chart visualization" --type skill --json
skillmeat search "csv processing" --type skill --json

Compare with deployed artifacts
Identify gaps
```

**Step 3: Presentation**:
```
Before I start, I found some artifacts that could help:

This task involves:
- Dashboard UI → react-dashboard (4.8★, components + layouts)
- Data visualization → chart-builder (4.6★, D3.js patterns)
- CSV processing → Already deployed ✓

Would you like me to deploy the first two before starting?
```

### Task Type → Artifact Mapping

**UI Development**:
- Check: react-patterns, component-library, frontend-design
- Suggest if: Creating new components, design system work

**API Development**:
- Check: api-scaffold, openapi-expert, rest-patterns
- Suggest if: Creating endpoints, documentation needed

**Data Processing**:
- Check: csv-processing, json-jq, data-transform
- Suggest if: Working with structured data

**Database Work**:
- Check: postgresql-psql, sql-query, database-schema
- Suggest if: Schema changes, query optimization

**Testing**:
- Check: test-patterns, pytest-advanced, test-data
- Suggest if: Writing tests, setting up test infrastructure

**Documentation**:
- Check: markdown-docs, api-docs, diagram-tools
- Suggest if: Creating user docs, technical docs

### Silent Analysis Pattern

**When to be silent**:
- Pre-task check finds no gaps
- User explicitly said "just do it"
- Simple tasks (< 5 minutes)
- User is expert in domain

**When to present**:
- 2+ relevant artifacts found
- Complex task (> 30 minutes)
- User new to domain
- Task has known pitfalls artifacts solve

---

## 6. Integration with Specialized Agents

### codebase-explorer

**Integration Points**:
```
WHEN: Starting codebase exploration
CHECK:
  - Architecture analysis skills
  - Language-specific linting tools
  - Documentation generators

IF FOUND:
  Add to summary:
  "Note: {skill} could help with {specific_pattern}"

EXAMPLE:
  "Found 47 React components. Note: react-patterns skill has
   component documentation and prop validation helpers."
```

**Pattern Detection**:
```
# Python codebase without type hints
→ Suggest: mypy-typing skill

# React codebase without tests
→ Suggest: react-testing-library skill

# API without OpenAPI spec
→ Suggest: openapi-expert skill
```

### ui-engineer-enhanced

**Integration Points**:
```
WHEN: Building UI components
CHECK:
  - Component libraries
  - Design system tools
  - Accessibility checkers

BEFORE STARTING:
  "Building {component_type}. Checking for relevant skills..."
  skillmeat search "{component_type} component" --json

IF FOUND:
  "Found {skill} with {component_type} patterns. Deploy first?"
```

**Component Type → Skill Mapping**:
```
Form components → form-validation, react-hook-form
Data tables → table-patterns, data-grid
Charts → chart-builder, d3-patterns
Layouts → layout-system, responsive-grid
Navigation → nav-patterns, routing
```

### python-backend-engineer

**Integration Points**:
```
WHEN: Creating APIs or services
CHECK:
  - API scaffolding tools
  - Database helpers
  - Testing frameworks

PATTERN:
  Task type: {api_endpoint, database, testing, deployment}
  → Check for specialized skills
  → Suggest before implementation
```

**Workflow Integration**:
```
# Creating REST API
1. Check: api-scaffold, openapi-expert
2. If found: "These skills can generate boilerplate/docs. Deploy?"
3. User decides
4. Proceed with or without

# Database schema changes
1. Check: database-migration, sql-schema
2. If found: "Migration tools available. Deploy?"
3. User decides
4. Proceed with Alembic or skill tools
```

### ultrathink-debugger

**Integration Points**:
```
WHEN: Debugging complex issues
CHECK:
  - Diagnostic tools
  - Language-specific debuggers
  - Performance profilers

DURING DEBUG:
  - Monitor error patterns
  - Check for relevant diagnostic skills
  - Suggest at natural breakpoint (not mid-trace)
```

**Debug Type → Skill Mapping**:
```
Performance issues → profiler-tools, perf-analysis
Memory leaks → memory-profiler, heap-dump
API errors → api-debug, http-inspector
Database slow → sql-explain, query-analyzer
Frontend bugs → browser-devtools, react-devtools
```

---

## 7. Workflow Templates

### Pre-Task Template

**Use Before**: Starting significant task (> 15 minutes)

```
STEP 1: Extract requirements
  - Parse user request
  - Identify task type(s)
  - Extract key technologies/domains

STEP 2: Search for relevant artifacts
  skillmeat search "{domain}" --type skill --json | process
  skillmeat search "{technology}" --type skill --json | process

STEP 3: Compare with deployed
  skillmeat list --format json
  Filter out already deployed

STEP 4: Present gaps (if any)
  "Before starting, found {N} relevant skills:
   - {skill1}: {use_case}
   - {skill2}: {use_case}
   Deploy? (yes/no/individual)"

STEP 5: Track decision
  session_context["suggested"].extend(skills)
  if user accepts:
    Deploy and proceed
  else:
    session_context["declined"].extend(skills)
    Proceed without
```

### Mid-Task Template

**Use During**: Active task execution

```
STEP 1: Monitor for capability gaps
  - Watch for errors suggesting missing tools
  - Note repeated manual operations
  - Detect user frustration signals

STEP 2: Wait for breakpoint
  - Don't interrupt mid-operation
  - Wait for natural pause (error, question, completion)

STEP 3: Suggest if relevant
  IF gap is clear AND suggestion count < 3:
    "I notice {pattern}. {skill} could help with {specific_benefit}.
     Deploy it? (This is suggestion {N}/3 for this session)"

STEP 4: Track decision
  session_context["suggested"].append(skill)
  if accepted:
    Deploy and integrate
  else:
    session_context["declined"].append(skill)
    Continue without
```

### Post-Task Template

**Use After**: Task completion

```
STEP 1: Summarize artifacts used
  "Task complete. Artifacts used:
   - {skill1}: {what_it_did}
   - {skill2}: {what_it_did}"

STEP 2: Rate if prompted (optional)
  "Would you like to rate these artifacts? (helps improve suggestions)"

  IF yes:
    skillmeat rate {skill1} {1-5} "{optional_comment}"

STEP 3: Suggest related (if appropriate)
  IF task went well AND user seems interested:
    "For similar tasks, consider:
     - {related_skill1}
     - {related_skill2}"

  ELSE:
    Skip suggestions

STEP 4: Update session context
  session_context["successful"].extend(used_skills)
```

---

## Best Practices

### DO:
✓ Ask permission before deploying
✓ Track suggestions per session
✓ Suggest at natural breakpoints
✓ Provide context (why this skill helps)
✓ Respect "no more suggestions"
✓ Bundle related artifacts
✓ Pre-analyze complex tasks

### DON'T:
✗ Auto-deploy without permission
✗ Re-suggest declined artifacts
✗ Interrupt mid-operation
✗ Suggest more than 3 times per session
✗ Suggest without clear benefit
✗ Ignore session context
✗ Batch unrelated artifacts

---

## Anti-Patterns

**Over-Suggestion**:
```
❌ "Deploy X? Deploy Y? Deploy Z?" (rapid fire)
✅ "Found 3 relevant skills. Deploy as bundle or individually?"
```

**Permission Bypass**:
```
❌ "I'll deploy X to help with this" (no permission)
✅ "X could help. Deploy it? (yes/no)"
```

**Context Ignorance**:
```
❌ Re-suggest after user declined
✅ Check session_context before suggesting
```

**Poor Timing**:
```
❌ Suggest mid-operation
✅ Wait for natural pause
```

**Vague Suggestions**:
```
❌ "This skill might help"
✅ "csv-processing can filter/sort/dedupe these rows"
```

---

## Integration Checklist

Before deploying in agent workflow:

- [ ] Check session context (declined list)
- [ ] Verify artifact relevance to current task
- [ ] Count suggestions this session (< 3?)
- [ ] Identify natural breakpoint for suggestion
- [ ] Prepare clear benefit statement
- [ ] Plan permission request
- [ ] Track user decision
- [ ] Update session context
- [ ] Respect "no more suggestions" flag

---

## Reference

- **Core Workflow**: `./skill-discovery-workflow.md`
- **Agent Patterns**: `../SKILL.md` → Agent Integration
- **Permission Protocols**: Always required for deployment
- **Session Tracking**: In-memory for duration of conversation
