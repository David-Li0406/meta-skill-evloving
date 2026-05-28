**Skill**: [Code Clone Assistant](../SKILL.md)


## Complete Detection Workflow

### Phase 1: Detection

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Create working directory
mkdir -p /tmp/dry-audit-$(date +%Y%m%d)
cd /tmp/dry-audit-$(date +%Y%m%d)

# Run both tools
pmd cpd -d /path/to/project -l python --minimum-tokens 20 -f markdown > pmd-cpd.md
semgrep --config=/path/to/clone-rules.yaml --sarif --quiet /path/to/project > semgrep.sarif
CONFIG_EOF
```

### Phase 2: Analysis

```bash
# Parse PMD CPD (direct read - LLM-native format)
cat pmd-cpd.md

# Parse Semgrep SARIF
jq -r '.runs[0].results[] | "\(.ruleId): \(.message.text) at \(.locations[0].physicalLocation.artifactLocation.uri):\(.locations[0].physicalLocation.region.startLine)"' semgrep.sarif
```

**Combine findings**:

1. List PMD CPD duplications by severity (tokens/lines)
1. List Semgrep violations by file
1. Prioritize: Exact duplicates across files > Large within-file > Patterns

### Phase 3: Presentation

Present to user:

- Total violations (PMD + Semgrep)
- Breakdown by type (exact vs pattern)
- Files affected
- Estimated refactoring effort
- Suggested approach

**Example**:

```
DRY Audit Results:
==================
PMD CPD: 9 exact duplications
Semgrep: 21 pattern violations
Total: ~27 unique DRY violations

Top Issues:
1. process_user_data() duplicated in file1.py:5 and file2.py:5 (21 lines)
2. Duplicate validation logic across 6 locations (Semgrep)
3. Error collection pattern repeated 5 times (Semgrep)

Recommended Refactoring:
- Extract process_user_data() to shared utils module
- Create validate_input() function for validation logic
- Create ErrorCollector class for error handling

Proceed with refactoring? (y/n)
```

### Phase 4: Refactoring (With User Approval)

1. Read affected files using Read tool
1. Create shared functions/classes
1. Replace duplicates using Edit tool
1. Run tests using Bash tool
1. Commit changes if tests pass

______________________________________________________________________

## Best Practices

**DO**:

- ✅ Run both PMD CPD and Semgrep (complementary coverage)
- ✅ Start with conservative thresholds (PMD: 50 tokens)
- ✅ Review results before refactoring
- ✅ Run full test suite after refactoring
- ✅ Commit incrementally

**DON'T**:

- ❌ Only use one tool (miss ~70% of violations)
- ❌ Set thresholds too low (noise overwhelms signal)
- ❌ Refactor without understanding context
- ❌ Skip test verification
