# Enqueueing Sync Jobs

## Function: enqueue_sync_job()

Create and queue a sync job for background execution.

```python
from tweaks.utils.sync_job import enqueue_sync_job

job = enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001"
)
```

## Required Parameters

### sync_job_type
- **Type**: `str`
- **Required**: Yes
- **Description**: Name of the Sync Job Type to execute

## Source Parameters

### source_doc
- **Type**: `Document` object
- **Default**: `None`
- **Description**: Source document object. Automatically extracts `source_document_type` and `source_document_name`

### source_document_type
- **Type**: `str`
- **Default**: From Sync Job Type or extracted from `source_doc`
- **Description**: DocType of the source document

### source_document_name
- **Type**: `str`
- **Default**: `None` (extracted from `source_doc` if provided)
- **Description**: Name of source document. Can be `None` if source was deleted (must provide `context` in this case)

## Target Parameters

### target_doc
- **Type**: `Document` object
- **Default**: `None`
- **Description**: Target document object. Automatically extracts `target_document_type` and `target_document_name`

### target_document_type
- **Type**: `str`
- **Default**: From Sync Job Type or extracted from `target_doc`
- **Description**: DocType of the target document

### target_document_name
- **Type**: `str`
- **Default**: `None`
- **Description**: Pre-specify target document name

## Operation Parameters

### operation
- **Type**: `str`
- **Default**: `None` (determined by controller)
- **Valid values**: `"Insert"`, `"Update"`, `"Delete"`
- **Description**: Pre-specify the sync operation

### context
- **Type**: `dict`
- **Default**: `None`
- **Description**: Custom data passed to controller. Required when `source_document_name` is `None`

## Control Flags

### insert_enabled
- **Type**: `bool`
- **Default**: `True`
- **Description**: Allow insert operations. Job will be skipped if operation is insert and this is `False`

### update_enabled
- **Type**: `bool`
- **Default**: `True`
- **Description**: Allow update operations. Job will be skipped if operation is update and this is `False`

### delete_enabled
- **Type**: `bool`
- **Default**: `True`
- **Description**: Allow delete operations. Job will be skipped if operation is delete and this is `False`

### update_without_changes_enabled
- **Type**: `bool`
- **Default**: `False`
- **Description**: Save target even if no changes detected

### dry_run
- **Type**: `bool`
- **Default**: `False`
- **Description**: Calculate diff without saving changes. Sets status to "Skipped"

## Queue Configuration

### queue
- **Type**: `str`
- **Default**: From Sync Job Type (default: `"default"`)
- **Valid values**: `"default"`, `"short"`, `"long"`, or custom queue name
- **Description**: RQ queue name for job execution

### timeout
- **Type**: `int` (seconds)
- **Default**: From Sync Job Type (default: `300`)
- **Description**: Maximum execution time before job is terminated

### retry_delay
- **Type**: `int` (minutes)
- **Default**: From Sync Job Type (default: `5`)
- **Description**: Base delay in minutes between retry attempts

### max_retries
- **Type**: `int`
- **Default**: From Sync Job Type (default: `3`)
- **Description**: Maximum number of retry attempts for failed jobs

### queue_on_insert
- **Type**: `bool`
- **Default**: `None` (automatically set: `False` in dev mode, `True` in production)
- **Description**: Whether to queue job immediately on insert. When `False`, job stays in "Pending" status

## Trigger Tracking

### trigger_type
- **Type**: `str`
- **Default**: `"Manual"`
- **Valid values**: `"Manual"`, `"Scheduler"`, `"Webhook"`, `"API"`, `"Document Hook"`
- **Description**: How the job was triggered

### triggered_by_doc
- **Type**: `Document` object
- **Default**: `None`
- **Description**: Document that triggered this sync. Automatically extracts type, name, and timestamp

### triggered_by_document_type
- **Type**: `str`
- **Default**: `None` (extracted from `triggered_by_doc`)
- **Description**: DocType that triggered this sync

### triggered_by_document_name
- **Type**: `str`
- **Default**: `None` (extracted from `triggered_by_doc`)
- **Description**: Document name that triggered this sync

### trigger_document_timestamp
- **Type**: `datetime`
- **Default**: `None` (extracted from `triggered_by_doc.modified`)
- **Description**: Timestamp of triggering document

## Hierarchy Parameters

### parent_sync_job
- **Type**: `str`
- **Default**: `None`
- **Description**: Name of parent sync job (for child jobs in batch operations)

## Usage Examples

### Basic Usage

```python
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001"
)
```

### With Document Object

```python
customer = frappe.get_doc("Customer", "CUST-00001")
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_doc=customer
)
```

### With Context

```python
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    context={"force_update": True, "batch_id": "BATCH-001"}
)
```

### Pre-specify Operation and Target

```python
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    operation="Update",
    target_document_name="SAP-CUST-001"
)
```

### With Control Flags

```python
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    insert_enabled=False,  # Disallow insert
    update_enabled=True,   # Allow update
    dry_run=True          # Test without saving
)
```

### Custom Queue and Timeout

```python
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    queue="long",         # Use long queue
    timeout=600,          # 10 minutes
    max_retries=5         # Retry up to 5 times
)
```

### Trigger Tracking

```python
# Using trigger document
sales_order = frappe.get_doc("Sales Order", "SO-00001")
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    trigger_type="Document Hook",
    triggered_by_doc=sales_order
)

# Manual specification
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    trigger_type="API",
    triggered_by_document_type="Sales Order",
    triggered_by_document_name="SO-00001"
)
```

### Deleted Source (Context Required)

```python
# When source is deleted, pass data via context
enqueue_sync_job(
    sync_job_type="Clear Bundle Properties",
    source_document_type="Product Bundle",
    # No source_document_name since deleted
    context={"component_names": ["ITEM-001", "ITEM-002"]}
)
```

### From Document Hooks

```python
# In hooks.py
doc_events = {
    "Customer": {
        "on_update": "myapp.utils.sync_customer"
    }
}

# In myapp/utils.py
def sync_customer(doc, method):
    enqueue_sync_job(
        sync_job_type="SAP Customer Sync",
        source_doc=doc,
        trigger_type="Document Hook"
    )
```

### From JavaScript

```javascript
frappe.call({
    method: 'tweaks.utils.sync_job.enqueue_sync_job',
    args: {
        sync_job_type: 'SAP Customer Sync',
        source_document_name: 'CUST-00001',
        context: {force_update: true}
    },
    callback: function(r) {
        console.log('Sync job queued:', r.message);
    }
});
```

## Dictionary Parameter Format

All parameters can be passed as a single dictionary:

```python
enqueue_sync_job({
    "sync_job_type": "SAP Customer Sync",
    "source_document_name": "CUST-00001",
    "context": {"force_update": True},
    "queue": "long",
    "timeout": 600
})
```
