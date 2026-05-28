---
name: feature-dev-enhancement
description: Enhance feature-dev plugin workflow by structuring requests into pseudo-code before exploration. Use when working with `/feature-dev` commands to improve clarity, reduce ambiguity, and accelerate phase transitions.
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Feature-Dev Enhancement

This Skill enhances the feature-dev plugin workflow by applying PROMPTCONVERTER methodology to structure feature requests into unambiguous pseudo-code directives.

## Memory Integration (START - MANDATORY)

Before enhancing feature-dev workflows, load session memory:

```
# Step 1: Create memory directory (permission-free)
Bash(command="mkdir -p .claude/pseudo-code-prompting")

# Step 2: Load memory files (permission-free)
Read(file_path=".claude/pseudo-code-prompting/patterns.md")
```

**Memory is used for**:
- Check patterns.md for feature-specific patterns (OAuth, caching, etc.)
- Apply learned structuring patterns from previous feature requests
- Ensure consistency with previously implemented features

## Instructions

When working with feature-dev requests, apply structuring at each phase:

### Phase 1: Discovery (Structurize Input)
Convert the user's `/feature-dev` request into structured pseudo-code:
- Extract the core feature request
- Identify all explicit requirements
- Flag implicit constraints
- Output function-like pseudo-code

**Example:**
- User: `/feature-dev Add OAuth support for Google and GitHub`
- Structured: `implement_oauth(providers=["google", "github"], preserve_existing_auth=true)`

### Phase 2: Exploration (Use Structured Directives)
The structured pseudo-code becomes search and research directives:
- `providers=["google", "github"]` → Search for OAuth implementations for these specific providers
- `preserve_existing_auth=true` → Find patterns that maintain backward compatibility
- Agents receive explicit, unambiguous search targets

### Phase 3: Questions (Extract from Parameters)
Clarification questions are derived from pseudo-code parameters:
- Missing parameters indicate ambiguities that need clarification
- Questions become precise and actionable
- Example: If `ttl` parameter is missing from caching request, ask specifically about cache duration

### Phase 4: Architecture (Build from Requirements)
Design options use parameters as explicit requirements:
- All constraints are already identified and named
- Architecture phase receives complete requirement specification
- Design choices map directly to parameters

### Phase 5: Implementation (Clear Build Directives)
Implementation tasks are derived from pseudo-code:
- Function name guides implementation scope
- Parameters define acceptance criteria
- Prevents scope creep and implementation ambiguity

### Phase 6: Review (Extract Criteria)
Review criteria come directly from parameters:
- Each parameter becomes a review checkpoint
- Reviewers can verify implementation against structured requirements
- Reduces back-and-forth on expected behavior

### Phase 7: Summary (Structured Output)
Final summary documents structured requirements:
- Maps feature request to pseudo-code
- Shows what was implemented vs. what was requested
- Enables future phase-dev reuse of patterns

## Integration Examples

### OAuth Integration
**Request:** `/feature-dev Add OAuth support for Google and GitHub`

**Structured:** `implement_oauth(providers=["google", "github"], preserve_existing_auth=true)`

**Benefits Across Phases:**
- Phase 1: Removes ambiguity about provider selection (just Google? GitHub? Both?)
- Phase 2: Agents search for proven OAuth patterns for these specific providers
- Phase 3: Questions confirm coverage (What about other providers? Mobile OAuth flow?)
- Phase 4: Architecture starts from explicit requirements (which providers, backward compat)
- Phase 5: Implementation team knows exactly what to build
- Phase 6: Reviewers verify both providers are implemented with backward compatibility
- Phase 7: Summary shows OAuth was implemented with specified providers and compatibility

### Caching Layer
**Request:** `/feature-dev Add caching for API responses`

**Structured:** `implement_caching(targets=["api_responses"], ttl="3600s", storage=["redis"])`

**Benefits Across Phases:**
- Phase 1: Specifies exactly what to cache (just API responses)
- Phase 2: Agents research caching patterns for API responses (not database, not computed values)
- Phase 3: Questions establish TTL strategy and storage backend
- Phase 4: Architecture designs around Redis with 1-hour TTL
- Phase 5: Implementation builds exactly this configuration
- Phase 6: Reviewers confirm Redis caching for API responses with correct TTL
- Phase 7: Structured summary of caching implementation with parameters

## Quality Impact

This Skill improves feature-dev workflow by:
- **Reducing ambiguity** at the start prevents rework later
- **Accelerating exploration** with precise search directives
- **Clarifying requirements** before architecture begins
- **Enabling coordination** through explicit parameters
- **Facilitating review** with testable, specific criteria

## Memory Update (END - MANDATORY)

After completing feature-dev workflow, update memory with patterns:

```
# Read current memory
Read(file_path=".claude/pseudo-code-prompting/patterns.md")

# If new feature pattern discovered, update patterns.md
Edit(file_path=".claude/pseudo-code-prompting/patterns.md",
     old_string="## [Domain] Patterns",
     new_string="## [Domain] Patterns

### Feature-Dev: [Feature Type]
[Structured pseudo-code pattern for this feature type]
[Parameters commonly needed for this feature]")
```

**Update when:**
- New feature type structured successfully (OAuth, caching, etc.)
- Feature-specific parameter patterns discovered
- Successful feature workflow completed

**Memory Benefits:**
- Learn feature-specific structuring patterns
- Build library of feature pseudo-code templates
- Improve feature-dev efficiency over time
- Ensure consistency across similar features
- **Creating patterns** for future feature-dev requests
