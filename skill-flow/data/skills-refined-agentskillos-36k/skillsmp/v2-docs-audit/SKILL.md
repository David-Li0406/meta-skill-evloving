---
name: v2-docs-audit
description: Orchestrate V2 transaction MDX documentation coverage and quality tracking
---

<introduction>
This skill is the **documentation manager** for V2 transaction MDX files in `content/docs/protocol/v2/transactions/`. It tracks documentation coverage, identifies gaps, and coordinates review work.

**Documentation Location**: `content/docs/protocol/v2/transactions/`

**Worker Skill**: Use `/v2-docs-review` to review individual transaction documentation.

**Tracker File**: `.claude/skills/v2-docs-audit/v2-docs-tracker.json`

**Related Skills**:
- `/transaction-audit` - Tracks CBOR analysis and YAML creation
- `/analyze-transaction` - Creates YAML + TypeScript from CBOR
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

## Commands

| Command | Description |
|---------|-------------|
| `/v2-docs-audit` | Show dashboard and coverage status |
| `/v2-docs-audit scan` | Rescan documentation directory |
| `/v2-docs-audit status` | Show summary counts only |
| `/v2-docs-audit next` | Suggest next documentation task |
| `/v2-docs-audit review <id>` | Run /v2-docs-review for specific tx |
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

<tracker-format>
## Tracker File Structure

```json
{
  "version": "1.0.0",
  "lastUpdated": "YYYY-MM-DD",
  "docsPath": "content/docs/protocol/v2/transactions",
  "summary": {
    "documented": N,
    "missing": N,
    "path-mismatch": N,
    "needs-review": N,
    "reviewed": N,
    "verified": N
  },
  "transactions": [
    {
      "id": "system.role.action",
      "endpoint": "/v2/tx/...",
      "system": "global|instance|course|project",
      "role": "general|owner|teacher|student|manager|contributor",
      "expectedPath": "path/to/expected.mdx",
      "currentPath": "path/to/current.mdx" | null,
      "status": "missing|path-mismatch|needs-review|reviewed|verified",
      "lastReviewed": "YYYY-MM-DD" | null,
      "yamlSource": "path/to/source.yaml" | null,
      "issues": ["list of known issues"],
      "notes": "..."
    }
  ]
}
```
</tracker-format>

<dashboard-format>
## Dashboard Output Format

```
═══════════════════════════════════════════════════════════════
              V2 DOCUMENTATION COVERAGE DASHBOARD
═══════════════════════════════════════════════════════════════

Last Updated: YYYY-MM-DD
Docs Path: content/docs/protocol/v2/transactions/

SUMMARY
───────────────────────────────────────────────────────────────
Total: 17 | Documented: 8 | Missing: 9 | Path Issues: 6

BY SYSTEM
───────────────────────────────────────────────────────────────
Global (1):     ██████████░░░░░░░░░░  50% [1/1] ⚠️ path mismatch
Instance (2):   ██████████░░░░░░░░░░  50% [1/2]
Course (6):     ████████████████████ 100% [6/6] ⚠️ 5 path mismatches
Project (8):    ░░░░░░░░░░░░░░░░░░░░   0% [0/8]

DOCUMENTATION STATUS
───────────────────────────────────────────────────────────────
[✓] global.general.access-token.mint     ⚠️ Wrong path
[✓] instance.owner.course.create         ⚠️ Wrong path
[✗] instance.owner.project.create        Missing
[✓] course.owner.teachers.manage         ⚠️ Wrong path
[✓] course.teacher.modules.manage        ⚠️ Wrong path
[✓] course.teacher.assignments.assess    ⚠️ Wrong path
[✓] course.student.enroll                OK
[✓] course.student.assignment.action     ⚠️ Wrong path
[✓] course.student.credential.claim      ⚠️ Wrong path
[✗] project.owner.managers.manage        Missing
...

PRIORITY ACTIONS
───────────────────────────────────────────────────────────────
1. Migrate 6 files to correct paths
2. Create instance/owner/project/create.mdx
3. Create 8 project transaction docs

To review: /v2-docs-review <transaction-id>
═══════════════════════════════════════════════════════════════
```
</dashboard-format>

<notes>
## Important Notes

1. **Path alignment is mandatory** - All MDX files must match API URL structure
2. **YAML is source of truth** - MDX content should align with analyzed YAML files
3. **Update index.mdx** - When adding new transactions, update the index page
4. **Create meta.json** - Each directory needs a meta.json for navigation
5. **tx_file frontmatter** - Links MDX to YAML for diagram rendering

## Related Files

- `v2-transaction-tracker.json` - CBOR analysis status (different tracker)
- `address-registry.json` - Validator/policy names
- YAML files in `public/yaml/transactions/v2/`
</notes>
