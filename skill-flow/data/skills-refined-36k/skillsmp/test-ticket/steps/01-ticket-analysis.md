# Step 1: Ticket Analysis

**Duration**: ~60 seconds
**Purpose**: Gather all sources of truth about what needs to be tested.

---

## Information Sources (Priority Order)

| Priority | Source | Purpose |
|----------|--------|---------|
| 1 | **Linear Ticket** | Requirements and acceptance criteria |
| 2 | **PR Description** | Implementation details (CRITICAL) |
| 3 | **Branch Code Changes** | Actual implementation to test |
| 4 | **Quoth Documentation** | Canonical test patterns (MANDATORY) |
| 5 | **Exolar Analytics** | Existing coverage and flaky history |

---

## Actions

### 1. Fetch Ticket from Linear MCP

Use the actual MCP tool name:

```
mcp__linear__get_issue({
  id: "{ticket-id}",
  includeRelations: true
})
```

**Response contains**:
```json
{
  "id": "c08f56d1-...",
  "identifier": "ENG-123",
  "title": "[BE] Feature implementation",
  "description": "...",
  "gitBranchName": "username/eng-123-feature-name",
  "status": "In Review",
  "labels": ["Feature", "API"],
  "attachments": [],
  "project": "Project Name",
  "team": "Engineering"
}
```

**Key fields**:
- `gitBranchName` - Branch to pull and analyze (CRITICAL)
- `description` - Primary requirements
- `labels` - Determines test type
- `attachments` - May contain PR links

---

### 2. Extract PR Description (CRITICAL SOURCE)

PR descriptions often contain implementation details not in the ticket:

```bash
# If gitBranchName exists, check for PR
gh pr view {gitBranchName} --json title,body,url,state

# Or search by branch name
gh pr list --head {gitBranchName} --json number,title,body,url
```

**PR body typically contains**:
- Implementation approach and decisions
- What was changed and why
- Testing notes from the developer
- Edge cases to consider

**Store PR info for test planning** - this is often more detailed than the ticket.

---

### 3. Pull the Branch (MANDATORY)

You MUST checkout the implementation branch to analyze actual code changes:

```bash
# Fetch latest from remote
git fetch origin

# Try to checkout the ticket branch
git checkout {gitBranchName}

# If branch doesn't exist, create test branch from main
git checkout main
git checkout -b test/{ticket-id}-automated-tests
```

**Why this is MANDATORY**:
- Tests must match actual implementation, not assumptions
- Code changes reveal what scenarios need testing
- Prevents generating tests for outdated code

---

### 4. Analyze Branch Changes (MANDATORY)

You MUST analyze what files were changed to understand test scope:

```bash
# List all changed files vs main
git diff main...HEAD --name-only

# See summary of changes
git diff main...HEAD --stat

# View specific file changes
git diff main...HEAD -- {file-path}
```

**What to look for**:
- **Components/Pages modified** - UI test targets
- **API endpoints changed** - API test targets
- **New files created** - New functionality to test
- **Test files already added** - Don't duplicate coverage
- **Config changes** - May affect test environment

**Read the changed files** to understand:
- Business logic that needs verification
- Error handling paths to test
- Integration points between components

---

### 5. Search Quoth for Test Patterns (MANDATORY)

Per project rules, you MUST search Quoth before generating tests:

```
mcp__quoth__quoth_search_index({
  query: "playwright test patterns for {feature-type}"
})
```

**Example queries**:
- `"playwright test patterns for authentication"`
- `"API integration test patterns"`
- `"form validation test patterns"`
- `"modal dialog test patterns"`

**Then read relevant docs**:
```
mcp__quoth__quoth_read_doc({
  doc_id: "{document-id-from-search}"
})
```

**Extract from documentation**:
- Canonical test structure
- Page object patterns used
- Fixture and helper usage
- Assertion patterns
- Common selectors and locators

---

### 6. Check Exolar for Existing Tests (RECOMMENDED)

Search for existing test coverage to avoid duplication:

```
mcp__exolar-qa__query_exolar_data({
  dataset: "test_search",
  filters: { query: "{feature-name}" }
})
```

**Check for flaky tests in this area**:
```
mcp__exolar-qa__query_exolar_data({
  dataset: "flaky_tests",
  filters: { min_runs: 5 }
})
```

**What to learn**:
- Tests that already exist for this feature
- Flaky tests to avoid similar patterns
- Test execution history and reliability

---

### 7. Determine Test Type Based on Labels

| Labels | Test Type | Location |
|--------|-----------|----------|
| `feature`, `ui` | E2E UI Tests | `automation/playwright/tests/{feature}/` |
| `bug`, `ui` | E2E Regression | `automation/playwright/tests/{feature}/` |
| `api`, `backend` | API Integration | `automation/playwright/tests/{feature}-api/` |
| `performance` | Load Tests | `automation/playwright/tests/performance/` |

---

### 8. Consolidate All Requirements

Before proceeding, ensure you have:

- [ ] Ticket description and acceptance criteria
- [ ] PR description (if exists)
- [ ] List of changed files
- [ ] Understanding of code changes
- [ ] Quoth patterns for this test type
- [ ] Exolar existing test coverage
- [ ] Determined test type and location

---

## Output

Generate analysis document: `docs/test-analysis/{ticket-id}.md`

**Document Structure**:
```markdown
# Test Analysis: {TICKET-ID}

## Ticket Summary
- **Title**: {title}
- **Type**: {feature|bug|api}
- **Labels**: {labels}
- **Branch**: {gitBranchName}
- **PR**: {pr-url if exists}

## Sources Analyzed
- [x] Linear ticket description
- [x] PR description: {summary of implementation approach}
- [x] Branch changes: {number} files modified
- [x] Quoth patterns: {patterns found}
- [x] Exolar coverage: {existing tests found}

## Code Changes Summary
### Modified Files
- `src/components/Feature.tsx` - Main component logic
- `src/api/endpoint.ts` - API integration
- `src/utils/validation.ts` - Validation helpers

### Key Implementation Details
{Summary of what the code actually does based on reading changed files}

## Acceptance Criteria
1. {criterion 1}
2. {criterion 2}
3. {criterion 3}

## Test Requirements
- **Test type**: {E2E UI|API Integration|Both}
- **Target directory**: {path}
- **Page objects needed**: {list}
- **Fixtures needed**: {list}

## Quoth Patterns to Follow
- Pattern: {pattern-name} from {doc-id}
- Pattern: {pattern-name} from {doc-id}

## Existing Test Coverage (from Exolar)
- {existing-test-1}: {status}
- {existing-test-2}: {status}

## Risks and Edge Cases
- {edge case from PR description}
- {error handling scenario from code analysis}
```

---

## MCP Tools Used

| MCP Server | Tool | Purpose |
|------------|------|---------|
| **linear** | `mcp__linear__get_issue` | Fetch ticket details |
| **quoth** | `mcp__quoth__quoth_search_index` | Search test patterns |
| **quoth** | `mcp__quoth__quoth_read_doc` | Read specific patterns |
| **exolar** | `mcp__exolar-qa__query_exolar_data` | Check existing tests |

---

## Error Handling

### Ticket Not Found
```
Error: Linear ticket {ticket-id} not found
```
**Solutions**:
- Verify ticket ID format (PREFIX-NUMBER)
- Check workspace configuration
- Ensure Linear MCP has correct permissions

### Branch Not Found
```
Warning: Branch {gitBranchName} not found on remote
```
**Actions**:
- Create new branch: `test/{ticket-id}-automated-tests`
- Proceed with ticket description only (less ideal)
- Note in analysis that code changes were not available

### PR Not Found
```
Warning: No PR found for branch {gitBranchName}
```
**Actions**:
- Proceed without PR description
- Rely more heavily on code change analysis
- Note in analysis that PR details were not available

### Quoth Not Connected
```
Warning: Quoth MCP not available - patterns will not be enforced
```
**Actions**:
- Warn user that tests may not follow canonical patterns
- Proceed with best-effort pattern matching
- Recommend manual review of generated tests

### No Labels Found
```
Warning: No labels found, defaulting to E2E UI tests
```
**Actions**:
- Infer test type from code changes
- Default to E2E UI tests
- Manual review recommended after generation

---

## Next Step

Once analysis is complete, proceed to [Step 2: Pattern Search](./02-pattern-search.md).
