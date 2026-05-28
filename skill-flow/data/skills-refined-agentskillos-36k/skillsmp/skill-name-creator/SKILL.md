---
name: skill-name-creator
description: Name new OpenCode skills and tool identifiers using the ASIS compliance test; outputs PASS/FAIL with error codes plus a valid OpenCode skill folder name.
license: MIT
metadata:
  short-description: ASIS-compliant skill naming
  standard: ASIS v2.01
---

# ASIS Skill Namer

## What I do
When creating or renaming a skill, I generate:
1. An **ASIS tool identifier** (PascalCase_With_Underscores)
2. A valid **OpenCode skill name** (lowercase-hyphen) + folder path
3. Run the **ASIS Compliance Test** and return **PASS/FAIL** with error codes

## When to use me
Use me **before**:
- Creating a new skill folder
- Renaming an existing skill
- Registering a new tool/function name that should follow ASIS

## Inputs I extract
From the user's request (no follow-up unless truly impossible):
- **Capability** (one sentence, operational)
- **Namespace**: Core vs Integration
- **Action**: from controlled vocabulary
- **Target**: concrete noun
- **Qualifier** (optional): output format / scope / mode

## Output
```json
{
  "asis_identifier": "Revit_Launch_Dynamo",
  "opencode_skill_name": "revit-launch-dynamo",
  "folder_path": ".opencode/skills/revit-launch-dynamo/SKILL.md",
  "result": "PASS",
  "errors": [],
  "warnings": [],
  "notes": "1-line rationale"
}
```

## Naming procedure

### Step 1 — Choose Namespace
- **Integration**: If request mentions specific product/platform/app (Revit, GitHub, Docker)
- **Core**: Otherwise (File, Shell, Net, Data, Logic)

### Step 2 — Choose Action (controlled vocabulary)

**CRUD**: Read, Write, Update, Delete, List, Search

**Ops**: Execute, Launch, Sync, Build, Deploy, Connect, Backup, Scan, Parse, Validate

**Hard mappings**:
- "create", "make" → Write
- "open", "get", "fetch" → Read or Net_Fetch_*, File_Read_*
- "fix", "improve", "handle", "manage" → INVALID

### Step 3 — Choose Target
Target must be concrete (File, Directory, Sheet, View, Image, Repo, Container).
Reject abstract targets (Quality, Idea, State, Happiness).

### Step 4 — Optional Qualifier
Only if needed to constrain output/format (Pdf, Json, Full, Incremental).

### Step 5 — Assemble
Format: `[Namespace]_[Action]_[Target]_[Qualifier(Optional)]`

### Step 6 — Run ASIS Compliance Test
Return PASS/FAIL with codes.

### Step 7 — Derive OpenCode Name
- Split by `_`
- Split PascalCase into tokens
- Lowercase everything
- Join with `-`

Example: `GitHub_Write_PullRequest` → `github-write-pull-request`

## ASIS Compliance Test

**Phase 1 — Syntax**: `^[A-Z][a-zA-Z0-9]*(?:_[A-Z][a-zA-Z0-9]*)*$`

**Phase 2 — Segments**: 3 or 4 segments (Namespace_Action_Target[_Qualifier])

**Phase 3 — Namespace Allowlist**
- Core: File, Shell, Net, Data, Logic
- Integration: Git, GitHub, Docker, AWS, Revit, Chrome

**Phase 4 — Action Allowlist**
- CRUD: Read, Write, Update, Delete, List, Search
- Ops: Execute, Launch, Sync, Build, Deploy, Connect, Backup, Scan, Parse, Validate

**Phase 5 — Target**: Must be concrete

**Phase 6 — Qualifier**: Must be constraining + concrete

**Phase 7 — Determinism**: No cognition/non-verifiable outcomes

## Quick examples

**PASS**:
- `Revit_Launch_Dynamo`
- `File_Search_Text`
- `Data_Backup_Snapshot`
- `Net_Fetch_Url`

**FAIL**:
- `Logic_Think_About_Problem` (ERR_ACTION_INVALID, ERR_NON_DETERMINISTIC)
- `Data_Improve_Quality` (ERR_ACTION_INVALID, ERR_TARGET_ABSTRACT)
- `Revit_Fix_Model` (ERR_ACTION_INVALID, ERR_NON_DETERMINISTIC)

## Error codes

| Code | Meaning |
|------|---------|
| ERR_SYNTAX_CASE | Invalid PascalCase |
| ERR_SEGMENT_COUNT | Not 3-4 segments |
| ERR_NAMESPACE_INVALID | Namespace not in allowlist |
| ERR_ACTION_INVALID | Action not in controlled vocabulary |
| ERR_TARGET_ABSTRACT | Target is abstract/cognitive |
| ERR_QUALIFIER_INVALID | Qualifier not constraining |
| ERR_NON_DETERMINISTIC | Describes cognition or non-verifiable outcomes |
