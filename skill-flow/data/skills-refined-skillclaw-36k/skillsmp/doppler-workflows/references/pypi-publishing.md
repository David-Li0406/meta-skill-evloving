**Skill**: [Doppler Credential Workflows](../SKILL.md)

## Use Case 1: PyPI Package Publishing

### Quick Start

```bash
# Publish package
doppler run --project claude-config --config dev \
  --command='uv publish --token "$PYPI_TOKEN"'
```

### Token Setup

**Doppler Storage:**

- Project: `claude-config`
- Config: `dev`
- Secret naming: `PYPI_TOKEN` (primary), `PYPI_TOKEN_{ABBREV}` (additional packages)

**Create New Token:**

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
# Step 1: Create project-scoped token on PyPI
# Go to: https://pypi.org/manage/account/token/
# Select specific project (NOT account-wide)

# Step 2: Store in Doppler (use stdin to avoid escaping)
echo -n 'pypi-AgEI...' | doppler secrets set PYPI_TOKEN_XXX \
  --project claude-config --config dev

# Step 3: Verify injection
doppler run --project claude-config --config dev \
  --command='echo "Length: ${#PYPI_TOKEN_XXX}"'
# Should show: 220-224 (valid token length)

# Step 4: Test publish
doppler run --project claude-config --config dev \
  --command='uv publish --token "$PYPI_TOKEN_XXX"'
VALIDATE_EOF
```

### PyPI Troubleshooting

**Issue: 403 Forbidden**

- Root cause: Token expired/revoked on PyPI
- Solution: Create new project-scoped token, update Doppler
- Verify: `doppler secrets get PYPI_TOKEN --plain | head -c 50` (should start with `pypi-AgEI`)

**Issue: Empty Token (Variable Not Expanding)**

- Root cause: Not using `--command` flag
- ❌ Wrong: `doppler run -- uv publish --token "$VAR"`
- ✅ Correct: `doppler run --command='uv publish --token "$VAR"'`

**Issue: Display vs Actual Value**

- `doppler secrets get` adds newline to display (formatting only)
- Actual value has NO newline when injected
- Verify: `doppler run --command='printf "%s" "$TOKEN" | wc -c'`
