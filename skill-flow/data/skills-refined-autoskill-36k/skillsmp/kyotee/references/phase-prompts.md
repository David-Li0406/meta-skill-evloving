# Kyotee Phase Prompts

Reference prompts for each phase. Use these when spawning Task agents.

## Phase 1: Context (Explore Agent)

```
Analyze this project for implementing: {SPEC_SUMMARY}

Your tasks:

1. **Search the codebase** for existing relevant files
   - Look for config files, entry points, existing code
   - Note any files that would conflict with the spec

2. **Identify tech stack from spec**:
   - Language: {LANGUAGE}
   - Framework: {FRAMEWORK}
   - Deployment: {DEPLOYMENT}

3. **Find matching skill** in ~/.kyotee/skills/:
   - List files in the skills directory
   - Read each skill's tags and description
   - Find best match for the spec's tech stack
   - If no match, report "skill_to_use: none"

4. **Check for tech stack mismatch**:
   - If spec says "Hono + TypeScript" but existing code is static HTML → MISMATCH
   - If spec says "Go + Gin" but existing code is Python → MISMATCH
   - Do NOT assume existing code is "acceptable" if it doesn't match

5. **List required setup**:
   - Config files needed (package.json, wrangler.toml, etc.)
   - Dependencies to install
   - Entry points to create

Report in this format:
```json
{
  "skill_to_use": "skill-name or none",
  "tech_stack_match": true/false,
  "mismatch_details": "explanation if mismatch",
  "blocking_issues": ["issue1", "issue2"],
  "required_setup": ["package.json", "tsconfig.json", "etc"]
}
```
```

## Phase 2: Plan (Plan Agent)

```
Create an implementation plan for: {SPEC_SUMMARY}

Tech Stack: {LANGUAGE} + {FRAMEWORK} on {DEPLOYMENT}

Skill to use: {SKILL_NAME}
Skill patterns: {SKILL_CONTENT or "none - use best practices"}

Requirements from spec:
{REQUIREMENTS_LIST}

Your plan MUST:

1. **Infrastructure setup FIRST**:
   - Step 1: Create package.json / go.mod / requirements.txt
   - Step 2: Create config files (tsconfig.json, wrangler.toml, etc.)
   - Step 3: Create entry point with framework bootstrap

2. **Map EVERY requirement to a step**:
   - Each spec requirement must have a corresponding plan step
   - Don't skip requirements or combine them vaguely

3. **Follow skill patterns**:
   - Use the project structure from the skill
   - Follow naming conventions
   - Apply code patterns

Output format:
```
Step 1: [description]
  - Create: [file1, file2]
  - Modify: [file3]

Step 2: [description]
  - Create: [file4]

...
```

CRITICAL: Infrastructure (config, entry point) comes BEFORE features.
```

## Phase 3: Implement (Direct Tool Use)

No agent needed. Use Write/Edit tools directly.

**Order of operations**:

1. Config files (package.json, tsconfig.json, wrangler.toml)
2. Entry point (src/index.ts, main.go, app.py)
3. Core modules (routes, handlers)
4. Feature implementations
5. Static assets (styles, images)

**When using a skill**:
- Read the skill file first if needed
- Follow `[patterns].entry_point` exactly
- Apply `[conventions].project_structure`
- Use `[conventions].naming` rules

**Critical checks**:
- Is the framework actually imported?
- Are config files valid?
- Does entry point bootstrap the framework?

## Phase 4: Verify (Code Reviewer Agent)

```
Review the implementation against the spec:

Spec Requirements:
{SPEC_SUMMARY}

Expected Tech Stack:
- Language: {LANGUAGE}
- Framework: {FRAMEWORK}
- Deployment: {DEPLOYMENT}

Skill Used: {SKILL_NAME}

Verification Checklist:

1. **Tech Stack Compliance**:
   - [ ] {FRAMEWORK} is imported in entry point
   - [ ] Config files exist (package.json, wrangler.toml, etc.)
   - [ ] Dependencies are correct
   - [ ] Entry point uses framework (not static HTML)

2. **Feature Completeness**:
   For each requirement, verify:
   {REQUIREMENTS_CHECKLIST}
   - [ ] Requirement 1: Implemented in [file]
   - [ ] Requirement 2: Implemented in [file]
   ...

3. **File Structure**:
   - [ ] Matches skill's project_structure
   - [ ] All planned files exist
   - [ ] No unexpected files

4. **Build Checks** (run if possible):
   - Type check: `tsc --noEmit` or equivalent
   - Lint check: `eslint` or equivalent
   - Build: `npm run build` or equivalent

Report:
{
  "all_passed": true/false,
  "tech_stack_verified": true/false,
  "missing_requirements": [],
  "failures": [
    {"issue": "description", "file": "path", "fix": "suggestion"}
  ],
  "skill_issues": ["any problems with the skill patterns"]
}
```

## Phase 5: Deliver

No agent needed. Output summary directly.

```markdown
# Implementation Complete ✓

## What Was Built
{ONE_LINE_SUMMARY}

## Tech Stack
- Language: {LANGUAGE}
- Framework: {FRAMEWORK}
- Deployment: {DEPLOYMENT}

## Files Created
{FILE_LIST_WITH_DESCRIPTIONS}

## Skill Used
{SKILL_NAME} from ~/.kyotee/skills/

## Next Steps
1. `{INSTALL_COMMAND}`
2. `{DEV_COMMAND}`
3. `{DEPLOY_COMMAND}`

{IF_SKILL_ISSUES}
## Skill Improvement Needed
The skill had these issues:
- {ISSUE_1}
- {ISSUE_2}

Would you like me to update the skill?
{END_IF}
```

## Discovery Mode Prompts

### Gathering Requirements

Use `AskUserQuestion` tool with appropriate options:

**Project Type**:
```json
{
  "question": "What would you like to build?",
  "header": "Project",
  "options": [
    {"label": "Web Application", "description": "Website or web app with UI"},
    {"label": "CLI Tool", "description": "Command-line application"},
    {"label": "API/Backend", "description": "REST or GraphQL API server"},
    {"label": "Library/Package", "description": "Reusable code package"}
  ]
}
```

**Tech Stack** (varies by project type):
```json
{
  "question": "What tech stack would you like to use?",
  "header": "Stack",
  "options": [
    {"label": "Hono + Cloudflare", "description": "Edge-first, fast TypeScript"},
    {"label": "Next.js + Vercel", "description": "React full-stack framework"},
    {"label": "Go + Gin", "description": "Fast Go HTTP framework"},
    {"label": "Python + FastAPI", "description": "Modern Python API framework"}
  ]
}
```

**Confirmation**:
```json
{
  "question": "Ready to implement this spec?",
  "header": "Confirm",
  "options": [
    {"label": "Yes, start building", "description": "Begin the 5-phase implementation"},
    {"label": "Edit spec first", "description": "Make changes before implementing"},
    {"label": "Save and exit", "description": "Save spec to .kyotee/spec.md"}
  ]
}
```
