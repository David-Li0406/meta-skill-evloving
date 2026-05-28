---
name: speckit-specify
description: Use this skill when you need to create or update a feature specification from a natural language feature description.
---

# Skill body

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Memory Integration

### Before Starting
Search for related prior work:
```bash
./scripts/memory-search "{feature keywords}"
```
Look for existing patterns, prior decisions, and related features to inform scope and avoid contradicting prior decisions.

### After Completion
Save key requirements captured:
```bash
./scripts/memory-save --decisions "Key requirements for {feature}: {summary}" --issues ""
```

## Constitution Alignment

This skill aligns with project principles:
- **User-Focused**: Specifications focus on WHAT users need, not HOW to implement.
- **Testable Requirements**: Every requirement must be verifiable.
- **Clear Boundaries**: Explicit scope and out-of-scope declarations.

## Integration Considerations (REQUIRED)

When specifying a feature, you MUST document integration points to prevent isolated implementations that don't connect to the system.

**Add to spec.md under "Scope" section:**

1. **Entry Points**: How will users access this feature?
   - CLI command? → Which command group?
   - Plugin? → Which plugin type?
   - API? → Which endpoint?

2. **Dependencies**: What existing components does this feature need?
   - Which packages? (e.g., floe-core, floe-dagster)
   - Which plugins? (e.g., ComputePlugin, CatalogPlugin)
   - Which services? (e.g., Polaris, S3)

3. **Outputs**: What does this feature produce that others consume?
   - New schemas? → Add to CompiledArtifacts.
   - New plugins? → Register entry points.
   - New APIs? → Document contracts.

**If integration is unclear**: Ask during `/speckit.clarify` before planning begins.

## Workflow

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords.
   - Create a short name that captures the essence of the feature in action-noun format (e.g., "add-user-auth").
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.).

2. **Check for existing branches before creating a new one**:
   a. Fetch all remote branches:
   ```bash
   git fetch --all --prune
   ```

   b. Find the highest feature number across all sources for the short name:
   - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
   - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
   - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`.

   c. Determine the next available number:
   - Extract all numbers from all three sources.
   - Find the highest number N and use N+1 for the new branch number.

   d. Run the script to create the new feature:
   ```bash
   .specify/scripts/bash/create-new-feature.sh --json "<feature description>" --number N+1 --short-name "<your-short-name>"
   ```

## Example

If the user wants to add user authentication, the feature description might be: "I want to add user authentication." The generated short name would be "user-auth", and the script would be executed accordingly.