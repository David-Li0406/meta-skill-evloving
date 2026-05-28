# Issue Criteria Reference

Detailed criteria for identifying issues in different document types.

## Issue Type Enumeration

Formal list of valid `type` values for issue objects. All issue-finder output and codex-validator input/output must use these types.

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `vague_instruction` | Instruction lacks specificity, reader must guess | Major | No |
| `ambiguous_scope` | Could mean multiple things, unclear boundaries | Major | No |
| `unresolved_todo` | TODO/TBD/FIXME/??? placeholder remaining | Major | No |
| `inconsistent_terminology` | Same concept, different names throughout | Major | Conditional (>70% → auto, else ask) |
| `broken_reference` | Link to non-existent target (section, file) | Critical | Sometimes (if target found elsewhere) |
| `redundant_content` | Same information repeated unnecessarily | Major | Yes |
| `formatting_inconsistency` | Mixed styles (bullets, headings, etc.) | Minor | Yes |
| `missing_definition` | Term used but never defined | Critical | No |
| `contradiction` | Two statements that conflict | Critical | No |
| `trailing_whitespace` | Extra spaces, unnecessary blank lines | Minor | Yes |
| `incomplete_list` | Single-item list that should be prose | Minor | Yes |
| `missing_context` | Assumes knowledge not provided | Major | No |

### Usage Notes

- **issue-finder** must set `type` field using values from this enum
- **codex-validator** must validate that incoming issues have valid types
- **SKILL.md Phase 3** switches on `type` to determine prompt strategy
- Unknown types should be logged and treated as `auto_fixable: false`

## Universal Issues (All File Types)

### Critical Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Contradiction | Two statements that conflict | "Always use X" then later "Never use X" | No |
| Broken reference | Links to non-existent target | `[see above](#nonexistent)` | Sometimes |
| Missing definition | Term used but never defined | "Configure the FrobNozzle" (never explained) | No |

### Major Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Inconsistent terminology | Same concept, different names | "user" vs "customer" vs "client" | Yes |
| Vague instruction | Reader must guess intent | "Handle errors appropriately" | No |
| Unresolved placeholder | TODO/TBD/??? remaining | "TODO: add details" | No |
| Redundant content | Same info repeated | Paragraph A says same as paragraph B | Yes |
| Ambiguous scope | Could mean multiple things | "Update the configuration" (which one?) | No |

### Minor Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Formatting inconsistency | Mixed styles | Bullets: `-`, `*`, `•` mixed | Yes |
| Single-item list | List with one item | `- Only item` | Yes |
| Trailing whitespace | Extra spaces | Lines ending with spaces | Yes |
| Inconsistent casing | Mixed case for same term | "API" vs "Api" vs "api" | Yes |

## File-Type Specific Criteria

### Markdown Documents

| Issue | Criteria | Severity |
|-------|----------|----------|
| Heading skip | h1 → h3 (skipped h2) | Minor |
| Orphan heading | Heading with no content below | Major |
| Dead link | Internal link to missing section | Critical |
| Unclosed formatting | `**bold without close` | Critical |
| Mixed list markers | `-` and `*` in same list | Minor |
| Code block no language | ``` without language tag | Minor |

### Implementation Plans

| Issue | Criteria | Severity |
|-------|----------|----------|
| Missing verification | Task has no `<verify>` | Critical |
| Missing done criteria | Task has no `<done>` | Critical |
| Vague action | Action is not specific | Major |
| Undefined dependency | Depends on unspecified thing | Major |
| Missing files list | No `<files>` for task | Major |
| Unmeasurable success | Success criteria not testable | Major |

### Configuration Files (YAML/JSON)

| Issue | Criteria | Severity |
|-------|----------|----------|
| Duplicate keys | Same key appears twice | Critical |
| Type mismatch | String where number expected | Critical |
| Missing required field | Schema requires field | Critical |
| Unused variable | Defined but never referenced | Minor |
| Inconsistent indentation | Mixed 2-space and 4-space | Minor |
| No default value | Optional field with no default | Minor |

### Code Files

| Issue | Criteria | Severity |
|-------|----------|----------|
| Naming inconsistency | camelCase and snake_case mixed | Major |
| Stale comment | Comment doesn't match code | Major |
| TODO/FIXME | Unresolved markers | Major |
| Dead code | Unreachable or unused | Minor |
| Missing type | No type annotation where expected | Minor |
| Magic number | Unexplained numeric literal | Minor |

## Mode Adjustments

### Default Mode

**Flag**: All Critical, all Major
**Auto-fix**: Formatting, clear inconsistencies
**Ask user**: Vague content, ambiguities, TODOs

### Aggressive Mode

**Flag**: All Critical, all Major, all Minor
**Auto-fix**: Everything possible
**Additional actions**:
- Remove verbose explanations
- Tighten prose
- Eliminate redundancy aggressively
- Suggest restructuring

### Conservative Mode

**Flag**: Critical + Ambiguities requiring user input
**Auto-fix**: Only clear errors (no subjective improvements)
**Preserve**:
- Author's style choices
- Verbose explanations (may be intentional)
- Structural decisions
- Minor formatting differences

**Note**: Conservative mode still flags vague instructions, unclear scope, and TODOs because these need user resolution. It just skips minor formatting issues.

## Detection Patterns

### Vague Instructions

Look for:
- "appropriately", "properly", "correctly"
- "as needed", "if necessary", "when required"
- "handle", "manage", "process" without specifics
- "etc.", "and so on", "and more"
- Passive voice without actor: "should be validated"

### Inconsistent Terminology

Check for:
- Same concept: user/customer/client, app/application, config/configuration
- Abbreviations: API/api, URL/url, DB/database
- British/American: colour/color, behaviour/behavior
- Pluralization: data is/data are

### Redundant Content

Patterns:
- Two paragraphs saying the same thing differently
- Bullet point that restates the heading
- "In other words..." followed by repetition
- Summary that just repeats previous sections

### Ambiguous Scope

Signals:
- "the configuration" (which one?)
- "update the file" (which file?)
- "this should work" (what conditions?)
- Pronouns with unclear antecedents
