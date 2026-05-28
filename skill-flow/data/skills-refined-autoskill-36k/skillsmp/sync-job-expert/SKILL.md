---
name: sync-job-expert
description: Expert guidance for creating, implementing, and troubleshooting Sync Jobs in the Frappe Tweaks framework. Use when working with Sync Job Types, Sync Job controllers, sync job enqueueing, debugging sync job issues, implementing sync logic, or understanding sync job lifecycle and hooks.
---

# Sync Job Expert

Expert guidance for the Frappe Tweaks Sync Job framework - a queue-based system for data synchronization between DocTypes.

## Core Concepts

**Sync Job Type**: Template defining sync configuration (source/target doctypes, queue, timeout, retry settings)  
**Sync Job**: Individual task instance tracking execution, status, errors, and diffs  
**Controller**: Python module implementing sync logic (Bypass or Standard mode)

## Quick Start

**Creating**: Navigate to **Sync Job Type > New**, set name and doctypes, save to generate controller  
**Enqueueing**: See [references/enqueueing.md](references/enqueueing.md) for `enqueue_sync_job()` parameters and examples  
**Implementing**: See [references/implementation.md](references/implementation.md) for step-by-step controller implementation

## Implementation Modes

Choose one of 3 paths (see [references/implementation.md](references/implementation.md) for details):

1. **Single Target** (Standard): One-to-one sync - implement `get_target_document()` + `update_target_doc()`
2. **Multiple Targets** (Standard): One-to-many sync - implement `get_multiple_target_documents()` + `update_target_doc()`
3. **Bypass**: Full control - implement `execute()`

## Status Flow

1. **Pending** → 2. **Queued** → 3. **Started** → **Finished/Failed/Skipped/Relayed/No Target**
- **Canceled**: Manual cancel (from Pending/Queued/Failed)
- **Failed**: Retries automatically if `retry_count < max_retries`

## Key Methods

**On sync_job:**
- `sync_job.get_context()` - Parse context dict
- `sync_job.get_source_document()` - Load source (even if deleted)
- `sync_job.get_trigger_document()` - Load triggering document
- `sync_job.get_target_document()` - Load target

**Flags (control operations):**
- `sync_job.insert_enabled/update_enabled/delete_enabled`
- `sync_job.update_without_changes_enabled`
- `sync_job.dry_run` - Calculate diff without saving

## Configuration

**Sync Job Type defaults (can override per job):**
- Queue: "default", "short", "long"
- Timeout: seconds
- Retry Delay: minutes between retries
- Max Retries: maximum attempts
- Verbose Logging: preserve data snapshots (disabled by default)

**Context**: Pass custom data to sync logic
**Trigger Tracking**: Track what triggered the job for auditing

## Dry Run Mode

Test sync without changes:

```python
sync_job = enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    dry_run=True  # Populates diff_summary without saving
)
```

## Troubleshooting

**Job stays Queued**: Check RQ workers running (`bench worker`), verify queue name  
**Job fails repeatedly**: Check `error_message`, verify documents exist, validate module path  
**No changes detected**: Set `update_without_changes_enabled=True` or check diff generation  
**Module not found**: Ensure controller exists, check naming (use scrubbed names), run `bench migrate`

## Best Practices

1. Use Standard Mode for simple mappings, Bypass for complex operations
2. Validate source/target before syncing
3. Handle missing targets gracefully (return `target_document_type=None`)
4. Use context for runtime parameters
5. Set appropriate timeouts for operation complexity
6. Use specific queues for heavy operations
7. Log important decisions with `frappe.log_error()`
8. Test retry logic with intentional failures

## Source Code References

- `tweaks/utils/sync_job.py` - Core utilities
- `tweaks/tweaks/doctype/sync_job_type/` - Sync Job Type DocType
- `tweaks/tweaks/doctype/sync_job/` - Sync Job DocType
- `tweaks/tweaks/doctype/sync_job_type/boilerplate/controller._py` - Controller template
