# SFTP-Driven Reconciliation Automation

Service: `reconciliation.ReconciliationAutomationServices.poll#SftpAndReconcile`

The automation stages SFTP drops and hands them to the shared router `reconciliation.ReconciliationCoreServices.reconcile#FilesByMapping`, which now funnels everything into the unified comparator `reconciliation.ReconciliationCoreServices.reconcile#UnifiedFiles` so CSV/JSON/Mixed all run through the same code path and output JSON.

This job polls configured SFTP locations, stages the newest matching files locally, and invokes the reconciliation services (CSV/JSON/Mixed) using existing mapping metadata.

## Prerequisites
- Install/configure the `moqui-sftp` component (already added to this repo).
- Create `SystemMessageRemote` records with SFTP credentials:
  - `receiveUrl`/`sendUrl`: host (with optional `:port`); can include a path, but prefer providing the path via `fileXRemotePath`.
  - `username` plus either `password` or `privateKey`/`publicKey`.
- Define `ReconciliationMappingMember` rows for each system with:
  - `systemEnumId` matching the inputs passed to the service.
  - `fileTypeEnumId` (`DftCsv` or `DftJson`).
  - `idFieldExpression` (CSV column or JSONPath/key); JSON runs also require `schemaFileName`.

## Inputs (key parameters)
- `reconciliationMappingId` – required; supplies file type, ID, schema metadata per system.
- `file1SystemEnumId`, `file2SystemEnumId` – required; ties mapping rows to each file.
- `file1SystemMessageRemoteId`, `file2SystemMessageRemoteId` – required; SFTP endpoints to poll.
- `file1FileTypeEnumId`, `file2FileTypeEnumId` – optional override (DftCsv, DftJson) when mapping is missing or you want to force a type.
- `file1SchemaFileName`, `file2SchemaFileName` – optional override for JSON schemas; required for JSON/Mixed runs when the mapping lacks schemas.
- `file1RemotePath`, `file2RemotePath` – optional path override (recommended: point to the directory to scan). If omitted, the path portion of `receiveUrl/sendUrl` is used or `/` if none is provided.
- Files are always selected as the newest file in the directory; no regex is needed. After download, the source file is moved into an `archive` subfolder (configurable via `archiveSubdir`; created if missing).
- Outputs default to a `reconciled` subfolder under the stage directory; override with `outputLocation` if needed.
- `stageLocation` (default `runtime://tmp/reconciliation/automation/input`) – where SFTP files are copied.
- `outputLocation` (default `runtime://tmp/reconciliation/automation/output`) – where diff files are written.
- `sparkMaster`, `sparkAppName` – optional Spark overrides.

## Behavior
- Uses `SftpClient` from `moqui-sftp` to list and download the newest file (filtered by regex when provided). Returns `dataAvailable=false` if either side has no file.
- If the configured host contains a path (e.g., `sftp://host:22/drop/`), that path is used as the default remote path unless you override with `fileXRemotePath`.
- Strips any protocol prefix (e.g., `sftp://`, `ssh://`, `ftp://`) from configured hosts before connecting; prefer storing hosts without a scheme, but prefixed values now work.
- Run log messages are emitted as service messages, so they appear in the Service Job run history (Messages column) for quick troubleshooting.
- Skips the archive subfolder when picking the newest file, and uploads the diff back into the same base path (creating it if missing); root uploads may be rejected by the server.
- Absolute output locations outside runtime are treated as remote upload targets: the diff is written locally under the default `reconciled` folder, then uploaded to that remote path (or the file 1 base path if none is provided).
- Diff filenames now include the mapping name/ID slug when a mapping is provided (e.g., `json-sftpTest-diff-yyyymmdd-hhmmss.json`) so outputs are traceable per reconciliation.
- Stages files locally (filenames sanitized) and delegates to `reconciliation.ReconciliationCoreServices.reconcile#FilesByMapping`, which normalizes inputs and routes to CSV/JSON/Mixed reconciliation without duplicating logic.
- JSON + Mixed still require `schemaFileName` in the mapping for the JSON side; CSV uses `systemFieldName` when present, otherwise `idFieldExpression` is used directly.
- Returns diff file path/name and per-side counts; `processingWarnings` include mapping or detection fallbacks.

## Scheduling Example (service-job)
```xml
<service-job job-name="PollSftpAndReconcileOrders"
    service-name="reconciliation.ReconciliationAutomationServices.poll#SftpAndReconcile"
    description="Check OMS vs Shopify SFTP drops and run reconciliation"
    frequency="600" pause-time="0">
    <parameter name="reconciliationMappingId" value="OrderIdMap"/>
    <parameter name="file1SystemEnumId" value="DarSysOms"/>
    <parameter name="file2SystemEnumId" value="DarSysShopify"/>
    <parameter name="file1SystemMessageRemoteId" value="OMS_SFTP"/>
    <parameter name="file2SystemMessageRemoteId" value="SHOPIFY_SFTP"/>
    <parameter name="stageLocation" value="runtime://tmp/reconciliation/automation/input/orders"/>
    <parameter name="outputLocation" value="runtime://tmp/reconciliation/automation/output/orders"/>
</service-job>
```

The service returns `dataAvailable=false` when no files are found so the job can be scheduled safely at short intervals without raising errors.

## UI: SFTP Automation Screen
- Navigate to **Reconciliation → SFTP Automation** to create/update schedules without editing XML.
- File 1/2 sections: choose systems, SFTP remotes, optional file type (CSV/JSON) and schema overrides, plus remote path/pattern filters.
- Schedule section: pick cadence (minutes/hours/daily) or supply a cron expression, set output location, and pause/resume.
- Advanced toggle: stage location defaults to `runtime://tmp/reconciliation/automation/input`; output defaults to a `reconciled` subfolder under that stage directory; archive folder name defaults to `archive`; Spark overrides are optional.
- Existing jobs for this service are listed with edit/pause/resume actions; editing preloads parameters so you can adjust patterns, paths, or cadence quickly.

## UI: Settings Screen (SFTP credentials)
- Navigate to **Reconciliation → Settings** to add/update `SystemMessageRemote` entries used by the automation screen.
- Store SFTP receive/send URLs, username, and either a password or private key; URLs are masked in the listing to avoid leaking credentials.
