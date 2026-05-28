---
name: duckdb-polaris-integration
description: Use this skill when configuring and managing the integration of DuckDB with the Polaris catalog in a data lakehouse architecture, particularly when using dbt and Dagster.
---

# DuckDB and Polaris Catalog Integration

This skill provides guidance on integrating **DuckDB** with the **Polaris catalog** for building modern data lakehouses. It covers configuration, management of namespaces, credential setup, and orchestration patterns using **dbt** and **Dagster**.

## When to Use This Skill

Invoke this skill when working on:
- Configuring the Polaris catalog in `platform.yaml`
- Managing namespaces and credentials (OAuth2, static, IAM roles)
- Integrating DuckDB via the dbt-duckdb plugin
- Performing operations with PyIceberg
- Debugging access control issues
- Creating Dagster assets with DuckDB

## Key Insights

### Two-Tier Configuration Model
- **Platform Engineers** manage `platform.yaml` with infrastructure details (endpoints, credentials).
- **Data Engineers** work with `floe.yaml` containing logical references (`catalog: default`).

### Catalog-as-Control-Plane
All table operations must flow through the Polaris catalog:
```
Apache Polaris (REST Catalog API)
        ↓
DuckDB (ATTACH) | dbt-duckdb (Plugin) | PyIceberg (Direct)
```

## Quick Reference

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

### Pre-Implementation Checklist

#### Step 1: Discover Existing Patterns (ALWAYS DO FIRST)

```bash
# Check floe-polaris client implementation
cat packages/floe-polaris/src/floe_polaris/client.py

# Review platform.yaml examples
cat demo/platform-config/platform/local/platform.yaml | grep -A 20 "catalogs:"
```

### Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | Polaris manages Iceberg table metadata |
| [ADR-0034](docs/architecture/adr/0034-dbt-duckdb-iceberg.md) | dbt-duckdb Workaround | Inline credentials for DuckDB ATTACH |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | Polaris coordinates multi-engine access |
| [ADR-0036](docs/architecture/adr/0036-storage-plugin-interface.md) | Storage Plugin Interface | Polaris uses pluggable storage backends |
| [ADR-0031](docs/architecture/adr/0031-infisical-secrets.md) | Infisical Secrets | OAuth2 credentials managed via secrets |