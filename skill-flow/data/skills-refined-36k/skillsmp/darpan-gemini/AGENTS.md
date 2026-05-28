# Darpan AGENTS.md

## Focus: best practices and coding guidelines
Component-generic guidance lives here; user-specific preferences are in `AGENTS.md` at the repo root.

### Where to implement changes
- Put business logic in `runtime/component/darpan/src/**` and expose it through service definitions in `runtime/component/darpan/service/*.xml`.
- Keep entity changes in `runtime/component/darpan/entity/*.xml` and update docs alongside code when behavior changes.
- Keep changes within `runtime/component/darpan/**`; avoid framework, `runtime/base-component/**`, and `runtime/template/**` unless explicitly requested.

### Documentation updates
- After code changes, update `runtime/component/darpan/docs/**` in the same PR to keep documentation aligned.
- Update the closest feature doc first (e.g., `docs/reconciliation/**`, `docs/reconciliation/json-reconciliation.md`).
- Add/refresh service signatures, input/output parameters, and defaults when service XML changes.
- Include one concrete example (sample inputs, JSONPath, or service call) when behavior changes.
- Note operational impacts: output locations, schema names, or required parameters.
- If a change is user-facing, add a brief “what changed” note in the relevant doc section.

### Moqui service conventions
- Define clear `in-parameters` and `out-parameters` with types, defaults, and descriptions.
- Prefer `component://` and `runtime://` locations in services and scripts; avoid absolute filesystem paths.
- For file uploads, accept `org.apache.commons.fileupload.FileItem` and persist to `runtime://tmp/**` with sanitized filenames.

### XML vs Groovy usage
- Use XML (entities, services, screens) for declarative configuration, routing, validation, and simple orchestration.
- Use Groovy scripts for complex logic, data transforms, Spark jobs, or anything requiring loops, branching, or library calls.
- Keep XML thin: call Groovy for heavy lifting; return structured outputs back to XML services.
- When logic becomes non-trivial, move it into `runtime/component/darpan/src/**` and keep XML as a wrapper.

### Groovy + Spark guidelines
- For reconciliation services, keep Spark sessions alive (no `spark.stop()`); stop in `finally` for one-off scripts/tests.
- Avoid `collect()` on large datasets; use `limit`, `select`, or write outputs to files instead.
- Persist large DataFrames to disk and `unpersist()` after use.
- Keep Spark defaults configurable via `sparkMaster` and `sparkAppName` parameters.
- When reading JDBC, get credentials from `SystemMessageRemote` and mask secrets in logs.

### Reconciliation behavior
- Validate inputs before compare and return validation errors in outputs; keep reconciliation output consistent even on validation failures.
- Emit consistent diff files under `runtime://tmp/reconciliation/**` so screens and jobs can find outputs.
- Preserve IDs and minimal fields in outputs; only include full objects when required by the use case.

### Darpan-specific patterns (from current code)
- Validate inputs early with explicit `IllegalArgumentException` messages; normalize strings with `?.toString()?.trim()` and booleans via `normalizeBool`.
- Keep helper closures near the top of scripts (`resolvePath`, `cleanFileName`, `normalizeBaseName`, `logStatus`) instead of duplicating logic.
- Resolve locations via `ec.resource.getLocationReference(...)`, create dirs/files with `makeDirectory`/`makeFile`, and fall back to runtime paths when needed.
- Name outputs with `ec.l10n.format(ec.user.nowTimestamp, 'yyyyMMdd-HHmmss')`, sanitize with `[^A-Za-z0-9._-]`, and suffix on collision; return both `diffLocation` and `diffFileName`.
- Standardize Spark IDs as `compare_id` (cast to string, filter null/blank) and use anti-joins for diffs.
- Resolve simple JSON keys to JSONPath via `JsonSchemaServices.resolve#JsonPathForKey`; default to `$.id` only with `processingWarnings`.
- Prefer streamed output writes: Spark `coalesce(1)` + temp dir rename for CSV, `toLocalIterator()` + `withWriter("UTF-8")` for JSON.

### UI screens
- Use Moqui’s built-in pagination widgets/styling; avoid custom HTML pagination unless there’s no alternative.
- For multiple paginated lists on one screen, prefer standalone list screens in dynamic containers so each list keeps its own pageIndex.

### JSON schema handling
- Store schemas in `runtime/schemas/json/*.schema.json` and reference by filename.
- Keep JSONPath expressions stable and documented in `runtime/component/darpan/docs/**`.
- Prefer library-backed schema parsing/validation (Jackson + json-schema-validator) over bespoke implementations; only hand-roll inference when no library exists.

### Logging, errors, and safety
- Use structured, readable logs with context (service name, file labels, counts).
- Never log credentials, API tokens, or raw connection strings; mask passwords in URLs.
- Treat config files and `mcp.json` as sensitive; do not commit secrets.

### Java 17 compatibility
- Spark requires `--add-exports=java.base/sun.nio.ch=ALL-UNNAMED`; preserve JDK flags in `runtime/component/darpan/docker/entrypoint.sh` and `runtime/component/darpan/docs/build/java17-compatibility.md`.

### Testing and verification
- Tests are not run by default; run `./gradlew test` or targeted tasks explicitly.
- Use `runtime/component/darpan/data/test/test-json-reconciliation.groovy` and schemas in `runtime/schemas/json/` for quick validation.
- When writing or editing XML (entities, services, screens), run an XML verification step every time (e.g., lint/validate or load in Moqui) and fix any schema or syntax errors immediately.

### System design tips
- Keep responsibilities separated: ingest -> normalize -> reconcile -> report; avoid mixing IO and compare logic.
- Make reconciliation runs idempotent; include run IDs/timestamps and write outputs to deterministic locations.
- Favor file-based inputs/outputs for bulk jobs; persist summaries to entities only when needed for UI/queries.
- Design for scale: avoid full in-memory loads; stream or partition data and use Spark for large datasets.
- Keep schemas and JSONPath expressions versioned; changing them is a breaking contract for feeds and reports.
- Build in observability: log counts, timings, and identifiers (without secrets) to trace runs.
