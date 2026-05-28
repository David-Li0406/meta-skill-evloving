---
name: v2-docs-review
description: Review individual V2 transaction MDX documentation for coverage and accuracy
---

<introduction>
This skill reviews individual V2 transaction MDX documentation files for completeness and accuracy. It compares MDX content against the analyzed YAML source files.

**Orchestrator Skill**: `/v2-docs-audit` tracks overall documentation coverage.

**Source of Truth**: YAML files in `public/yaml/transactions/v2/`

**Output**: Updated MDX files in `content/docs/protocol/v2/transactions/`
</introduction>

<workflow>
## When Invoked

1. **Identify Transaction**
   - User specifies transaction ID (e.g., `course.student.enroll`)
   - Look up in v2-docs-tracker.json for current state

2. **Gather Sources**
   - Read the YAML source file (if exists)
   - Read the current MDX file (if exists)
   - Read address-registry.json for validator names

3. **Perform Review**
   - Compare MDX content against YAML
   - Check all required sections are present
   - Verify accuracy of costs, endpoints, schemas
   - Note any discrepancies

4. **Generate Report**
   - List what's correct
   - List what's missing
   - List what's incorrect
   - Provide specific fixes needed

5. **Offer Actions**
   - Create new MDX if missing
   - Update existing MDX with fixes
   - Migrate file to correct path if needed

## Invocation

```
/v2-docs-review course.student.enroll
```

Or with action:
```
/v2-docs-review course.student.enroll --fix
/v2-docs-review course.student.enroll --create
/v2-docs-review course.student.enroll --migrate
```
</workflow>

<review-checklist>
## Review Checklist

### Frontmatter
- [ ] `title` - Clear, descriptive title
- [ ] `description` - One-line summary
- [ ] `tx_file` - Points to correct YAML file path

### API Endpoint Section
- [ ] Endpoint path matches API (`/v2/tx/{system}/{role}/{action}`)
- [ ] Method is POST

### Cost Breakdown Table
- [ ] Transaction Fee matches YAML `costs.txFee`
- [ ] Protocol Fee matches YAML `costs.protocolFee`
- [ ] MinUTxO values match YAML `costs.minUtxo`
- [ ] Wallet Delta calculation is correct
- [ ] Notes about recoverable deposits if applicable

### Request Body Section
- [ ] JSON example uses current field names from YAML `request_body`
- [ ] Required vs optional fields are correct
- [ ] Field descriptions match YAML
- [ ] Example values are realistic

### Transaction Pattern
- [ ] Pattern correctly identified (Mint/Spend/Burn)
- [ ] Brief explanation of what happens

### Inputs Table
- [ ] All inputs from YAML are listed
- [ ] Validator names match address-registry.json
- [ ] Descriptions are accurate

### Outputs Table
- [ ] All outputs from YAML are listed
- [ ] Values match YAML (lovelace amounts, tokens)
- [ ] Validator addresses are correct

### Minting Operations (if applicable)
- [ ] All mints from YAML are listed
- [ ] Policy names match address-registry.json
- [ ] Token names and quantities are correct

### Datum Changes Section
- [ ] Shows before/after datum structures
- [ ] Constructor numbers are correct
- [ ] Field descriptions match YAML

### Reference Inputs
- [ ] All reference inputs listed
- [ ] Descriptions explain purpose

### Notes Section
- [ ] Key insights from YAML `design_notes`
- [ ] Any caveats or important behaviors
</review-checklist>

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

<path-rules>
## Path Rules

### File Path
MDX file path must match API endpoint structure:
- API: `/v2/tx/{system}/{role}/{action}`
- MDX: `content/docs/protocol/v2/transactions/{system}/{role}/{action}.mdx`

### tx_file Frontmatter
Points to YAML source (relative to `public/yaml/transactions/v2/`):
- YAML: `public/yaml/transactions/v2/{system}/{role}/{action}.yaml`
- tx_file: `{system}/{role}/{action}.yaml`

### Examples

| Transaction | MDX Path | tx_file |
|-------------|----------|---------|
| course.student.assignment.commit | course/student/assignment/commit.mdx | course/student/assignment/commit.yaml |
| course.teacher.assignments.assess | course/teacher/assignments/assess.mdx | course/teacher/assignments/assess.yaml |
| global.general.access-token.mint | global/general/access-token/mint.mdx | global/general/access-token/mint.yaml |
</path-rules>

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
4. **Update tracker** - After review, update v2-docs-tracker.json
5. **Create directories** - Ensure meta.json exists for navigation
6. **Test locally** - Run `npm run dev` to verify navigation works

## Related Skills

- `/v2-docs-audit` - Orchestrator for overall coverage
- `/analyze-transaction` - Creates YAML from CBOR
- `/transaction-audit` - Tracks CBOR analysis progress
</notes>
