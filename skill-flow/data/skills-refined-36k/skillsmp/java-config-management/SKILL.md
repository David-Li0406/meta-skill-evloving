---
name: java-config-management
description: Build a deterministic configuration system with layering (env, files, flags, secrets), strong validation, and operational runbooks. Use when deploying to multiple environments, handling config drift, or improving safety for secrets and defaults.
license: MIT
compatibility: JDK 17+ (recommended 21), any runtime (VM/container/Kubernetes), any framework
metadata:
  owner: platform
  version: "1.0"
  tags: [java, config, envvars, secrets, validation, operations]
---

# Java Configuration Management (Layering + Validation + Runbook)

## Scope

**In scope**

- Configuration layering model: defaults -> config files -> environment variables -> runtime overrides.
- Strong typing + validation at startup (fail fast).
- Secrets handling guidance (inject at runtime, avoid leakage).
- Operational runbooks (how to set/change config safely).
- Safe defaults, backward-compatible config evolution, and deprecation strategy.

**Out of scope**

- Choosing a single config library for all projects (we provide patterns).
- Organization-wide secret store selection (Vault/KMS/etc).

## Core mental model

Configuration is a product interface for operators. Treat config like an API:

- It must be documented.
- It must be validated.
- It must evolve compatibly.

## Layering and precedence (recommended default)

From lowest to highest precedence:

1. **Hardcoded defaults** (safe, minimal, non-secret)
2. **Versioned config files** (non-secret; environment-specific overlays allowed)
3. **Environment variables** (deployment-time overrides; keep minimal)
4. **Secrets injection** (never committed; runtime-mounted or fetched)
5. **Runtime flags** (emergency toggles; audited)

Rule: the **higher** the layer, the **smaller** it should be.

### Why not “everything in env”?

Environment variables are convenient but can leak via process inspection, crash dumps, logs, or misconfigured tooling. Use them for non-secret toggles and endpoints, not for long-lived secrets.

## Configuration contract

### Recommended structure (example)

- `server.port` (int, default 8080)
- `db.url` (string, required)
- `db.pool.maxSize` (int, default 20)
- `auth.jwt.issuer` (string, required)
- `featureFlags.newCheckout` (bool, default false)
- `timeouts.httpClient.connectMs` (int, default 200)
- `timeouts.httpClient.readMs` (int, default 1000)

### Naming conventions

- Use dot-separated keys: `domain.subdomain.key`.
- Avoid duplicated meaning: do not mix `dbMaxPool` and `db.pool.maxSize`.
- For env vars: map to uppercase with underscores:
  - `DB_POOL_MAX_SIZE` -> `db.pool.maxSize` (document mapping rules).

## Validation (fail fast)

### Startup validation checklist

- Required fields present.
- Range checks: ports, timeouts, pool sizes.
- Cross-field checks:
  - if `featureFlags.x=true` then `xConfig.*` must be present.
- URL formats, file path existence, enum values.
- Secret presence without printing secret values.

### Recommended approach (framework-agnostic)

1. Load raw config into a typed object (`AppConfig`).
2. Validate using a validator (e.g., Bean Validation style constraints).
3. If validation fails:
   - log a safe summary (missing keys, invalid ranges)
   - exit non-zero.

## Secrets handling (must-have rules)

1. Never commit secrets into Git.
2. Never log secrets.
3. Prefer runtime injection:
   - mount secret files (tmpfs/in-memory volume) or
   - fetch from a secret store using identity (short-lived credentials).
4. Rotate secrets:
   - support reload where possible, or restart safely.
5. Protect access:
   - least privilege and auditing.

### Kubernetes (if applicable)

- Use Secrets with encryption-at-rest enabled.
- Minimize secret distribution; mount only where needed.

## Default values and backward compatibility

- Provide safe defaults for non-critical settings.
- Introduce new config keys with defaults first (“expand”).
- Deprecate old keys with warnings.
- Remove keys only after one full release cycle (or your policy).

## Operational runbook (template)

### 1) Discover current config

- Identify environment (dev/staging/prod).
- Enumerate config sources and precedence.
- Confirm effective values (do not print secrets).

### 2) Change process

- Make change in the lowest appropriate layer.
- Prefer config file/overlay change over ad-hoc env var tweaks.
- Use a change request with:
  - reason
  - risk assessment
  - rollback plan
  - owner

### 3) Rollout

- Canary or staged deployment.
- Validate health checks and SLOs.
- If rollback: revert only the changed layer.

### 4) Post-change validation

- Confirm metrics/logs/traces show expected behavior.
- Document change in a changelog/runbook.

## Outputs / artifacts

- `docs/config.md` (full contract + mapping rules)
- `config/defaults.yml` (or equivalent)
- `config/<env>.yml` overlays (non-secret)
- `runbooks/config-operations.md`
- `tests/config-validation-test.*`

## Definition of Done (DoD)

- [ ] Configuration contract documented (keys, types, defaults, required).
- [ ] Layering precedence implemented and deterministic.
- [ ] Startup validation fails fast with safe messages.
- [ ] Secrets never committed and never logged.
- [ ] Runbook exists with change + rollback steps.

## Guardrails (What NOT to do)

- Never log `System.getenv()` wholesale.
- Never put secrets in config files committed to Git.
- Avoid “silent fallback” for required keys (must fail fast).
- Avoid per-service ad-hoc naming schemes (increases operator burden).

## Common failure modes & fixes

- Symptom: config drift across environments -> Fix: centralize overlays; reduce env var sprawl.
- Symptom: “works on my machine” -> Fix: document precedence; add “effective config dump” (redacted).
- Symptom: secret leaked in logs -> Fix: add redaction filters; audit logging statements.

## References (see references/)

- `references/config-contract-template.md`
- `references/secrets-hygiene.md`
- `references/runbook-template.md`
