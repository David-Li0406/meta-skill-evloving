**Skill**: [Code Clone Assistant](../SKILL.md)

## Detection Commands

### PMD CPD (Exact Duplicates)

```bash
# Markdown format (optimal for AI processing)
pmd cpd -d . -l python --minimum-tokens 20 -f markdown

# Multi-language projects (run separately per language)
pmd cpd -d . -l python --minimum-tokens 20 -f markdown > pmd-python.md
pmd cpd -d . -l ecmascript --minimum-tokens 20 -f markdown > pmd-js.md
```

**Tuning thresholds**:

- New codebases: 30-50 tokens
- Legacy codebases: 75-100 tokens (start high, lower gradually)

**Exclusions**:

```bash
pmd cpd -d . -l python --minimum-tokens 20 \
    --exclude="**/tests/**,**/node_modules/**,**/__pycache__/**" \
    -f markdown
```

### Semgrep (Pattern Violations)

```bash
# SARIF format (CI/CD standard)
semgrep --config=clone-rules.yaml --sarif --quiet

# Text format (human-readable)
semgrep --config=clone-rules.yaml --quiet

# Parse SARIF with jq
semgrep --config=clone-rules.yaml --sarif --quiet | \
    jq -r '.runs[0].results[] | "\(.ruleId): \(.message.text)"'
```

Full rules file: `./clone-rules.yaml`

______________________________________________________________________
