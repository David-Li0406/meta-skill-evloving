# Test ContextGraph Skill - Findings

## Purpose
This test skill was created to validate the end-to-end flow of skill file loading in Claude Code agents.

## Key Findings

### 1. Skill Directory Structure
Skills must be placed in: `.claude/skills/<skill-name>/SKILL.md`

**Example:**
```
.claude/skills/test-contextgraph-skill/SKILL.md
```

### 2. SKILL.md Format
Skills use YAML frontmatter followed by markdown content:

```yaml
---
name: skill-name
description: Brief description of what this skill does
---

# Skill Name

Instructions for Claude...
```

### 3. Skill Loading Behavior
- **Skills are loaded at agent startup**, not dynamically during execution
- The SDK init message (type: 'system', subtype: 'init') includes a `skills: []` array
- Skills appear in this array when the agent initializes
- Skills cannot be added or invoked after the agent has started

**Evidence:** See `__tests__/claude-sdk.test.ts` line 102:
```typescript
function createInitMessage(sessionId: string): SDKSystemMessage {
  return {
    type: 'system',
    subtype: 'init',
    skills: [],  // Skills loaded at startup appear here
    // ... other fields
  };
}
```

### 4. Skill Invocation
- Skills are invoked using the `Skill` tool with the skill name
- Example: `Skill({ skill: "test-contextgraph-skill" })`
- If a skill is not in the loaded skills array, the tool returns an error: `Unknown skill: skill-name`

### 5. Testing Skill Loading
To verify a skill is loaded:
1. Create the skill file in `.claude/skills/<skill-name>/SKILL.md`
2. Start a new agent session
3. Check the SDK init message `skills` array
4. Attempt to invoke the skill using the `Skill` tool

### 6. Prototype Validation Results

**What we validated:**
- ✅ Skills can be written to `.claude/skills/` directory
- ✅ File naming convention: `<skill-name>/SKILL.md`
- ✅ YAML frontmatter format is correct
- ✅ Skills are loaded at agent startup (not during execution)
- ✅ SDK exposes loaded skills via init message

**What we learned:**
- Skills must be present before the agent starts
- For the contextgraph/agent system, this means:
  - Skill files must be written to the temp directory **before** launching Claude Code
  - Skills cannot be hot-reloaded during execution
  - Skill sync must happen during agent setup phase

## Next Steps for Integration

For the full skill injection system:

1. **Timing**: Write skills to `.claude/skills/` in the temp directory BEFORE starting Claude Code
2. **API Integration**: Fetch skills from the ContextGraph API during agent setup
3. **File Writing**: Each skill becomes a directory with a SKILL.md file
4. **Verification**: Log the skills array from the SDK init message to confirm loading
5. **Error Handling**: Agent should proceed even if skill sync fails (graceful degradation)

## Repository Context
- **Repository**: https://github.com/contextgraph/agent
- **Branch**: main
- **Action ID**: 22698e45-6dcb-469e-9919-bb81a21f761e
