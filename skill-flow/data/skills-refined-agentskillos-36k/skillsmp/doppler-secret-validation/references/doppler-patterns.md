**Skill**: [Doppler Secret Validation](../SKILL.md)

# Doppler CLI Patterns

Common patterns for working with Doppler secrets management.

## Basic Operations

### List Projects

```bash
doppler projects
```

### List Configs in Project

```bash
doppler configs --project PROJECT_NAME
```

### List Secrets in Config

```bash
# Table view
doppler secrets --project PROJECT --config CONFIG

# Names only
doppler secrets --project PROJECT --config CONFIG --only-names
```

### Get Single Secret

```bash
# Plain text (for scripting)
doppler secrets get SECRET_NAME --project PROJECT --config CONFIG --plain

# Table view (masked)
doppler secrets get SECRET_NAME --project PROJECT --config CONFIG
```

### Set Secret

```bash
doppler secrets set SECRET_NAME="value" --project PROJECT --config CONFIG
```

**Note**: Doppler CLI doesn't support `--note` flag. Add notes via dashboard:
1. Go to https://dashboard.doppler.com
2. Navigate: PROJECT → CONFIG → SECRET_NAME
3. Click "Edit" → Add note

## Environment Injection

### Run Command with Secrets

```bash
# Doppler injects all secrets as environment variables
doppler run --project PROJECT --config CONFIG -- COMMAND
```

**Examples**:

```bash
# Run Python script
doppler run --project claude-config --config prd -- python script.py

# Run with uv
doppler run --project claude-config --config prd -- uv run script.py

# Run shell command
doppler run --project claude-config --config prd -- bash -c 'echo $SECRET_NAME'
```

### Export Secret to Environment

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# Export for current shell
export SECRET_NAME=$(doppler secrets get SECRET_NAME \
  --project PROJECT --config CONFIG --plain)

# Use in commands
command --token $SECRET_NAME
CONFIG_EOF
```

## Validation Workflow

### 1. Add Secret

```bash
doppler secrets set PYPI_TOKEN="pypi-..." \
  --project claude-config --config prd
```

### 2. Verify Storage

```bash
# Check exists
doppler secrets --project claude-config --config prd | grep PYPI_TOKEN

# Retrieve value
doppler secrets get PYPI_TOKEN --project claude-config --config prd --plain
```

### 3. Test Retrieval

```bash
/usr/bin/env bash << 'CONFIG_EOF_2'
TOKEN=$(doppler secrets get PYPI_TOKEN --project claude-config --config prd --plain)
echo "Length: ${#TOKEN}"
CONFIG_EOF_2
```

### 4. Test Environment Injection

```bash
/usr/bin/env bash << 'CONFIG_EOF_3'
doppler run --project claude-config --config prd -- \
  bash -c 'echo "Token available: ${PYPI_TOKEN:0:20}..."'
CONFIG_EOF_3
```

## Tool Integration Patterns

### uv Publish

```bash
/usr/bin/env bash << 'CONFIG_EOF_4'
# Method 1: Doppler auto-injects PYPI_TOKEN
doppler run --project claude-config --config prd -- uv publish

# Method 2: Manual export
export PYPI_TOKEN=$(doppler secrets get PYPI_TOKEN \
  --project claude-config --config prd --plain)
uv publish --token $PYPI_TOKEN
CONFIG_EOF_4
```

### twine Upload

```bash
/usr/bin/env bash << 'CONFIG_EOF_5'
# Method 1: Doppler run (uses PYPI_TOKEN as password)
doppler run --project claude-config --config prd -- \
  twine upload dist/* --username __token__

# Method 2: Manual export
export TWINE_PASSWORD=$(doppler secrets get PYPI_TOKEN \
  --project claude-config --config prd --plain)
export TWINE_USERNAME=__token__
twine upload dist/*
CONFIG_EOF_5
```

### GitHub Actions

```yaml
- name: Setup Doppler
  uses: dopplerhq/secrets-fetch-action@v1.3.0
  with:
    doppler-token: ${{ secrets.DOPPLER_TOKEN }}
    doppler-project: claude-config
    doppler-config: prd

- name: Use Secret
  run: uv publish
  env:
    PYPI_TOKEN: ${{ steps.doppler.outputs.PYPI_TOKEN }}
```

## Security Best Practices

### 1. Never Log Secrets

```bash
/usr/bin/env bash << 'DOPPLER_PATTERNS_SCRIPT_EOF'
# ✗ BAD: Logs secret
echo "Token: $PYPI_TOKEN"

# ✓ GOOD: Masks secret
echo "Token: ${PYPI_TOKEN:0:20}..."
DOPPLER_PATTERNS_SCRIPT_EOF
```

### 2. Use --plain for Scripts Only

```bash
# ✗ BAD: Human-readable shows secret
doppler secrets get TOKEN --project foo --config bar

# ✓ GOOD: Plain text for piping to commands
doppler secrets get TOKEN --project foo --config bar --plain | command
```

### 3. Prefer doppler run Over Export

```bash
/usr/bin/env bash << 'CONFIG_EOF_6'
# ✓ BEST: Scoped to single command
doppler run --project foo --config bar -- command

# ⚠ OK: Exported to shell session (risk if shell shared)
export TOKEN=$(doppler secrets get TOKEN --project foo --config bar --plain)
CONFIG_EOF_6
```

### 4. Use Separate Configs for Environments

```
project/
├── dev     (development secrets)
├── stg     (staging secrets)
└── prd     (production secrets)
```

## Common Token Types

### API Tokens

**Format**: Usually `prefix-base64string`
- PyPI: `pypi-AgEI...` (179 chars)
- GitHub: `ghp_...` (40+ chars)
- Quarto: `qpa_...` (variable length)

**Validation**: Check prefix, length, and test authentication

### Service Credentials

**Format**: Username/password pairs or JSON keys
- Store as separate secrets: `SERVICE_USER`, `SERVICE_PASS`
- Or as single JSON: `SERVICE_CREDENTIALS`

## Troubleshooting

### Secret Not Found

```bash
# Check spelling
doppler secrets --project foo --config bar --only-names

# Check you're in right project/config
doppler whoami
```

### Permission Denied

```bash
# Re-authenticate
doppler login

# Check project access
doppler projects
```

### Command Timeout

```bash
# Increase timeout (if supported by command)
timeout 30 doppler secrets get TOKEN --project foo --config bar --plain
```

## Reference

- Official docs: https://docs.doppler.com/docs
- CLI reference: https://docs.doppler.com/docs/cli
- Install: `brew install dopplerhq/cli/doppler`
