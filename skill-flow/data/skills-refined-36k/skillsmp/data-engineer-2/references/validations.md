# Data Engineer - Validations

## Non-Idempotent Insert

### **Id**
non-idempotent-insert
### **Severity**
error
### **Type**
regex
### **Pattern**
  - INSERT INTO(?!.*ON CONFLICT|.*UPSERT|.*MERGE)
  - \.insert\((?!.*upsert|.*on_conflict)
### **Message**
Insert without upsert/conflict handling. Re-runs will create duplicates.
### **Fix Action**
Use INSERT ON CONFLICT or MERGE for idempotent inserts
### **Applies To**
  - **/*.py
  - **/*.sql

## Multi-Statement Without Transaction

### **Id**
no-transaction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - execute.*execute(?!.*transaction|.*BEGIN)
  - \.run\(\).*\.run\(\)(?!.*atomic)
### **Message**
Multiple statements without transaction. Partial failure leaves inconsistent state.
### **Fix Action**
Wrap in transaction: async with db.transaction()
### **Applies To**
  - **/*.py

## Silent Exception Swallowing

### **Id**
except-pass
### **Severity**
error
### **Type**
regex
### **Pattern**
  - except.*:\s*pass
  - except.*:\s*continue
  - catch.*\{\s*\}
### **Message**
Exception silently swallowed. Data may be lost without trace.
### **Fix Action**
Log error and send to dead letter queue
### **Applies To**
  - **/*.py
  - **/*.ts

## Timezone-Naive Datetime

### **Id**
naive-datetime
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - datetime\.now\(\)(?!.*tz)
  - datetime\.utcnow\(\)
  - TIMESTAMP(?!.*WITH TIME ZONE)
### **Message**
Timezone-naive datetime can cause aggregation errors.
### **Fix Action**
Use datetime.now(timezone.utc) or TIMESTAMP WITH TIME ZONE
### **Applies To**
  - **/*.py
  - **/*.sql

## Long Pipeline Without Checkpoint

### **Id**
no-checkpoint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*in.*:.*process(?!.*checkpoint|.*commit)
  - while.*:.*batch(?!.*save.*state)
### **Message**
Long-running loop without checkpointing. Failure loses all progress.
### **Fix Action**
Add checkpoint/commit after each batch
### **Applies To**
  - **/*.py

## Hardcoded Batch Size

### **Id**
hardcoded-batch-size
### **Severity**
info
### **Type**
regex
### **Pattern**
  - batch_size\s*=\s*\d{4,}
  - LIMIT\s+\d{4,}
  - chunk.*size.*=.*\d{4,}
### **Message**
Large hardcoded batch size may cause memory issues.
### **Fix Action**
Make batch size configurable and test with production data volumes
### **Applies To**
  - **/*.py

## Loading Without Validation

### **Id**
no-data-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - insert.*\(data\)(?!.*validate|.*schema)
  - load.*(?!.*check|.*valid)
### **Message**
Loading data without validation. Bad data propagates.
### **Fix Action**
Validate schema and business rules before loading
### **Applies To**
  - **/*.py

## Using Processing Time for Windowing

### **Id**
processing-time-window
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - now\(\).*GROUP BY
  - processing_time.*window
  - arrival_time.*aggregate
### **Message**
Using processing time for windows. Late data will be in wrong window.
### **Fix Action**
Use event_time with watermarks for accurate windowing
### **Applies To**
  - **/*.py
  - **/*.sql

## Query Without Bounds

### **Id**
unbounded-query
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SELECT.*FROM(?!.*WHERE|.*LIMIT)
  - \.find\(\{\}\)(?!.*limit)
### **Message**
Query without bounds may return unbounded data.
### **Fix Action**
Add WHERE clause with date range or LIMIT
### **Applies To**
  - **/*.py
  - **/*.sql

## No Record Count Reconciliation

### **Id**
no-reconciliation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - load.*complete(?!.*count|.*verify)
  - pipeline.*done(?!.*reconcil)
### **Message**
Pipeline completes without record count verification.
### **Fix Action**
Compare source and sink counts after pipeline run
### **Applies To**
  - **/*.py

## Polling for Changes

### **Id**
polling-instead-cdc
### **Severity**
info
### **Type**
regex
### **Pattern**
  - while.*sleep.*SELECT.*WHERE.*updated
  - poll.*interval.*query
  - WHERE updated_at > last_sync
### **Message**
Polling for changes is inefficient. Consider CDC.
### **Fix Action**
Use Change Data Capture (Debezium, pg_notify) instead
### **Applies To**
  - **/*.py

## No Dead Letter Queue

### **Id**
no-dead-letter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - except.*log.*error(?!.*dead.*letter|.*dlq)
  - catch.*console\.error(?!.*retry|.*queue)
### **Message**
Errors logged but not sent to dead letter queue for retry.
### **Fix Action**
Send failed records to DLQ for investigation and reprocessing
### **Applies To**
  - **/*.py
  - **/*.ts