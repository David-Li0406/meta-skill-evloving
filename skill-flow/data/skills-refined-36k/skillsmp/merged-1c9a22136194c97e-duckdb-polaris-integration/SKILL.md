---
name: duckdb-polaris-integration
description: Use this skill when building data lakehouses with DuckDB and managing Polaris catalogs, including configuration, integration, and debugging access control issues.
---

# DuckDB and Polaris Catalog Integration

This skill provides patterns for building modern data lakehouses using **DuckDB** as ephemeral compute and **Polaris** for catalog-managed storage. It covers the integration of DuckDB with dbt-duckdb and Dagster, as well as managing Polaris catalog configurations.

## Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | Polaris manages Iceberg table metadata |
| [ADR-0034](docs/architecture/adr/0034-dbt-duckdb-iceberg.md) | dbt-duckdb Workaround | Inline credentials for DuckDB ATTACH |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | Polaris coordinates multi-engine access |
| [ADR-0036](docs/architecture/adr/0036-storage-plugin-interface.md) | Storage Plugin Interface | Polaris uses pluggable storage backends |
| [ADR-0031](docs/architecture/adr/0031-infisical-secrets.md) | Infisical Secrets | OAuth2 credentials managed via secrets |

## When to Use This Skill

Invoke this skill when working on:
- Building data lakehouses with DuckDB and Polaris
- Configuring Polaris catalog in `platform.yaml`
- Managing namespaces and credentials (OAuth2, static)
- Integrating DuckDB via dbt-duckdb plugin
- Debugging access control issues and multi-engine coordination

## Core Principles

### 1. Catalog-as-Control-Plane

**NEVER write directly to storage**. All table operations MUST flow through Polaris catalog:

```
Apache Polaris (REST Catalog API)
        ↓
DuckDB (ATTACH) | dbt-duckdb (Plugin) | PyIceberg (Direct)
```

### 2. Two-Tier Configuration Architecture

| File | Audience | Contains |
|------|----------|----------|
| `platform.yaml` | Platform Engineers | Polaris endpoints, credentials, storage |
| `floe.yaml` | Data Engineers | Logical references (`catalog: default`) |

**Data engineers NEVER see credentials.**

## Quick Reference: Common Patterns

### DuckDB Connection Patterns

```python
import duckdb

# Ephemeral in-memory (recommended for pipelines)
conn = duckdb.connect(":memory:")

# File-based (for floe-platform)
conn = duckdb.connect("/tmp/floe.duckdb")

# With configuration
conn = duckdb.connect(config={
    'memory_limit': '8GB',
    'threads': 4,
    'temp_directory': '/tmp/duckdb'
})
```

### Polaris Catalog Configuration

```yaml
# platform/local/platform.yaml
catalogs:
  default:
    type: polaris
    uri: "http://floe-infra-polaris:8181/api/catalog"
    warehouse: demo_catalog
    credentials:
      mode: oauth2
      client_id:
        secret_ref: polaris-client-id    # → POLARIS_CLIENT_ID env var
      client_secret:
        secret_ref: polaris-client-secret # → POLARIS_CLIENT_SECRET env var
      scope: "PRINCIPAL_ROLE:service_admin"
    access_delegation: none
    token_refresh_enabled: true
```

### DuckDB ATTACH with Inline Credentials

```sql
-- Plugin automatically executes on dbt run:
ATTACH 'demo_catalog' AS polaris_catalog (
    TYPE ICEBERG,
    CLIENT_ID 'demo_client',
    CLIENT_SECRET 'demo_secret',
    OAUTH2_SERVER_URI 'http://polaris:8181/api/catalog/v1/oauth/tokens',
    ENDPOINT 'http://polaris:8181/api/catalog'
);
```

## Implementation Workflow

1. ✅ Discover existing patterns in `packages/floe-polaris`
2. ✅ Verify Polaris availability (local or K8s)
3. ✅ Research unfamiliar features (WebSearch)
4. ✅ Use floe-polaris factory functions (`create_catalog`)
5. ✅ Follow two-tier configuration (credentials in `platform.yaml`)
6. ✅ Test DuckDB ATTACH (run `dbt debug`)
7. ✅ Verify table writes via DuckDB native Iceberg
8. ✅ Run integration tests (`pytest packages/floe-polaris/tests/integration`)

## Common Errors and Solutions

**1. Authentication failure (401)**
- Verify `POLARIS_CLIENT_ID` and `POLARIS_CLIENT_SECRET` env vars
- Check `token_refresh_enabled: true`
- Test OAuth2 token manually

**2. DuckDB ATTACH fails**
- Check `catalog_uri` includes `/api/catalog`
- Verify environment variables in dbt profiles.yml

**3. Namespace not found**
- Use `create_parents=True` when creating nested namespaces
- Check hierarchical creation order (parent before child)

## Detailed Documentation

For comprehensive details, see:
- **Integration Patterns**: `.claude/skills/polaris-skill/docs/integration-patterns.md`
- **API Reference**: `.claude/skills/polaris-skill/docs/api-reference.md`
- **Helm Initialization**: `demo/platform-config/charts/floe-infrastructure/templates/polaris-init-job.yaml`
- **floe-polaris Package**: `packages/floe-polaris/README.md`
- **Platform Config Guide**: `docs/platform-config.md`
- **Apache Polaris Docs**: https://polaris.apache.org

## Security Best Practices

- Use `SecretStr` for all credentials
- Never log secrets or credentials
- Use `PRINCIPAL_ROLE:<role_name>` (least-privilege scope)
- NEVER use `PRINCIPAL_ROLE:ALL` in production
- Rotate credentials via K8s secrets
- Enable audit logging in production