# Commands Reference

## CI Commands

```bash
# TypeScript checking
npm run typecheck

# ESLint
npm run lint

# ESLint auto-fix
npm run lint -- --fix

# Unit + integration tests
npm run test:unit -- --run
```

## E2E Tests

Use these exact flags:
```bash
npx playwright test --workers=3 --retries=3 --timeout=1800000 --reporter=line
```

| Flag | Purpose |
|------|---------|
| `--workers=3` | Run 3 tests in parallel |
| `--retries=3` | Retry failed tests up to 3 times |
| `--timeout=1800000` | 30 minute timeout per test |
| `--reporter=line` | Minimal output format |

## Selective Testing

```bash
# Run specific unit test
npm run test:unit -- --run <file>

# Run specific E2E test
npx playwright test <spec-file> --retries=3
```

## Git Commands

```bash
# Check status
git status --short

# Stage specific files
git add <file>

# Commit with message
git commit -m "message"

# Show recent commits
git log --oneline -5
```

## Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
<type>: <description>

<body explaining changes>

Tests: <unit count> passed, <e2e count> passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructure
- `test`: Adding tests
- `docs`: Documentation
- `chore`: Maintenance
