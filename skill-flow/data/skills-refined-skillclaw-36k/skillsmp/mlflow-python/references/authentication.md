**Skill**: [MLflow Python](../SKILL.md)

# Authentication Patterns

Idiomatic MLflow authentication using separate environment variables.

## Correct Pattern (Recommended)

MLflow uses **separate environment variables** for credentials:

```bash
# .env.local (gitignored)
MLFLOW_TRACKING_URI=http://mlflow.eonlabs.com:5000
MLFLOW_TRACKING_USERNAME=eonlabs
MLFLOW_TRACKING_PASSWORD=<password>
```

The MLflow Python client automatically reads these variables.

## Why Not Embedded URI?

Some documentation shows credentials in the URI:

```bash
# NOT RECOMMENDED - non-idiomatic
MLFLOW_TRACKING_URI=http://user:pass@mlflow.server.com:5000
```

This pattern:

- Is not officially documented by MLflow
- May break with special characters in passwords
- Leaks credentials in logs and stack traces
- Doesn't work consistently across all MLflow versions

## mise Configuration

Use mise `[env]` as the Single Source of Truth:

```toml
# .mise.toml
[env]
MLFLOW_TRACKING_URI = "http://localhost:5000"
MLFLOW_DEFAULT_EXPERIMENT = "default"

# Load secrets from .env.local (gitignored)
_.file = { path = ".env.local", redact = true }
```

Create `.env.local` for credentials:

```bash
MLFLOW_TRACKING_URI=http://mlflow.eonlabs.com:5000
MLFLOW_TRACKING_USERNAME=eonlabs
MLFLOW_TRACKING_PASSWORD=your_password_here
```

## Verification

Test authentication with:

```bash
/usr/bin/env bash << 'AUTHENTICATION_SCRIPT_EOF'
cd ${CLAUDE_PLUGIN_ROOT}/skills/mlflow-python
uv run scripts/query_experiments.py experiments
AUTHENTICATION_SCRIPT_EOF
```

Expected output: List of experiments on the server.

## Troubleshooting

| Error                 | Cause                    | Fix                                   |
| --------------------- | ------------------------ | ------------------------------------- |
| 401 Unauthorized      | Wrong credentials        | Check `.env.local` values             |
| Connection refused    | Server not reachable     | Verify `MLFLOW_TRACKING_URI`          |
| No experiments found  | Wrong server or new user | Create experiment first               |
| SSL certificate error | HTTPS without valid cert | Use HTTP or configure SSL certificate |
