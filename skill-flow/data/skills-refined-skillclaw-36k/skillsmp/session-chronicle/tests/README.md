# Session Chronicle Tests

Validation scripts and fixtures for session-chronicle S3 artifact sharing.

**ADR**: [Session Chronicle S3 Sharing](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md)

## Running Validations

Run all validations:

```bash
cd plugins/devops-tools/skills/session-chronicle
bash tests/scripts/validate-e2e.sh
```

Run individual validations:

```bash
bash tests/scripts/validate-prerequisites.sh
bash tests/scripts/validate-brotli.sh
bash tests/scripts/validate-credential-access.sh
bash tests/scripts/validate-s3-upload.sh
bash tests/scripts/validate-extract-chain.sh
bash tests/scripts/validate-commit-format.sh
bash tests/scripts/validate-cross-references.sh
```

## Validation Scripts

| Script                          | Purpose                          |
| ------------------------------- | -------------------------------- |
| `validate-prerequisites.sh`     | Tool installation check          |
| `validate-brotli.sh`            | Compression round-trip test      |
| `validate-credential-access.sh` | 1Password access verification    |
| `validate-s3-upload.sh`         | S3 connectivity test             |
| `validate-extract-chain.sh`     | Script modification check        |
| `validate-commit-format.sh`     | Commit message format validation |
| `validate-cross-references.sh`  | Cross-reference integrity check  |
| `validate-e2e.sh`               | Master validation runner         |

## Test Fixtures

| File                     | Description                   |
| ------------------------ | ----------------------------- |
| `mock-session.jsonl`     | Synthetic Claude Code session |
| `mock-uuid-chain.jsonl`  | Pre-traced UUID chain         |
| `expected-manifest.json` | Expected manifest output      |

## Prerequisites

```bash
brew install brotli awscli 1password-cli jq
op signin
```

## Validation Execution Order

```
1. validate-prerequisites.sh      → Tool installation check
2. validate-brotli.sh             → Compression round-trip
3. validate-credential-access.sh  → 1Password access
4. validate-s3-upload.sh          → AWS connectivity
5. validate-extract-chain.sh      → Script modification check
6. validate-commit-format.sh      → Output format check
7. validate-cross-references.sh   → Cross-reference integrity
8. validate-e2e.sh                → Full integration
```

## Use Cases

- **Regression testing**: Re-run after any changes to session-chronicle
- **Onboarding**: New contributors can verify their setup
- **CI-local validation**: Manual pre-push checks
- **Documentation**: Scripts serve as executable documentation
