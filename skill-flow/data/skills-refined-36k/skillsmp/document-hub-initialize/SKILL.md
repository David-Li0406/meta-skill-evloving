---
name: document-hub-initialize
description: Bootstrap a new project's documentation hub by creating the four core documentation files (systemArchitecture.md, keyPairResponsibility.md, glossary.md, techStack.md) with initial content based on codebase analysis.
---

# Document Hub: Initialize

Bootstrap a new project with a complete documentation hub structure.

**Helper Scripts Available**:
- `scripts/validate_hub.py` - Validates documentation structure
- `scripts/extract_glossary.py` - Extracts domain-specific terms from code
- `scripts/detect_drift.py` - Detects existing modules and technologies

**Always run scripts with `--help` or check scripts/README.md first** to understand their usage and output format.

## What This Skill Does

Creates the Documentation Hub file structure in a project's `cline-docs/` directory:

```
project-root/
└── cline-docs/
    ├── systemArchitecture.md      # High-level architecture diagrams
    ├── keyPairResponsibility.md   # Module responsibilities
    ├── glossary.md                # Domain-specific terms
    └── techStack.md               # Technologies used
```

## Decision Tree: When to Use This Skill

```
User wants to set up documentation → Does cline-docs/ exist?
    ├─ Yes → Run validation first
    │         ├─ Valid → Use /document-hub read instead
    │         └─ Invalid → Ask user: overwrite or skip?
    │
    └─ No → Initialize new hub:
        1. Create directory structure
        2. Detect technologies (detect_drift.py)
        3. Extract glossary terms (extract_glossary.py)
        4. Generate initial content
        5. Validate result (validate_hub.py)
```

## Initialization Workflow

### Step 1: Check Existing State

First, check if a documentation hub already exists:

```bash
# Check if cline-docs exists
ls project-root/cline-docs/

# If exists, validate it first
python scripts/validate_hub.py /path/to/project
```

If validation returns `"valid": false` with missing files, proceed with initialization.

### Step 2: Gather Project Information

Use helper scripts to analyze the project:

**Detect existing technologies and modules:**
```bash
python scripts/detect_drift.py /path/to/project
```

This returns JSON with:
- Actual modules found in `src/`
- Technologies detected from `package.json`/`requirements.txt`
- Configuration files present

**Extract domain-specific terms:**
```bash
python scripts/extract_glossary.py /path/to/project
```

This returns ranked terms with context from code comments.

### Step 3: Create Documentation Files

Create the four core files with initial content based on the gathered information.

**systemArchitecture.md template:**
```markdown
# System Architecture

## High-Level Overview

[Brief description of what this project does]

## Architecture Diagram

\`\`\`mermaid
flowchart TD
    Client[Client/User] --> Server[Application Server]
    Server --> DB[Database]
\`\`\`

## Database Schema

[If applicable, add ER diagram or schema description]

## Key Processes

[Describe major workflows]
```

**keyPairResponsibility.md template:**
```markdown
# Key Modules & Responsibilities

## Project Overview

[What this project does and why]

## Module Breakdown

### [Module Name]
**Location:** `src/module-name/`
**Responsibility:** [What this module handles]
**Key Files:**
- `file1.ts` - [Purpose]
- `file2.ts` - [Purpose]
```

**glossary.md template:**
```markdown
# Glossary

Domain-specific terms used throughout the codebase.

## A

**[Term]** - [Definition based on code context]
```

**techStack.md template:**
```markdown
# Technology Stack

## Core Technologies

### [Framework Name]
**Purpose:** [What it's used for]
**Version:** [If detected from package.json]

## Infrastructure

[Databases, caching, etc.]

## Development Tools

[Build tools, testing frameworks, etc.]
```

### Step 4: Populate with Detected Information

Use the JSON output from helper scripts to populate initial content:

1. **From detect_drift.py output:**
   - Add detected technologies to `techStack.md`
   - Add detected modules to `keyPairResponsibility.md`

2. **From extract_glossary.py output:**
   - Add top 20-30 terms to `glossary.md` alphabetically
   - Include contexts as definitions

### Step 5: Prompt User for Additional Context

After creating initial files, ask the user:

```
Documentation hub initialized with detected information.

Please provide additional context:
1. What is the primary purpose of this project?
2. Are there any key architectural decisions to document?
3. Any specific modules or workflows that need detailed explanation?

I can update the documentation with your input.
```

### Step 6: Validate Result

After initialization, always validate:

```bash
python scripts/validate_hub.py /path/to/project
```

Check that:
- `"valid": true`
- All required files exist
- No Mermaid syntax errors

## Example: Complete Initialization

```python
import json
import subprocess
from pathlib import Path

project_path = Path("/path/to/project")
docs_path = project_path / "cline-docs"

# Step 1: Check if exists
if docs_path.exists():
    print("Documentation hub already exists. Validating...")
    result = subprocess.run(
        ["python", "scripts/validate_hub.py", str(project_path)],
        capture_output=True, text=True
    )
    validation = json.loads(result.stdout)
    if validation["valid"]:
        print("Hub is valid. Use /document-hub read to view it.")
        exit(0)

# Step 2: Create directory
docs_path.mkdir(exist_ok=True)

# Step 3: Detect technologies and modules
drift_result = subprocess.run(
    ["python", "scripts/detect_drift.py", str(project_path)],
    capture_output=True, text=True
)
drift_data = json.loads(drift_result.stdout)

# Step 4: Extract glossary terms
glossary_result = subprocess.run(
    ["python", "scripts/extract_glossary.py", str(project_path)],
    capture_output=True, text=True
)
glossary_data = json.loads(glossary_result.stdout)

# Step 5: Generate files
# [Create files using templates + detected data]

# Step 6: Validate
validate_result = subprocess.run(
    ["python", "scripts/validate_hub.py", str(project_path)],
    capture_output=True, text=True
)
validation = json.loads(validate_result.stdout)

if validation["valid"]:
    print("✓ Documentation hub initialized successfully!")
else:
    print("⚠ Issues detected:", validation["errors"])
```

## Best Practices

- **Run detection scripts first** - Don't guess what's in the project
- **Use templates** - Ensure consistent structure across projects
- **Validate after creation** - Always run `validate_hub.py` at the end
- **Prompt for context** - Auto-detected info needs human input for completeness
- **Keep diagrams simple** - Initial architecture diagrams should be high-level

## Common Pitfalls

❌ **Don't** create documentation without analyzing the codebase first
❌ **Don't** overwrite existing valid documentation without user confirmation
❌ **Don't** create empty files - populate with at least template structure

✅ **Do** use helper scripts to gather information
✅ **Do** validate before and after
✅ **Do** ask user for additional context

## What Comes Next

After initialization:
1. User reviews generated documentation
2. User provides additional context via prompts
3. Documentation is refined
4. Future updates use `/document-hub update` skill

## Helper Script Reference

**validate_hub.py** - Check documentation structure
```bash
python scripts/validate_hub.py /path/to/project
# Returns: {"valid": bool, "errors": [], "warnings": []}
```

**detect_drift.py** - Find undocumented code
```bash
python scripts/detect_drift.py /path/to/project
# Returns: {"module_drift": {...}, "technology_drift": {...}}
```

**extract_glossary.py** - Extract domain terms
```bash
python scripts/extract_glossary.py /path/to/project
# Returns: {"terms": [{term, contexts, score}...]}
```

See `scripts/README.md` for complete documentation.
