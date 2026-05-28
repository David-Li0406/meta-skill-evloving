---
name: document-hub-update
description: Comprehensive review and update of the documentation hub. Analyzes recent code changes, detects drift, validates structure, and proposes specific updates to keep documentation synchronized with the codebase.
---

# Document Hub: Update

Intelligently update documentation based on code changes and drift detection.

**Helper Scripts Available**:
- `scripts/analyze_changes.py` - Analyzes git history since last doc update
- `scripts/detect_drift.py` - Finds undocumented modules and technologies
- `scripts/validate_hub.py` - Validates documentation structure
- `scripts/extract_glossary.py` - Extracts new domain terms

**Always run scripts with `--help` or check scripts/README.md first** to understand their usage and output format.

## What This Skill Does

Performs a comprehensive review and update of all documentation hub files:

1. Analyzes what changed since last doc update (via git)
2. Detects drift between docs and codebase
3. Proposes specific, scoped updates
4. Validates result after updates

## Decision Tree: Update Strategy

```
User requests update → Is this a git repository?
    ├─ Yes → Analyze changes since last doc update
    │         ├─ No changes → Check drift anyway (dependencies might have changed)
    │         └─ Changes detected → Categorize and scope update
    │
    └─ No git → Full drift analysis
        ├─ Low drift (<0.15) → Minor updates only
        ├─ Medium drift (0.15-0.35) → Focused updates
        └─ High drift (>0.35) → Comprehensive review needed
```

## Update Workflow

### Phase 1: Pre-Update Analysis

**Step 1: Validate Current State**

Always validate before making changes:

```bash
python scripts/validate_hub.py /path/to/project
```

If validation fails:
- Fix structural errors first
- Address broken cross-references
- Repair invalid Mermaid diagrams
- Then proceed with content updates

**Step 2: Analyze Recent Changes**

Use git history to scope the update:

```bash
# Auto-detect since last doc update
python scripts/analyze_changes.py /path/to/project

# Or specify a commit/date
python scripts/analyze_changes.py /path/to/project abc123
```

This returns JSON categorizing changes.

**Step 3: Detect Drift**

Even if no recent changes, check for drift:

```bash
python scripts/detect_drift.py /path/to/project
```

This identifies undocumented modules, missing technologies, and documented-but-removed code.

### Phase 2: Propose Updates

Based on analysis, propose specific updates to the user with priorities (high/medium/low).

### Phase 3: Execute Updates

Update each file systematically based on change analysis.

### Phase 4: Post-Update Validation

After making updates, always validate:

```bash
python scripts/validate_hub.py /path/to/project
```

## Best Practices

- **Always validate first** - Fix structural issues before content updates
- **Use git analysis** - Let `analyze_changes.py` scope the update
- **Present proposals** - Show user what will change
- **Update incrementally** - One file at a time, validate between

See `scripts/README.md` for complete helper script documentation.
