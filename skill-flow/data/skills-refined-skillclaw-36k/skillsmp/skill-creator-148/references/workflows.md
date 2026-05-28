# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Decision Trees

For complex branching with multiple paths:

```markdown
## Workflow Decision Tree

Start here and follow the arrows:

┌─────────────────────────────────┐
│ What type of document?          │
└────────────┬────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌────────┐      ┌────────┐
│  PDF   │      │  DOCX  │
└───┬────┘      └───┬────┘
    │               │
    ▼               ▼
[PDF flow]    [DOCX flow]
```

## Error Recovery Workflows

For fragile operations, include explicit error handling:

```markdown
## Image Processing Workflow

1. Load image
   - **If format unsupported**: Convert using ImageMagick first
   - **If corrupted**: Report error, suggest alternative source

2. Apply transformations
   - **If memory error**: Reduce resolution, retry
   - **If timeout**: Split into smaller operations

3. Save output
   - **If disk full**: Clean temp files, retry
   - **If permission denied**: Suggest alternative path
```

## Parallel vs Sequential

Indicate when steps can be parallelized:

```markdown
## Data Processing Workflow

### Sequential (order matters):
1. Validate input schema
2. Transform data
3. Write to database

### Parallel (can run simultaneously):
- Generate thumbnails
- Extract metadata
- Calculate checksums
```

## Context7 Integration in Workflows

When workflows involve external APIs or libraries, include Context7 lookup steps:

```markdown
## API Integration Workflow

1. **Research Phase** (Context7):
   - Resolve library: `context7_resolve-library-id "{api-name}"`
   - Fetch docs: `context7_get-library-docs {id} --topic "{relevant-topic}"`
   - Note current patterns and any deprecations

2. **Implementation Phase**:
   - Apply patterns from documentation
   - Use current API syntax
   - Follow documented best practices

3. **Validation Phase**:
   - Test against documented behavior
   - Verify error handling matches docs
```
