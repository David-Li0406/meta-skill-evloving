# Spark for Reconciliation at Scale

## Why Spark (Benefits)

- SQL over files: full outer joins and aggregations directly on ingested CSV/JSON/Parquet, no rigid schemas required.
- Scale and performance: built for large batches; partitioning and predicate pushdown keep runs fast as data grows.
- Flexibility: schema evolution and variable columns per client are handled naturally; no need to remodel entities per feed.
- Reuse of logic: same code path for small POC runs and larger production batches; deploy once, scale out.
- Ecosystem: built-in support for S3/HDFS/local files, Parquet/CSV, and UDFs for normalization and matching.

## Journey

We started with NoSQL/Elasticsearch for easy ingest of messy CSVs. That worked for landing data but fell short for comparisons that behave like full outer joins (what's missing, what changed). SQL engines (Postgres/EAV) expressed the joins well, but we needed file-first, scalable execution. Spark gives us SQL semantics over files with scale and without rigid schemas, making it the best fit.

## How to Use Spark Here

- Inputs: normalized files (CSV/JSON/Parquet) with `reconBatchId`, `reconRunId`, `sourceSystemId`, `matchKey`, `eventDate`, `payload`.
- Core logic: full outer join on `matchKey` across sources; rule-based checks on selected fields; classify match/mismatch/missing.
- Outputs: result DataFrame with match status and deltas; write to Parquet/CSV for downstream use; optionally persist summaries to a relational store.
- Operational: partition by run/date; handle schema drift with permissive reads; run on a cluster or local for POC; keep file paths/systemMessageId for audit.

## In-Repo Example

- Spark-based comparison: `runtime/component/darpan/src/reconciliation/sample/compareSampleOrderIds.groovy`
- Service entry point: `runtime/component/darpan/service/ReconciliationSampleServices.xml` (`compare#SampleOrderIds`)
- Sample JSON inputs: `runtime/component/darpan/data/sample/omsBulkData.json`, `runtime/component/darpan/data/sample/shopifyBulkData.json`

## When to Add Elasticsearch

- As a landing/search layer for quick ingest and ad-hoc lookups; not the primary comparison engine.
- Keep time-based indices and audit fields if used; run comparisons in Spark.
