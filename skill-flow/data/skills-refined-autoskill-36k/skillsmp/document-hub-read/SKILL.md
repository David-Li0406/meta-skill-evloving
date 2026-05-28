---
name: document-hub-read
description: Read and summarize the current state of the documentation hub. Provides a quick overview of system architecture, module responsibilities, technology stack, and glossary terms.
---

# Document Hub: Read

View and summarize the current documentation hub state.

**Helper Scripts Available**:
- `scripts/validate_hub.py` - Validates documentation structure

**Use this skill to** quickly understand a project's documentation without reading all files individually.

## What This Skill Does

Reads all documentation hub files and presents a structured summary:

1. Validates the hub structure
2. Extracts key information from each file
3. Presents an organized overview
4. Identifies any gaps or issues

## Decision Tree: When to Use This Skill

```
User wants to understand docs → Does hub exist?
    ├─ No → Suggest /document-hub initialize
    │
    └─ Yes → Read and summarize:
        1. Validate structure first
        2. Read all four core files
        3. Extract key sections
        4. Present formatted summary
        5. Identify any warnings/gaps
```

## Read Workflow

### Step 1: Validate Before Reading

Always validate first to catch structural issues:

```bash
python scripts/validate_hub.py /path/to/project
```

If validation returns warnings or errors, include them in the summary.

### Step 2: Read Core Files

Read all four core files:
- `systemArchitecture.md`
- `keyPairResponsibility.md`
- `glossary.md`
- `techStack.md`

### Step 3: Extract Key Information

From each file, extract:

**systemArchitecture.md:**
- High-level system description
- Number of Mermaid diagrams
- Key architectural components

**keyPairResponsibility.md:**
- Project purpose
- Number of documented modules
- Module names and responsibilities

**glossary.md:**
- Total number of terms
- Sample key terms (top 5-10)

**techStack.md:**
- Core technologies listed
- Infrastructure components
- Development tools

### Step 4: Present Summary

Format the summary in a clear, scannable structure:

```
Documentation Hub Summary
=========================

Status: ✓ Valid (or ⚠ Issues detected)

## System Architecture
- Description: [1-2 sentence summary]
- Diagrams: 3 Mermaid diagrams
- Key Components: API Gateway, Auth Service, Database

## Module Responsibilities
- Total Modules: 8
- Key Modules:
  • auth - User authentication and authorization
  • payments - Payment processing integration
  • notifications - Email and push notifications

## Technology Stack
- Framework: Next.js 14
- Database: PostgreSQL + Redis
- Infrastructure: Docker, AWS
- [X more technologies]

## Glossary
- Total Terms: 42
- Key Terms: FulfillmentJob, CIP, Ledger, BatchProcessor, ...

## Health Check
- Validation: ✓ Passed
- Warnings: 1 (Complex diagram in systemArchitecture.md)
- Last Updated: [Git last modified date if available]
```

## Example: Complete Read Operation

```python
import json
import subprocess
from pathlib import Path

project_path = Path("/path/to/project")
docs_path = project_path / "cline-docs"

# Step 1: Validate
validate = subprocess.run(
    ["python", "scripts/validate_hub.py", str(project_path)],
    capture_output=True, text=True
)
validation = json.loads(validate.stdout)

# Step 2: Check if hub exists
if not docs_path.exists():
    print("Documentation hub not found.")
    print("Run /document-hub initialize to create it.")
    exit(0)

# Step 3: Read files
files = {
    "arch": docs_path / "systemArchitecture.md",
    "resp": docs_path / "keyPairResponsibility.md",
    "glossary": docs_path / "glossary.md",
    "tech": docs_path / "techStack.md"
}

content = {}
for key, file_path in files.items():
    if file_path.exists():
        with open(file_path) as f:
            content[key] = f.read()

# Step 4: Extract and summarize
# [Parse content and extract key information]

# Step 5: Present summary
print("Documentation Hub Summary")
print("=" * 50)
print(f"Status: {'✓ Valid' if validation['valid'] else '⚠ Issues'}")
# [Rest of summary...]
```

## Use Cases

### Quick Onboarding

When joining a project:
```
Developer: "What does this project do?"
→ Run /document-hub read
→ Get instant architecture + module overview
```

### Pre-Task Context

Before starting work:
```
Developer: "I need to understand the auth system"
→ Run /document-hub read
→ See auth module responsibility
→ Check glossary for domain terms
```

### Documentation Health Check

Periodic maintenance:
```
→ Run /document-hub read
→ Check for validation warnings
→ If drift detected, run /document-hub analyze
```

## Best Practices

- **Always validate first** - Catch structural issues
- **Present concisely** - Users want overview, not full content
- **Highlight warnings** - Draw attention to validation issues
- **Suggest actions** - If issues found, suggest next steps

## Common Pitfalls

❌ **Don't** just dump file contents - summarize them
❌ **Don't** skip validation - it catches important issues
❌ **Don't** hide warnings - users need to know about problems

✅ **Do** provide structured, scannable output
✅ **Do** include health status upfront
✅ **Do** suggest follow-up actions if needed

## What Comes Next

After reading:
- If gaps found → Suggest `/document-hub analyze` for detailed drift report
- If outdated → Suggest `/document-hub update` to refresh
- If invalid → Show specific errors and suggest fixes

## Helper Script Reference

**validate_hub.py** - Check documentation structure
```bash
python scripts/validate_hub.py /path/to/project
# Returns: {"valid": bool, "errors": [], "warnings": []}
```

See `scripts/README.md` for complete documentation.
