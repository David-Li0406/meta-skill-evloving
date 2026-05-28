---
name: research
description: Comprehensive research for projects and phases, covering domain ecosystems, implementation strategies, and quality improvement to avoid common pitfalls
argument-hint: "[project|phase <number>]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
  - mcp__context7__*
---

<objective>
Comprehensive research at project and phase levels to inform planning and avoid common pitfalls.

For project-level research: Analyze domain ecosystem before creating roadmap. Answers questions for quality roadmaps:
- What's the standard stack for this type of product?
- What features do users expect?
- How are these systems typically structured?
- What do projects in this domain commonly get wrong?

For phase-level research: Research how to implement a phase before planning, for niche/complex domains where knowledge is sparse. Discovers:
- What libraries exist for this problem
- What architecture patterns experts use
- What the standard stack looks like
- What problems people commonly hit
- What NOT to hand-roll (use existing solutions)

Includes strategies to avoid common research mistakes and ensure quality improvement.

Output: For projects - .planning/research/ folder with ecosystem knowledge; For phases - RESEARCH.md with actionable ecosystem knowledge.

Run after /ag4:new-project for projects, or when planning complex phases.
</objective>

<execution_context>
@~/.claude/ag4one/references/principles.md
@~/.claude/ag4one/workflows/research-project.md
@~/.claude/ag4one/templates/research-project/SUMMARY.md
@~/.claude/ag4one/templates/research-project/STACK.md
@~/.claude/ag4one/templates/research-project/FEATURES.md
@~/.claude/ag4one/templates/research-project/ARCHITECTURE.md
@~/.claude/ag4one/templates/research-project/PITFALLS.md
@~/.claude/ag4one/workflows/research-phase.md
@~/.claude/ag4one/templates/research.md
@~/.claude/ag4one/references/research-pitfalls.md
</execution_context>

<context>
Argument: $ARGUMENTS (optional - "project" or "phase <number>")

If "project" or no argument:
@.planning/PROJECT.md
@.planning/config.json (if exists)

If "phase <number>":
Phase number: <number>

**Load project state:**
@.planning/STATE.md

**Load roadmap:**
@.planning/ROADMAP.md

**Load requirements:**
@.planning/REQUIREMENTS.md

Extract phase requirements:
1. Find the phase in ROADMAP.md, get its `Requirements:` list
2. Look up each REQ-ID in REQUIREMENTS.md for full description
3. Use concrete requirements to focus research domains

**Load phase context if exists:**
Check for `.planning/phases/XX-name/{phase}-CONTEXT.md` - bonus context from discuss-phase.
</context>

<process>

<step name="validate">
Determine research type:
- If argument starts with "phase", extract phase number
- Else, assume project research

```bash
# For project research
if [ "$ARGUMENTS" != "phase "* ]; then
  # Verify project exists
  [ -f .planning/PROJECT.md ] || { echo "ERROR: No PROJECT.md found. Run /ag4:new-project first."; exit 1; }

  # Check if roadmap already exists
  [ -f .planning/ROADMAP.md ] && echo "WARNING: ROADMAP.md already exists. Research is typically done before roadmap creation."

  # Check if research already exists
  [ -d .planning/research ] && echo "RESEARCH_EXISTS" || echo "NO_RESEARCH"
fi

# For phase research
if [ "$ARGUMENTS" = "phase "* ]; then
  phase_num=$(echo $ARGUMENTS | cut -d' ' -f2)
  # Validate phase exists in roadmap
  # ... (similar to original)
fi
```
</step>

<step name="check_existing">
For project: If RESEARCH_EXISTS, use AskUserQuestion as in original.

For phase: Check if RESEARCH.md exists, offer to update or use existing.
</step>

<step name="execute_research">
If project: Follow research-project.md workflow - analyze PROJECT.md, identify questions, spawn agents, aggregate to .planning/research/

If phase: Follow research-phase.md workflow - analyze phase, identify gaps, research domains, execute via Context7/docs/WebSearch, cross-verify, create RESEARCH.md

In both cases, apply research-pitfalls verification:
- Verify all configuration scopes
- Specify exact sources
- Check for deprecated features
- Document tool variations
- Verify negative claims with official docs
- Enumerate all possibilities
- Cross-reference multiple sources
- Verify source completeness and currency
</step>

<step name="done">
For project:
```
Research complete:

- Summary: .planning/research/SUMMARY.md
- Stack: .planning/research/STACK.md
- Features: .planning/research/FEATURES.md
- Architecture: .planning/research/ARCHITECTURE.md
- Pitfalls: .planning/research/PITFALLS.md

---

## ▶ Next Up

**Define requirements** — scope your v1 from research findings

`/ag4:define-requirements`

<sub>`/clear` first → fresh context window</sub>

**Flow:** research → **define-requirements** → create-roadmap

---
```

For phase:
Research complete: RESEARCH.md created with ecosystem knowledge.

## ▶ Next Up

**Plan the phase** — create detailed implementation plan

`/ag4:plan-phase <number>`

**Flow:** research → **plan-phase**
</step>

</process>

<when_to_use>
**Use research for:**
- Greenfield projects in established domains (community, e-commerce, SaaS)
- When "what features should exist" is partially unknown
- Complex integrations requiring ecosystem knowledge
- Domains where best practices matter (auth, payments, real-time)
- Any project where you'd Google "how to build a [X]" before starting
- Implementing phases in niche/complex domains where Claude's knowledge is sparse
- When planning phases requiring specific libraries, patterns, or architectures
- Any situation where research pitfalls could compromise quality

**Skip research for:**
- Well-defined specs ("build exactly this API")
- Simple tools/utilities with clear scope
- Adding features to existing codebases with known patterns
- Domains you've built in many times before
- Straightforward phases with standard solutions
</when_to_use>

<success_criteria>
- [ ] Research type validated (project or phase)
- [ ] Domain/ecosystem identified from description
- [ ] Comprehensive research executed (Context7 + official docs + WebSearch where applicable)
- [ ] All WebSearch findings cross-verified with authoritative sources
- [ ] Research documents created (.planning/research/ or RESEARCH.md)
- [ ] Standard stack/libraries identified
- [ ] Architecture patterns documented
- [ ] Common pitfalls catalogued
- [ ] What NOT to hand-roll is clear
- [ ] Research pitfalls verification applied:
  - All enumerated items investigated
  - Negative claims verified with official docs
  - Multiple sources cross-referenced for critical claims
  - URLs provided for all official documentation
  - Publication dates checked (prefer recent/current)
  - Tool/environment-specific variations documented
  - Confidence levels assigned honestly
  - Assumptions distinguished from verified facts
- [ ] User knows next steps (define-requirements or plan-phase)
</success_criteria>

<reief_pitfalls_reference>
<purpose>
This section catalogs research mistakes discovered in production use, providing specific patterns to avoid and verification strategies to prevent recurrence.
</purpose>

<known_pitfalls>
[Include the known_pitfalls section from research-pitfalls]
</known_pitfalls>

<red_flags>
[Include the red_flags section]
</red_flags>

<continuous_improvement>
[Include the continuous_improvement section]
</continuous_improvement>

<quick_reference>
[Include the quick_reference section]
</quick_reference>
</brief_pitfalls_reference>

<known_pitfalls>

<pitfall_config_scope>
**What**: Assuming global configuration means no project-scoping exists
**Example**: Concluding "MCP servers are configured GLOBALLY only" while missing project-scoped `.mcp.json`
**Why it happens**: Not explicitly checking all known configuration patterns
**Prevention**:
```xml
<verification_checklist>
**CRITICAL**: Verify ALL configuration scopes:
□ User/global scope - System-wide configuration
□ Project scope - Project-level configuration files
□ Local scope - Project-specific user overrides
□ Workspace scope - IDE/tool workspace settings
□ Environment scope - Environment variables
</verification_checklist>
```
</pitfall_config_scope>

<pitfall_search_vagueness>
**What**: Asking researchers to "search for documentation" without specifying where
**Example**: "Research MCP documentation" → finds outdated community blog instead of official docs
**Why it happens**: Vague research instructions don't specify exact sources
**Prevention**:
```xml
<sources>
Official sources (use WebFetch):
- https://exact-url-to-official-docs
- https://exact-url-to-api-reference

Search queries (use WebSearch):
- "specific search query {current_year}"
- "another specific query {current_year}"
</sources>
```
</pitfall_search_vagueness>

<pitfall_deprecated_features>
**What**: Finding archived/old documentation and concluding feature doesn't exist
**Example**: Finding 2022 docs saying "feature not supported" when current version added it
**Why it happens**: Not checking multiple sources or recent updates
**Prevention**:
```xml
<verification_checklist>
□ Check current official documentation
□ Review changelog/release notes for recent updates
□ Verify version numbers and publication dates
□ Cross-reference multiple authoritative sources
</verification_checklist>
```
</pitfall_deprecated_features>

<pitfall_tool_variations>
**What**: Conflating capabilities across different tools/environments
**Example**: "Claude Desktop supports X" ≠ "Claude Code supports X"
**Why it happens**: Not explicitly checking each environment separately
**Prevention**:
```xml
<verification_checklist>
□ Claude Desktop capabilities
□ Claude Code capabilities
□ VS Code extension capabilities
□ API/SDK capabilities
Document which environment supports which features
</verification_checklist>
```
</pitfall_tool_variations>

<pitfall_negative_claims>
**What**: Making definitive "X is not possible" statements without official source verification
**Example**: "Folder-scoped MCP configuration is not supported" (missing `.mcp.json`)
**Why it happens**: Drawing conclusions from absence of evidence rather than evidence of absence
**Prevention**:
```xml
<critical_claims_audit>
For any "X is not possible" or "Y is the only way" statement:
- [ ] Is this verified by official documentation stating it explicitly?
- [ ] Have I checked for recent updates that might change this?
- [ ] Have I verified all possible approaches/mechanisms?
- [ ] Am I confusing "I didn't find it" with "it doesn't exist"?
</critical_claims_audit>
```
</pitfall_negative_claims>

<pitfall_missing_enumeration>
**What**: Investigating open-ended scope without enumerating known possibilities first
**Example**: "Research configuration options" instead of listing specific options to verify
**Why it happens**: Not creating explicit checklist of items to investigate
**Prevention**:
```xml
<verification_checklist>
Enumerate ALL known options FIRST:
□ Option 1: [specific item]
□ Option 2: [specific item]
□ Option 3: [specific item]
□ Check for additional unlisted options

For each option above, document:
- Existence (confirmed/not found/unclear)
- Official source URL
- Current status (active/deprecated/beta)
</verification_checklist>
```
</pitfall_missing_enumeration>

<pitfall_single_source>
**What**: Relying on a single source for critical claims
**Example**: Using only Stack Overflow answer from 2021 for current best practices
**Why it happens**: Not cross-referencing multiple authoritative sources
**Prevention**:
```xml
<source_verification>
For critical claims, require multiple sources:
- [ ] Official documentation (primary)
- [ ] Release notes/changelog (for currency)
- [ ] Additional authoritative source (for verification)
- [ ] Contradiction check (ensure sources agree)
</source_verification>
```
</pitfall_single_source>

<pitfall_assumed_completeness>
**What**: Assuming search results are complete and authoritative
**Example**: First Google result is outdated but assumed current
**Why it happens**: Not verifying publication dates and source authority
**Prevention**:
```xml
<source_verification>
For each source consulted:
- [ ] Publication/update date verified (prefer recent/current)
- [ ] Source authority confirmed (official docs, not blogs)
- [ ] Version relevance checked (matches current version)
- [ ] Multiple search queries tried (not just one)
</source_verification>
```
</pitfall_assumed_completeness>
</known_pitfalls>

<red_flags>

<red_flag_zero_not_found>
**Warning**: Every investigation succeeds perfectly
**Problem**: Real research encounters dead ends, ambiguity, and unknowns
**Action**: Expect honest reporting of limitations, contradictions, and gaps
</red_flag_zero_not_found>

<red_flag_no_confidence>
**Warning**: All findings presented as equally certain
**Problem**: Can't distinguish verified facts from educated guesses
**Action**: Require confidence levels (High/Medium/Low) for key findings
</red_flag_no_confidence>

<red_flag_missing_urls>
**Warning**: "According to documentation..." without specific URL
**Problem**: Can't verify claims or check for updates
**Action**: Require actual URLs for all official documentation claims
</red_flag_missing_urls>

<red_flag_no_evidence>
**Warning**: "X cannot do Y" or "Z is the only way" without citation
**Problem**: Strong claims require strong evidence
**Action**: Flag for verification against official sources
</red_flag_no_evidence>

<red_flag_incomplete_enum>
**Warning**: Verification checklist lists 4 items, output covers 2
**Problem**: Systematic gaps in coverage
**Action**: Ensure all enumerated items addressed or marked "not found"
</red_flag_incomplete_enum>
</red_flags>

<continuous_improvement>

When research gaps occur:

1. **Document the gap**
   - What was missed or incorrect?
   - What was the actual correct information?
   - What was the impact?

2. **Root cause analysis**
   - Why wasn't it caught?
   - Which verification step would have prevented it?
   - What pattern does this reveal?

3. **Update this document**
   - Add new pitfall entry
   - Update relevant checklists
   - Share lesson learned
</continuous_improvement>

<quick_reference>

Before submitting research, verify:

- [ ] All enumerated items investigated (not just some)
- [ ] Negative claims verified with official docs
- [ ] Multiple sources cross-referenced for critical claims
- [ ] URLs provided for all official documentation
- [ ] Publication dates checked (prefer recent/current)
- [ ] Tool/environment-specific variations documented
- [ ] Confidence levels assigned honestly
- [ ] Assumptions distinguished from verified facts
- [ ] "What might I have missed?" review completed

**Living Document**: Update after each significant research gap
**Lessons From**: MCP configuration research gap (missed `.mcp.json`)
</quick_reference>
