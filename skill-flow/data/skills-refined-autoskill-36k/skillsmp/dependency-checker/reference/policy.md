# Dependency Policy & Commands

## Version Pinning Rules

| Type | Format | Example | When to Use |
|------|--------|---------|-------------|
| Exact | `==` | `requests==2.31.0` | Production |
| Bounded | `>=,<` | `flask>=2.0,<3.0` | Dev dependencies |
| Minimum | `>=` | `pytest>=7.0` | Dev only (not recommended) |
| None | (blank) | `requests` | ❌ Never |

---

## Priority Guidelines

| Severity | Response Time | Action |
|----------|---------------|--------|
| CRITICAL | 24 hours | Block deployment, fix immediately |
| HIGH | 1 week | Schedule urgent fix |
| MEDIUM | 1 month | Include in next release |
| LOW | Quarterly | Review and plan |

---

## Common Commands

### Security Audit

```bash
# Primary (recommended)
pip-audit -r requirements.txt

# Alternative
pip install safety && safety check -r requirements.txt

# JSON output for CI
pip-audit -r requirements.txt --format json
```

### Check Outdated

```bash
# List outdated
pip list --outdated

# JSON format
pip list --outdated --format json

# Specific package
pip show package-name
```

### Dependency Analysis

```bash
# Check conflicts
pip check

# Dependency tree
pip install pipdeptree && pipdeptree

# Specific package tree
pipdeptree -p package-name
```

### Lock File Management

```bash
# Generate lock
pip freeze > requirements.lock

# Install from lock (reproducible)
pip install -r requirements.lock

# Compare
diff requirements.txt requirements.lock
```

---

## Remediation Steps

### Critical Vulnerability

```bash
# 1. Identify fixed version
pip-audit -r requirements.txt

# 2. Update package
pip install package-name==fixed-version

# 3. Update requirements.txt
sed -i 's/package==old/package==new/' requirements.txt

# 4. Test
pytest tests/ -v

# 5. Regenerate lock
pip freeze > requirements.lock
```

### Unpinned Dependency

```bash
# 1. Check current version
pip show package-name | grep Version

# 2. Pin in requirements.txt
echo "package-name==X.Y.Z" >> requirements.txt
```

### Conflict Resolution

```bash
# 1. Identify conflict
pip check

# 2. Update conflicting package
pip install package-name==compatible-version

# 3. Verify
pip check
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip-audit` not found | `pip install pip-audit` |
| Vulnerability DB outdated | `pip install --upgrade pip-audit` |
| Timeout during audit | Add `--timeout 300` flag |
| Lock file out of sync | `pip freeze > requirements.lock` |

---

## Adding New Dependencies

1. Check license compatibility (MIT, Apache 2.0, BSD preferred)
2. Review project maintenance (recent commits?)
3. Check for known vulnerabilities
4. Evaluate alternatives (fewer deps = less risk)
5. Document rationale in PR
