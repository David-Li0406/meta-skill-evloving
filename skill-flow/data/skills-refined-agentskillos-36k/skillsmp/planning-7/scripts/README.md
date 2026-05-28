# Planning Skill Scripts

## Overview

These scripts support the planning skill workflows. They are Node.js scripts (NOT Python) that automate common planning tasks.

**Note**: These are placeholder scripts. Full implementation would use Node.js with ESM syntax.

---

## Scripts

### generate-prd.sh

**Purpose**: Generate PRD from feature request

**Usage**:
```bash
./scripts/generate-prd.sh "Feature description" "category"
```

**Process**:
1. Parse feature description
2. Determine category (harden-polish, features, enhancements, refactors)
3. Generate kebab-case filename
4. Load PRD template
5. Fill in template sections based on description
6. Write to `docs/project_plans/PRDs/[category]/[feature-name]-v1.md`

**Output**: Path to created PRD file

**Status**: Placeholder - needs Node.js implementation

---

### generate-impl-plan.sh

**Purpose**: Generate implementation plan from PRD

**Usage**:
```bash
./scripts/generate-impl-plan.sh "path/to/prd.md"
```

**Process**:
1. Read PRD content
2. Extract requirements and proposed phases
3. Generate 8-phase task breakdown following MP architecture
4. Add subagent assignments using `../references/subagent-assignments.md`
5. Calculate total lines
6. If >800 lines: Create phase breakout files
7. Write main plan and phase files to `docs/project_plans/implementation_plans/[category]/`

**Output**: Path(s) to created implementation plan file(s)

**Status**: Placeholder - needs Node.js implementation

---

### optimize-plan.sh

**Purpose**: Break long plan into phase-specific files

**Usage**:
```bash
./scripts/optimize-plan.sh "path/to/plan.md"
```

**Process**:
1. Read plan and count lines
2. If <800 lines: Report "no optimization needed"
3. If >800 lines:
   - Identify phases
   - Determine optimal grouping strategy (see `../references/optimization-patterns.md`)
   - Create subdirectory: `[plan-name]/`
   - Create phase files with grouped content
   - Update parent plan with summary and links
4. Validate all content preserved

**Output**: List of created phase files

**Status**: Placeholder - needs Node.js implementation

---

### assign-subagents.sh

**Purpose**: Add subagent assignments to tasks in plan

**Usage**:
```bash
./scripts/assign-subagents.sh "path/to/plan.md"
```

**Process**:
1. Read plan and extract all tasks
2. For each task:
   - Determine task type (database, API, frontend, testing, etc.)
   - Look up appropriate subagents in `../references/subagent-assignments.md`
   - Add "Assigned Subagent(s): agent-1, agent-2" to task description
3. Update plan file with assignments

**Output**: "Updated [filename] with subagent assignments"

**Status**: Placeholder - needs Node.js implementation

---

### create-progress-tracking.sh

**Purpose**: Create progress tracking document from implementation plan

**Usage**:
```bash
./scripts/create-progress-tracking.sh "path/to/plan.md"
```

**Process**:
1. Read implementation plan
2. Extract all phases and tasks
3. Determine feature name from plan filename
4. Load progress tracking template
5. Fill in:
   - Phase overview table
   - Per-phase task checklists
   - Subagent assignments (from plan or assign dynamically)
   - Success criteria
6. Create directory: `.claude/progress/[feature-name]/`
7. Write `all-phases-progress.md`
8. Update PRD with link to progress file

**Output**: Path to created progress tracking file

**Status**: Placeholder - needs Node.js implementation

---

## Implementation Notes

### Technology Choice

**Use Node.js with ESM syntax** (NOT Python):

```javascript
#!/usr/bin/env node

import { readFile, writeFile } from 'fs/promises';
import { parse } from 'yaml';

// Script implementation
```

**Why Node.js?**
- Consistent with MeatyPrompts ecosystem (TypeScript/JavaScript)
- Native async/await support
- Better for file I/O and text processing
- Aligns with other tooling

### Dependencies

Likely dependencies for full implementation:

```json
{
  "dependencies": {
    "yaml": "^2.3.0",
    "gray-matter": "^4.0.3",
    "markdown-it": "^13.0.0",
    "commander": "^11.0.0"
  }
}
```

### Error Handling

All scripts should:
- Validate inputs
- Check file existence
- Handle parsing errors
- Provide clear error messages
- Exit with appropriate codes

### Testing

Scripts should be tested with:
- Valid inputs
- Invalid inputs
- Edge cases (very short/long content)
- File system errors

---

## Future Implementation

To implement these scripts:

1. **Set Up Node.js Project**:
   ```bash
   cd .claude/skills/planning/scripts
   npm init -y
   npm install yaml gray-matter markdown-it commander
   ```

2. **Implement Each Script**:
   - Use templates from `../templates/`
   - Reference guides from `../references/`
   - Follow Node.js best practices
   - Add comprehensive error handling

3. **Add CLI Interfaces**:
   - Use `commander` for argument parsing
   - Provide help text
   - Support flags and options

4. **Test Thoroughly**:
   - Unit tests for parsing logic
   - Integration tests with real files
   - Edge case testing

5. **Document Usage**:
   - Update this README with full examples
   - Add to SKILL.md
   - Include in main project docs

---

## Quick Reference

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| generate-prd.sh | Create PRD | Feature description | PRD file path |
| generate-impl-plan.sh | Create plan | PRD path | Plan file path(s) |
| optimize-plan.sh | Break up plan | Plan path | Phase file paths |
| assign-subagents.sh | Add assignments | Plan path | Updated plan |
| create-progress-tracking.sh | Create progress doc | Plan path | Progress file path |

---

## Contributing

When implementing these scripts:

1. Follow Node.js conventions
2. Use ESM syntax (import/export)
3. Add comprehensive error handling
4. Write tests for all functionality
5. Update this README with examples
6. Document any new dependencies
