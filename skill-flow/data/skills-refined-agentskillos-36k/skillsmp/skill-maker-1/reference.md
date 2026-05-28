# Skill Maker - Technical Reference

## Advanced Skill Generation Patterns

### Multi-File Skill Architectures

Complex skills may benefit from modular file organization:

```
skill-name/
├── SKILL.md (primary definition)
├── reference.md (advanced usage, API details)
├── examples.md (comprehensive usage scenarios)
├── scripts/
│   ├── validator.py (input validation)
│   ├── processor.py (core logic)
│   └── formatter.py (output formatting)
└── templates/
    ├── config.template.json
    └── output.template.md
```

**When to Use Multi-File Architecture**:
- Skills requiring external script execution
- Complex workflows benefiting from modular decomposition
- Skills providing templating or scaffolding functionality
- Documentation-heavy skills requiring comprehensive reference materials

### Tool Restriction Strategies

The `allowed-tools` field enables fine-grained capability control:

**Read-Only Skills**:
```yaml
allowed-tools: Read, Grep, Glob
```

**Analysis-Only Skills**:
```yaml
allowed-tools: Read, Grep, Glob, Bash
```
(Bash restricted to read-only commands through instructions)

**File Modification Skills**:
```yaml
allowed-tools: Read, Edit, Write, Grep, Glob
```

**Web-Enabled Skills**:
```yaml
allowed-tools: Read, Write, WebFetch, WebSearch
```

**Unrestricted Skills** (omit `allowed-tools` entirely):
- Appropriate for general-purpose utilities
- Skills requiring adaptive tool selection
- Meta-skills like skill-maker itself

### Description Optimization for Discovery

Effective descriptions maximize skill activation probability through strategic keyword inclusion:

**Pattern: Function + Triggers + Context**

```yaml
description: |
  Extract text and tables from PDF files, fill PDF forms, merge and split documents.
  Use when working with PDF files, Adobe documents, or when the user mentions PDFs,
  forms, document extraction, OCR, or text parsing from portable documents.
```

**Keyword Categories**:
1. **File Extensions**: .pdf, .xlsx, .csv, .json, .xml
2. **Domain Terminology**: API, database, authentication, testing
3. **Action Verbs**: extract, analyze, transform, generate, validate
4. **Technology Names**: React, Python, Docker, Kubernetes
5. **Operational Contexts**: deployment, CI/CD, debugging, monitoring

### Instruction Engineering for Autonomous Execution

Skills must provide sufficient procedural detail for Claude to execute without human intervention:

**Insufficient Instruction**:
```markdown
## Instructions
1. Read the file
2. Process it
3. Output results
```

**Adequate Instruction**:
```markdown
## Instructions

### Phase 1: Input Validation
1. Verify target file existence using Read tool
2. Validate file format matches expected type
3. If validation fails, report specific error and halt

### Phase 2: Processing
1. Parse file content using appropriate method:
   - JSON: Parse with standard library
   - CSV: Split by delimiter, handle quoted fields
   - XML: Parse DOM structure
2. Apply transformation logic:
   - Filter rows matching criteria
   - Aggregate statistical measures
   - Restructure data format
3. Validate processing completeness

### Phase 3: Output Generation
1. Format results according to user preference:
   - Tabular display for terminal output
   - JSON for programmatic consumption
   - Markdown for documentation
2. Write output using Write tool
3. Confirm completion with summary statistics
```

## YAML Frontmatter Validation

### Common Syntax Errors

**Error: Missing Closing Delimiter**
```yaml
---
name: my-skill
description: Does something useful
# Missing closing ---
```
**Resolution**: Add closing `---` before markdown content

**Error: Invalid Character in Name**
```yaml
---
name: My_Skill (underscore invalid)
description: Does something useful
---
```
**Resolution**: Use kebab-case: `my-skill`

**Error: Unquoted Special Characters**
```yaml
---
name: skill-name
description: Handles files: PDFs, CSVs, and JSON (colon requires quoting)
---
```
**Resolution**: Quote the description:
```yaml
description: "Handles files: PDFs, CSVs, and JSON"
```

**Error: Tab Characters in YAML**
```yaml
---
name: skill-name
→description: Uses tab for indentation (invalid)
---
```
**Resolution**: Use spaces exclusively

### Validation Checklist

Before finalizing generated skills, verify:

- [ ] Opening `---` on line 1
- [ ] Closing `---` before markdown content
- [ ] Name field: kebab-case, ≤64 chars, [a-z0-9-] only
- [ ] Description field: ≤1024 chars, includes triggers
- [ ] allowed-tools field (if present): comma-separated valid tool names
- [ ] No tab characters in YAML section
- [ ] Special characters properly quoted
- [ ] Valid YAML structure (test with parser if uncertain)

## Skill Naming Conventions

### Naming Patterns by Skill Type

**File Format Processors**:
- `pdf-processor`, `csv-analyzer`, `json-transformer`
- Pattern: `{format}-{verb}`

**Technology-Specific Tools**:
- `react-component-generator`, `docker-compose-manager`
- Pattern: `{technology}-{domain}-{verb}`

**Workflow Automation**:
- `code-reviewer`, `test-runner`, `deployment-checker`
- Pattern: `{noun}-{verb}` or `{verb}-{noun}`

**Domain-Specific Utilities**:
- `api-client-generator`, `database-migrator`
- Pattern: `{domain}-{function}`

### Naming Anti-Patterns

**Too Generic** (poor discoverability):
- `helper`, `utility`, `tool`

**Too Verbose** (poor readability):
- `advanced-multi-format-document-processor-with-ocr`

**Technology-Ambiguous** (poor clarity):
- `processor` (what does it process?)
- `analyzer` (what does it analyze?)

## Dependency Documentation Patterns

### Python Dependencies

```markdown
## Requirements

This skill requires Python packages. Install via:

\```bash
pip install pandas openpyxl xlsxwriter
\```

Or add to requirements.txt:
\```
pandas>=2.0.0
openpyxl>=3.1.0
xlsxwriter>=3.0.0
\```
```

### System Utilities

```markdown
## Requirements

This skill requires system utilities:

**Linux/macOS**:
\```bash
sudo apt-get install imagemagick  # Debian/Ubuntu
brew install imagemagick          # macOS
\```

**Windows**:
Download from https://imagemagick.org/script/download.php
```

### Node.js Dependencies

```markdown
## Requirements

This skill requires Node.js packages:

\```bash
npm install --save-dev prettier eslint
\```

Or using yarn:
\```bash
yarn add --dev prettier eslint
\```
```

## Error Handling Patterns

### Graceful Degradation

Skills should handle missing dependencies gracefully:

```markdown
## Instructions

1. Check for required dependency:
   \```bash
   which pdftotext || echo "MISSING"
   \```

2. If dependency missing:
   - Inform user of missing requirement
   - Provide installation instructions
   - Halt execution gracefully

3. If dependency available:
   - Proceed with normal workflow
```

### Input Validation

```markdown
## Instructions

### Input Validation Phase

1. Verify file exists:
   - Use Read tool to attempt file access
   - If file not found, report error with exact path attempted

2. Verify file format:
   - Check file extension matches expected type
   - For binary formats, validate magic bytes/file signature
   - If format mismatch, report expected vs. actual format

3. Verify file accessibility:
   - Attempt to read first 100 bytes
   - If permission denied, report access issue
```

## Testing Generated Skills

### Activation Testing Strategy

After generating a skill, verify activation with targeted queries:

**Example: Testing csv-processor skill**

Description includes: "CSV files", "tabular data", "spreadsheet"

**Test Queries**:
- "Analyze this CSV file"
- "Process the tabular data in data.csv"
- "Read this spreadsheet and show me statistics"

**Expected Behavior**: Skill should activate for all queries

**Non-Activation Test**: "Analyze this PDF file"
**Expected Behavior**: csv-processor should NOT activate

### Functional Testing Checklist

After skill activation:

- [ ] Instructions execute in correct sequence
- [ ] Tool calls use appropriate tools
- [ ] Error handling triggers on invalid input
- [ ] Output format matches specification
- [ ] Dependencies properly detected/reported
- [ ] Edge cases handled gracefully

## Meta-Skill Design Patterns

The skill-maker itself exemplifies meta-skill patterns:

**Self-Referential Documentation**:
- Skill demonstrates its own standards
- Instructions reference the output format

**Recursive Capability**:
- Could theoretically generate improved versions of itself
- Demonstrates skill generation by being a skill

**Quality Enforcement**:
- Validates outputs against documented standards
- Implements systematic verification procedures

## Advanced: Plugin-Based Skill Distribution

Skills may be bundled within plugins for distribution:

```
my-plugin/
├── plugin.json
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

**plugin.json Structure**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "skills": ["skill-one", "skill-two"]
}
```

When generating skills intended for plugin distribution, consider:
- Namespace conflicts with existing skills
- Cross-skill dependencies
- Plugin-level documentation requirements
- Version compatibility specifications

## Template: Minimal Viable Skill

The absolute minimum required for a functional skill:

```yaml
---
name: example-skill
description: Does X when user mentions Y. Use for Z contexts.
---

# Example Skill

## Instructions

1. Perform action A
2. Perform action B
3. Output result C
```

## Template: Comprehensive Skill

Full-featured skill with all optional components:

```yaml
---
name: comprehensive-example
description: Performs X, Y, and Z operations on A, B, C file types. Use when user mentions keywords K1, K2, K3 or works with files F1, F2, F3.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Comprehensive Example Skill

## Purpose
[High-level capability statement]

## Instructions

### Phase 1: Preparation
[Detailed steps]

### Phase 2: Execution
[Detailed steps]

### Phase 3: Validation
[Detailed steps]

## Requirements

[Dependencies with installation commands]

## Common Workflows

### Workflow 1: [Name]
[Specific procedural guidance]

### Workflow 2: [Name]
[Specific procedural guidance]

## Error Handling

### Error Condition 1
[Detection and resolution]

### Error Condition 2
[Detection and resolution]

## Examples

See [examples.md](examples.md) for comprehensive usage scenarios.

## Advanced Usage

See [reference.md](reference.md) for technical details.
```

## Skill Generation Decision Tree

```
User requests skill creation
├─ Is functional purpose clear?
│  ├─ Yes: Proceed to tool selection
│  └─ No: Ask "What specific task should this skill perform?"
│
├─ Are activation triggers defined?
│  ├─ Yes: Proceed to scope validation
│  └─ No: Ask "What keywords/contexts should activate this skill?"
│
├─ Are required tools known?
│  ├─ Yes: Proceed to dependency check
│  └─ No: Ask "What operations are needed? (read files, web search, etc.)"
│
├─ Are external dependencies required?
│  ├─ Yes: Document installation procedures
│  └─ No: Proceed to generation
│
├─ Is scope appropriately focused?
│  ├─ Yes: Generate skill
│  └─ No: Suggest decomposition into multiple skills
│
└─ Generate and validate
```

## References

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [YAML Specification](https://yaml.org/spec/1.2/spec.html)
- [Kebab Case Naming Convention](https://en.wikipedia.org/wiki/Letter_case#Kebab_case)
