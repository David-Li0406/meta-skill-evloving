---
name: v2-docs-management
description: Use this skill to manage and review V2 transaction MDX documentation for coverage, accuracy, and alignment with YAML sources.
---

# Body of the merged SKILL.md

<introduction>
This skill orchestrates the management and review of V2 transaction MDX documentation files located in `content/docs/protocol/v2/transactions/`. It tracks documentation coverage, identifies gaps, and ensures accuracy by comparing MDX content against the analyzed YAML source files.
</introduction>

<workflow>
## When Invoked

1. **Scan Documentation Directory**
   - List all MDX files in `content/docs/protocol/v2/transactions/`
   - Compare against expected transactions from `v2-transaction-tracker.json`
   - Identify missing, outdated, or misaligned documentation

2. **Display Coverage Dashboard**
   - Show summary: X documented, Y missing, Z needs update
   - List transactions by system (global, instance, course, project)
   - Highlight path misalignments between current and expected paths

3. **Identify Work Needed**
   - List transactions with no MDX file
   - List transactions with path misalignment (legacy paths)
   - List transactions that need content review (outdated info)

4. **Prompt for Action**
   - Offer to run `/v2-docs-review` for specific transactions
   - Offer to migrate files to correct paths
   - Offer to create missing documentation stubs

5. **Review Individual Transaction**
   - User specifies transaction ID (e.g., `course.student.enroll`)
   - Look up in `v2-docs-tracker.json` for current state
   - Gather sources: Read the YAML source file, current MDX file, and address-registry.json
   - Compare MDX content against YAML, checking for completeness and accuracy
   - Generate a report listing correct, missing, and incorrect items with specific fixes needed
   - Offer actions to create new MDX, update existing MDX, or migrate files to correct paths
</workflow>

<statuses>
## Documentation Statuses

| Status | Meaning |
|--------|---------|
| `missing` | No MDX file exists for this transaction |
| `path-mismatch` | MDX exists but at wrong path (needs migration) |
| `needs-review` | MDX exists but content may be outdated |
| `reviewed` | MDX reviewed and content is current |
| `verified` | MDX verified against live API documentation |

## Status Flow

```
missing → created → needs-review → reviewed → verified
                         ↑              ↓
path-mismatch → migrated ┘              │
                         ↑              ↓
                         └──────────────┘ (if API changes)
```
</statuses>

<path-alignment>
## Path Alignment Rules

MDX paths MUST match the API endpoint structure:

| API Endpoint | Expected MDX Path |
|--------------|-------------------|
| `/v2/tx/{system}/{role}/{action}` | `{system}/{role}/{action}.mdx` |

### Current Path Issues (Known)

| Transaction ID | Current Path | Expected Path |
|----------------|--------------|---------------|
| instance.owner.course.create | course/admin/create.mdx | instance/owner/course/create.mdx |
| instance.owner.project.create | (missing) | instance/owner/project/create.mdx |
| course.owner.teachers.manage | course/admin/teachers-update.mdx | course/owner/teachers/manage.mdx |
| course.teacher.assignments.assess | course/teacher/assignments-assess.mdx | course/teacher/assignments/assess.mdx |
| course.student.assignment.action | course/student/assignment-update.mdx | course/student/assignment/action.mdx |
| course.student.credential.claim | course/student/credential-claim.mdx | course/student/credential/claim.mdx |
| global.general.access-token.mint | general/mint-access-token.mdx | global/general/access-token/mint.mdx |

### Base Path
- MDX: `content/docs/protocol/v2/transactions/`
</path-alignment>

<coverage-checklist>
## Documentation Coverage Checklist

Each transaction MDX should include:

### Required Sections
- [ ] **Title & Description** - Frontmatter with tx_file reference
- [ ] **API Endpoint** - Correct path format (`/v2/tx/...`)
- [ ] **Cost Breakdown** - Table with fees, deposits, wallet delta
- [ ] **Request Body** - JSON example with current field names
- [ ] **Transaction Pattern** - Mint/Spend/Burn pattern description
- [ ] **Inputs** - Table of inputs with validators
- [ ] **Outputs** - Table of outputs with values
- [ ] **Minting Operations** - If applicable
- [ ] **Datum Changes** - Before/after datum structures
- [ ] **Reference Inputs** - Script references used
- [ ] **Notes** - Key insights and caveats

### Quality Checks
- [ ] API endpoint matches current Atlas API
- [ ] Request body fields match current API schema
- [ ] Costs are accurate (compare to YAML)
- [ ] Validator names match address-registry.json
- [ ] tx_file frontmatter points to correct YAML
</coverage-checklist>

<mdx-template>
## MDX Template

```mdx
---
title: "{Transaction Title}"
description: "{One-line description}"
tx_file: "{path/to/yaml}"
---

# {Transaction Title}

{Brief description of what this transaction does.}

## API Endpoint

\`\`\`
POST /v2/tx/{system}/{role}/{action}
\`\`\`

## Cost Breakdown

| Component | Amount |
|-----------|--------|
| Transaction Fee | ~{X.XX} ADA |
| Protocol Fee | {X} ADA |
| {Deposit Type} | ~{X.XX} ADA |
| **Total Wallet Delta** | **~{X.XX} ADA** |

{Notes about deposits being recoverable, etc.}

## Request Body

\`\`\`json
{
  "field1": "value1",
  "field2": "value2"
}
\`\`\`

{Description of fields, which are required/optional.}

## Transaction Pattern

**{Pattern Name}** - {Brief description of what happens}.

## Inputs

| ID | Type | Validator | Description |
|----|------|-----------|-------------|
| {input_id} | script/wallet | {validator-name} | {description} |

## Outputs

| ID | Type | Validator | Value | Description |
|----|------|-----------|-------|-------------|
| {output_id} | script/wallet | {validator-name} | ~{X.XX} ADA + {tokens} | {description} |

## Minting Operations

| Policy | Token | Quantity | Description |
|--------|-------|----------|-------------|
| {policy-name} | {token-name} | {qty} | {description} |

## Datum Changes

### Before
\`\`\`json
{
  "constructor": N,
  "fields": [...]
}
\`\`\`

### After
\`\`\`json
{
  "constructor": N,
  "fields": [...]
}
\`\`\`

## Reference Inputs

| ID | Description |
|----|-------------|
| {ref_id} | {description} |

## Notes

- {Key insight 1}
- {Key insight 2}
- {Caveat or important behavior}
```
</mdx-template>

<migration-steps>
## Migration Steps (for path-mismatch)

When a file exists at the wrong path:

1. **Read current file** at old path
2. **Update tx_file frontmatter** to new YAML path
3. **Review content** against YAML source
4. **Create directories** for new path if needed
5. **Write file** to new path
6. **Delete old file**
7. **Update meta.json** files for old and new directories
8. **Update v2-docs-tracker.json** with new path and status

### Directory Structure Updates

When creating new directories, ensure each has:
- `index.mdx` - Overview page for that section
- `meta.json` - Navigation configuration

Example meta.json:
```json
{
  "title": "Student",
  "pages": ["enroll", "assignment", "credential"]
}
```

For nested actions (e.g., `credential/claim`), the parent becomes a directory:
```
course/student/
├── index.mdx
├── meta.json
├── enroll.mdx
├── assignment/
│   ├── index.mdx
│   ├── meta.json
│   └── action.mdx
└── credential/
    ├── index.mdx
    ├── meta.json
    └── claim.mdx
```
</migration-steps>

<report-format>
## Review Report Format

```
═══════════════════════════════════════════════════════════════
           V2 DOCUMENTATION REVIEW: {transaction.id}
═══════════════════════════════════════════════════════════════

MDX Path: {current_path} → {expected_path}
YAML Source: {yaml_path}
Status: {status}

SECTION REVIEW
───────────────────────────────────────────────────────────────
[✓] Frontmatter - Complete
[✓] API Endpoint - Correct
[✗] Cost Breakdown - Fee amount incorrect (0.35 vs 0.27 ADA)
[✓] Request Body - Current
[!] Inputs - Missing wallet-inputs entry
[✓] Outputs - Complete
[✓] Minting - N/A
[!] Datum Changes - Missing after state
[✓] Reference Inputs - Complete
[✗] Notes - Outdated information

ISSUES FOUND
───────────────────────────────────────────────────────────────
1. [ERROR] Cost Breakdown: txFee should be 276274 lovelace (~0.27 ADA)
2. [WARN] Inputs: Missing wallet-inputs entry from YAML
3. [WARN] Datum: Missing "after" datum structure
4. [ERROR] Notes: Mentions old API endpoint format

RECOMMENDED ACTIONS
───────────────────────────────────────────────────────────────
[ ] Migrate file to correct path
[ ] Update cost breakdown with accurate fees
[ ] Add missing input entry
[ ] Add datum after state
[ ] Update notes with current info

To apply fixes: /v2-docs-review {transaction.id} --fix
═══════════════════════════════════════════════════════════════
```
</report-format>

<notes>
## Important Notes

1. **YAML is source of truth** - When YAML and MDX disagree, YAML wins
2. **Don't invent content** - Only include what's in the YAML
3. **Preserve custom notes** - Keep any MDX-specific insights not in YAML
4. **Update tracker** - After review, update `v2-docs-tracker.json`
5. **Create directories** - Ensure meta.json exists for navigation
6. **Test locally** - Run `npm run dev` to verify navigation works

## Related Skills

- `/v2-docs-audit` - Orchestrator for overall coverage
- `/analyze-transaction` - Creates YAML from CBOR
- `/transaction-audit` - Tracks CBOR analysis progress
</notes>