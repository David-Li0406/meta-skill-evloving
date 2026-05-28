# M2 Ink Language Validation Review

This document captures findings from a comprehensive review of all M2 AI-assisted branching design documents to validate that the proposed architecture is compatible with Ink's capabilities and uses Ink terminology consistently.

## Executive Summary

**Overall Assessment**: The M2 architecture is **compatible with Ink** and makes reasonable design choices. However, there are terminology inconsistencies and several places where Ink-specific implementation details should be clarified.

**Key Findings**:
1. **Terminology inconsistencies**: "scene" vs "knot" used interchangeably in some places
2. **Ink-compatible design**: The branch injection model works well with Ink's runtime
3. **Good practices found**: `ink_syntax_validation` rule properly validates with InkJS parser
4. **Missing details**: Some implementation notes should clarify Ink-specific behaviors

---

## 1. Ink Terminology Reference

For clarity, here is the standard Ink terminology that should be used consistently:

| Ink Term | Description | Example |
|----------|-------------|---------|
| **Knot** | Major story section | `=== knot_name ===` |
| **Stitch** | Subsection within a knot | `= stitch_name` |
| **Choice** | Player decision point | `* [Choice text] -> target` or `+ [Sticky choice]` |
| **Divert** | Navigation to another location | `-> knot_name` or `-> knot.stitch` |
| **Variable** | Story state | `VAR health = 100` |
| **Tag** | Metadata attached to content | `# tag_name` |
| **Tunnel** | Subroutine-style call/return | `-> tunnel ->` |
| **Thread** | Parallel content execution | `<- thread_knot` |
| **External function** | Host-game integration | `EXTERNAL function_name(arg)` |
| **Gather** | Collecting after choices | `- gathered content` |

---

## 2. Terminology Inconsistencies Found

### 2.1 "Scene" vs "Knot" Usage

**Issue**: Documents use "scene" and "knot" somewhat interchangeably. While "scene" is a valid game design term, when referring to Ink story structure, "knot" should be preferred for precision.

**Files affected**:
- `branch-proposal.json` - `current_scene` field
- `schema-docs.md` - references "current scene/knot"
- `telemetry-schema.md` - `current_scene` in event context
- `runtime-hooks.md` - uses "scene" consistently (acceptable for game-level concept)

**Recommendation**: 
- Keep `current_scene` in schemas (it represents game state, not Ink structure)
- Add documentation clarifying the mapping: `current_scene` = game-level scene identifier, which maps to an Ink knot/stitch path
- When discussing Ink-specific structure, use "knot" and "stitch"

**Examples of good usage**:
```
schema-docs.md line 104: "The current scene/knot in Ink script (e.g., `chapter_2.encounter_with_guard`)"
```

**Examples needing clarification**:
```
telemetry-schema.md line 39: "current_scene": "act2.campfire"
```
Should clarify: this is the Ink knot path (e.g., `act2.campfire` = `=== act2 === = campfire`)

### 2.2 "Dialogue Node" Terminology

**Issue**: Some documents reference "dialogue node" or "dialogue_node_not_found" errors, which isn't standard Ink terminology.

**Files affected**:
- `telemetry-schema.md` line 428: `"error_type": "dialogue_node_not_found"`
- `runtime-hooks.md` - refers to "dialogue node" in error handling

**Recommendation**: Clarify that "dialogue node" means an Ink knot, stitch, or choice that the branch content references. The error should be:
- `"error_type": "ink_knot_not_found"` or `"ink_divert_target_missing"`

### 2.3 "Return Path" Mapping to Ink

**Issue**: The `return_path` field is well-designed, but documentation should clarify how it maps to Ink diverts.

**Current usage** (correct):
```json
"return_path": "main_story.act2.campfire_next_morning"
```

**Ink equivalent**:
```ink
-> main_story.act2.campfire_next_morning
```

**Recommendation**: Add a note in `schema-docs.md` explaining that `return_path` must be a valid Ink divert target (knot or knot.stitch path).

---

## 3. Ink Compatibility Validation

### 3.1 Branch Type Mappings

The schema defines three branch types. Here's how they map to Ink:

| Branch Type | Ink Equivalent | Validation Notes |
|-------------|----------------|------------------|
| `ink_fragment` | Inline content (no choice points) | Must be valid Ink prose; cannot contain knot/stitch headers |
| `narrative_delta` | Non-Ink prose for narration | No Ink parsing needed; displayed as-is |
| `ink_knot` | Full knot with choices | Must parse as valid Ink; choices must have valid divert targets |

**Assessment**: This mapping is sound and covers the primary use cases.

### 3.2 Ink Syntax Validation Rule

The `policy-ruleset.md` includes an `ink_syntax_validation` rule:

```javascript
const inkParser = new inkjs.Compiler();
try {
    const parsedStory = inkParser.Compile(proposalContent);
    return { result: 'pass' };
} catch (parseError) {
    return { result: 'fail', message: parseError.message };
}
```

**Assessment**: This is correct for full Ink stories/knots. For `ink_fragment` type, the validation should wrap the content appropriately:

```javascript
// For ink_fragment, wrap in a test knot before parsing
if (branchType === 'ink_fragment') {
    contentToValidate = `=== test_knot ===\n${proposalContent}\n-> END`;
}
```

**Recommendation**: Update `policy-ruleset.md` to show fragment wrapping for validation.

### 3.3 Return Path Validation

The return path validation in `policy-ruleset.md`:

```javascript
const allKnots = story_script.all_knots();  // Get all knot names
const targetKnot = proposal.return_path.split('.')[0];  // Extract knot from path
```

**Assessment**: Correct approach. Ink's InkJS runtime provides methods to enumerate knots.

**Enhancement**: Should also validate stitch paths:
```javascript
// For paths like "act2.campfire", verify both knot and stitch exist
const [knot, stitch] = proposal.return_path.split('.');
if (stitch) {
    const stitchesInKnot = story_script.stitches_for_knot(knot);
    if (!stitchesInKnot.includes(stitch)) {
        return { result: 'fail', message: `Stitch '${stitch}' not found in knot '${knot}'` };
    }
}
```

### 3.4 Branch Injection Model

The runtime integration model (inject at hook points, divert to branch, divert back to return path) is fully compatible with Ink:

```ink
=== main_story ===
= encounter_with_guard
// Hook point: Director decides to inject branch here
{branch_available: -> ai_branch_001}
The guard eyes you suspiciously.
-> continue

=== ai_branch_001 ===
// AI-generated branch content
The guard's hand instinctively moved toward his sword hilt...
* [Confront him] -> ai_branch_001.confront
* [Back away] -> ai_branch_001.retreat

= confront
You stand your ground.
-> main_story.guard_reveals_knowledge  // Return path

= retreat
You take a step back.
-> main_story.after_confrontation  // Alternative return path
```

**Assessment**: This model works well with Ink. The conditional divert `{branch_available: -> ai_branch_001}` or similar patterns can gate branch injection.

### 3.5 Runtime Content Generation

The two-phase content generation model (pre-validated structure + runtime dialogue) has implications for Ink:

**Phase 1 (Detail stage)**: Generate Save-the-Cat structure with beat outlines
**Phase 2 (Runtime)**: Generate actual Ink dialogue dynamically

**Ink considerations**:
- Dynamic content can be injected via external functions or variable interpolation
- Fresh dialogue per playthrough requires storing generated text in Ink variables or using external function callbacks

**Example pattern**:
```ink
EXTERNAL get_ai_dialogue(beat_id)

=== ai_branch ===
{get_ai_dialogue("opening")}  // Calls runtime to get generated content
* [{get_ai_dialogue("choice_1")}] -> choice_1_result
* [{get_ai_dialogue("choice_2")}] -> choice_2_result
```

**Recommendation**: Add an implementation note to `proposal-lifecycle.md` explaining this pattern.

---

## 4. Good Practices Found

### 4.1 Ink Tags Usage

The schema correctly includes `ink_tags` field:
```json
"ink_tags": ["dialogue", "tension", "character_interaction"]
```

This aligns with Ink's tag system (`# tag_name`) for metadata.

### 4.2 Example Proposals

The example proposals in `examples/` correctly use Ink syntax:

**example_04_temple_spirit.json**:
```ink
=== temple_spirit_awakens ===
The altar pulsed with sickly blue light...
* [Claim the compass is destiny] -> temple_spirit_accepts
* [Ask who your ancestor was] -> temple_spirit_explains
* [Try to flee] -> temple_spirit_blocks
```

This is valid Ink syntax with proper knot header, prose, and choices with diverts.

### 4.3 Return Path Confidence

Including `return_path_confidence` alongside `return_path` is good design. It allows the Director to assess whether the AI Writer is confident in its divert target.

---

## 5. Missing Ink-Specific Details

### 5.1 Variable State Management

**Issue**: Documents don't explicitly address how AI-generated branches interact with Ink variables.

**Concern**: If a branch modifies Ink variables (`VAR player_reputation = "hero"`), and the branch is rolled back, the variables must also be reset.

**Recommendation**: Add to `runtime-hooks.md`:
```
### Ink Variable Rollback

When rolling back a branch, the runtime must:
1. Capture all Ink variables (via `story.variablesState`) before integration
2. Restore Ink variables from snapshot if rollback occurs
3. Variables modified by the branch are undone automatically
```

### 5.2 Thread/Tunnel Usage

**Issue**: Documents don't mention Ink threads (`<- thread`) or tunnels (`-> tunnel ->`).

**Assessment**: This is acceptable for M2 MVP. Threads and tunnels add complexity and are not required for basic branch injection.

**Recommendation**: Add a note to `proposal-lifecycle.md`:
```
**Out of Scope (M2)**: Branch proposals should not use Ink threads (`<-`) or tunnels 
(`-> tunnel ->`). These advanced features may be considered in future phases.
```

### 5.3 External Functions

**Issue**: If runtime dialogue generation uses Ink external functions, this must be documented.

**Recommendation**: Add to `runtime-hooks.md`:
```
### Ink External Function Integration

AI-generated branches may use external functions for dynamic content:

```javascript
// Register external function before running story
story.BindExternalFunction("get_ai_dialogue", (beatId) => {
    return aiWriter.generateDialogue(beatId, currentLore);
});
```

This enables fresh dialogue generation on each playthrough while maintaining
the pre-validated branch structure.
```

### 5.4 Choice Handling Details

**Issue**: The choice presentation model should clarify sticky vs non-sticky choices.

**Ink behavior**:
- `* [Choice]` - non-sticky (disappears after selection)
- `+ [Choice]` - sticky (remains available)

**Recommendation**: Add to `writer-prompts.md`:
```
### Ink Choice Guidelines

- Use `* [Choice text]` for standard one-time choices
- Use `+ [Choice text]` only for repeatable options (e.g., "Ask another question")
- Every choice must have a valid divert target (`-> knot` or `-> knot.stitch`)
- Fallback choices should divert to the return path
```

---

## 6. Recommendations Summary

### High Priority (Should fix before Phase 1)

1. **Add Ink terminology clarification** to `schema-docs.md`:
   - Clarify that `current_scene` maps to an Ink knot/stitch path
   - Explain `return_path` must be a valid Ink divert target

2. **Update `ink_syntax_validation` rule** in `policy-ruleset.md`:
   - Show fragment wrapping for `ink_fragment` type validation
   - Add stitch-level validation for return paths

3. **Document Ink variable rollback** in `runtime-hooks.md`:
   - Explain how Ink `variablesState` is captured/restored

### Medium Priority (Should address in Phase 1-2)

4. **Add external function integration notes** to `runtime-hooks.md`

5. **Document out-of-scope Ink features** (threads, tunnels) in `proposal-lifecycle.md`

6. **Update error type terminology**:
   - Change `dialogue_node_not_found` to `ink_divert_target_missing` in telemetry schema

### Low Priority (Nice to have)

7. **Standardize on "knot" terminology** when discussing Ink-specific structure

8. **Add Ink choice guidelines** (sticky vs non-sticky) to `writer-prompts.md`

---

## 7. Conclusion

The M2 AI-assisted branching architecture is **well-designed for Ink compatibility**. The branch injection model, return path validation, and Ink syntax checking are all appropriate for the Ink runtime.

The main areas for improvement are:
1. Terminology consistency (scene vs knot)
2. Explicit documentation of Ink-specific implementation details
3. Variable state management during rollback

These are documentation improvements, not fundamental design changes. The architecture is sound.

---

**Status**: Review complete. Recommendations ready for implementation.
**Reviewer**: AI Agent
**Date**: 2026-01-16
