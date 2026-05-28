# Implementation Guide

Step-by-step guide for implementing sync job controllers.

## Implementation Paths

There are **3 distinct implementation paths**, each with different required functions:

### Path 1: Single Target (Standard Mode)
**Use when**: One source document syncs to one target document

**Required functions:**
- `get_target_document(sync_job, source_doc)` - Return single target metadata
- `update_target_doc(sync_job, source_doc, target_doc)` - Update target fields

### Path 2: Multiple Targets (Standard Mode)
**Use when**: One source document syncs to multiple target documents (creates child jobs)

**Required functions:**
- `get_multiple_target_documents(sync_job, source_doc)` - Return list of targets
- `update_target_doc(sync_job, source_doc, target_doc)` - Update target fields

**Note:** Do NOT implement both `get_target_document()` and `get_multiple_target_documents()`. Framework checks for `get_multiple_target_documents()` first.

### Path 3: Bypass Mode
**Use when**: You need full control over the sync process (custom transactions, external APIs, complex logic)

**Required function:**
- `execute(sync_job, source_doc)` - Complete sync logic, returns dict with target_doc, operation, diff

**Note:** In Bypass mode, you handle everything including dry run mode. Check `sync_job.get("dry_run")`.

## Creating a Sync Job Type

### Step 1: Create via UI

1. Navigate to **Sync Job Type > New**
2. Fill in required fields:
   - **Sync Job Type Name**: Descriptive name (e.g., "SAP Customer Sync")
   - **Source Document Type**: DocType to sync from
   - **Target Document Type**: DocType to sync to
   - **Module**: Module for organization (auto-set from source doctype)

### Step 2: Configure Options

Optional configuration:
- **Queue**: RQ queue name (default: "default")
  - Options: "default", "short", "long"
  - Use "long" for heavy operations
- **Timeout**: Job timeout in seconds (default: 300)
- **Retry Delay**: Minutes between retries (default: 5)
- **Max Retries**: Maximum retry attempts (default: 3)
- **Verbose Logging**: Preserve data snapshots after completion (default: unchecked)
  - When disabled: Clears `current_data` and `updated_data` fields when job finishes
  - When enabled: Keeps snapshots for debugging

### Step 3: Save and Generate Controller

When saved in developer mode (`is_standard = "Yes"`), a boilerplate controller is created at:

```
{app}/{module}/sync_job_type/{scrubbed_name}/{scrubbed_name}.py
```

Example for "SAP Customer Sync" in Tweaks module:
```
tweaks/tweaks/sync_job_type/sap_customer_sync/sap_customer_sync.py
```

The controller template includes:
- Commented examples of both modes
- All optional hook functions
- Usage notes for each function

## Standard Mode Implementation

### Required Functions

#### get_target_document(sync_job, source_doc)

Returns metadata about the target document.

**Parameters:**
- `sync_job`: Sync Job document (contains operation, context, flags)
- `source_doc`: Source document (may be `None` if source was deleted)

**Returns:**
Dictionary with keys:
- `operation`: `"insert"`, `"update"`, or `"delete"` (required)
- `target_document_type`: Target DocType (optional - uses Sync Job Type default if not provided)
- `target_document_name`: Target document name (required for update/delete, optional for insert)
- `context`: Context dict for this target (optional - overrides existing context)

Or return `None` or dict with `target_document_type=None` to skip sync (job finishes with status "No Target").

**Example:**
```python
def get_target_document(sync_job, source_doc):
    # Try to find existing target
    target_name = frappe.db.get_value(
        "SAP Customer",
        {"erp_customer": source_doc.name}
    )
    
    if target_name:
        return {
            "operation": "update",
            "target_document_name": target_name
        }
    else:
        return {
            "operation": "insert"
        }
```

#### update_target_doc(sync_job, source_doc, target_doc)

Updates target document fields with data from source.

**Parameters:**
- `sync_job`: Sync Job document (contains operation, context)
- `source_doc`: Source document (may be `None` if source was deleted)
- `target_doc`: Target document to update (not yet saved)

**Returns:**
None (framework saves automatically)

**Example:**
```python
def update_target_doc(sync_job, source_doc, target_doc):
    # Set reference on insert
    if not target_doc.erp_customer:
        target_doc.erp_customer = source_doc.name
    
    # Map fields
    target_doc.customer_name = source_doc.customer_name
    target_doc.customer_type = source_doc.customer_type
    target_doc.territory = source_doc.territory
```

### Optional Functions

#### get_multiple_target_documents(sync_job, source_doc)

Returns multiple targets. Framework creates child jobs if > 1 target.

**Parameters:**
- `sync_job`: Sync Job document
- `source_doc`: Source document (may be `None` if source was deleted)

**Returns:**
List of dicts with keys:
- `target_document_type`: Target DocType
- `target_document_name`: Target name (None for insert)
- `operation`: `"insert"`, `"update"`, or `"delete"`
- `context`: Context dict for this target (optional)

Or empty list to finish with status "No Target".

**Note:** Do not return document objects - only metadata. Objects will be serialized to child jobs.

**Example:**
```python
def get_multiple_target_documents(sync_job, source_doc):
    targets = []
    for item in source_doc.get("items"):
        target_name = frappe.db.get_value(
            "Target Item",
            {"source_id": item.name}
        )
        targets.append({
            "target_document_type": "Target Item",
            "target_document_name": target_name,
            "operation": "update" if target_name else "insert",
            "context": {"line_number": item.idx}
        })
    return targets
```

#### after_start(sync_job, source_doc)

Called after job starts (after status changes to "Started").

**When to use:**
- Initialize before sync begins
- Log job execution start
- Validate preconditions

**Note:** Runs even in dry run mode.

**Example:**
```python
def after_start(sync_job, source_doc):
    context = sync_job.get_context()
    frappe.log_error(
        f"Starting sync for {source_doc.name if source_doc else 'deleted source'}",
        "Sync Start"
    )
```

#### before_relay(sync_job, source_doc, targets)

Called before child jobs are queued (when `get_multiple_target_documents` returns > 1).

**Parameters:**
- `sync_job`: Sync Job document (parent job)
- `source_doc`: Source document (may be `None`)
- `targets`: List of target dicts that will create child jobs

**When to use:**
- Validate targets before creating child jobs
- Modify or filter the targets list
- Perform setup before batch processing

**Note:** Runs even in dry run mode.

**Example:**
```python
def before_relay(sync_job, source_doc, targets):
    if len(targets) > 100:
        frappe.throw("Too many targets - limit is 100")
```

#### after_relay(sync_job, source_doc, child_jobs)

Called after child jobs are queued.

**Parameters:**
- `sync_job`: Sync Job document (parent, status = "Relayed")
- `source_doc`: Source document (may be `None`)
- `child_jobs`: List of dicts with child job info
  - Each dict has: `target_document_type`, `target_document_name`, `operation`, `context`, `sync_job`

**When to use:**
- Track or log child job creation
- Perform cleanup after batch setup
- Update parent records with child references

**Note:** Runs even in dry run mode.

**Example:**
```python
def after_relay(sync_job, source_doc, child_jobs):
    source_name = source_doc.name if source_doc else "deleted source"
    frappe.log_error(
        f"Created {len(child_jobs)} child jobs for {source_name}",
        "Batch Sync"
    )
```

#### before_sync(sync_job, source_doc, target_doc)

Called before sync (before save).

**Parameters:**
- `sync_job`: Sync Job document
- `source_doc`: Source document (may be `None`)
- `target_doc`: Target document (not yet saved)

**When to use:**
- Perform validation before save
- Modify target before persistence
- Set additional fields based on runtime conditions

**Note:** Does NOT run in dry run mode.

**Example:**
```python
def before_sync(sync_job, source_doc, target_doc):
    # Set sync timestamp
    target_doc.last_synced = frappe.utils.now()
```

#### after_sync(sync_job, source_doc, target_doc)

Called after sync (after save).

**Parameters:**
- `sync_job`: Sync Job document
- `source_doc`: Source document (may be `None`)
- `target_doc`: Target document (saved)

**When to use:**
- Trigger related processes
- Update related documents
- Send notifications

**Note:** Does NOT run in dry run mode.

**Example:**
```python
def after_sync(sync_job, source_doc, target_doc):
    # Update linked records
    frappe.db.set_value(
        "Customer",
        source_doc.name,
        "sap_id",
        target_doc.name
    )
```

#### finished(sync_job, source_doc, target_doc)

Called when sync finishes successfully (status = "Finished", "Skipped", or "Relayed").

**Parameters:**
- `sync_job`: Sync Job document
- `source_doc`: Source document (may be `None`)
- `target_doc`: Target document (saved) or `None` for relayed jobs

**When to use:**
- Send completion notifications
- Trigger additional processes
- Update audit records

**Note:** Runs even in dry run mode (status "Skipped") and for relayed jobs (target_doc is `None`).

**Example:**
```python
def finished(sync_job, source_doc, target_doc):
    if target_doc:
        source_name = source_doc.name if source_doc else "deleted source"
        frappe.sendmail(
            recipients=["admin@example.com"],
            subject=f"Sync completed: {target_doc.name}",
            message=f"Successfully synced {source_name} to {target_doc.name}"
        )
    else:
        # Relayed job
        frappe.sendmail(
            recipients=["admin@example.com"],
            subject=f"Batch sync started: {sync_job.name}",
            message=f"Created child jobs for batch processing"
        )
```

### Hook Execution Order

**Single Target:**
1. `after_start` - Job starts
2. `get_target_document` - Discover target
3. `update_target_doc` - Update fields
4. `before_sync` - Pre-save (not in dry run)
5. Target saved (not in dry run)
6. `after_sync` - Post-save (not in dry run)
7. `finished` - Completion (runs even in dry run)

**Multiple Targets (Relayed):**
1. `after_start` - Job starts
2. `get_multiple_target_documents` - Discover targets (> 1)
3. `before_relay` - Before child creation
4. Child jobs created and queued
5. `after_relay` - After child creation
6. Parent status set to "Relayed"
7. `finished` - Completion (target_doc is None)

## Bypass Mode Implementation

### execute(sync_job, source_doc)

Full control over sync process.

**Parameters:**
- `sync_job`: Sync Job document
- `source_doc`: Source document (may be `None`)

**Returns:**
Dictionary with keys:
- `target_doc`: Target document (saved or unsaved)
- `operation`: `"insert"`, `"update"`, or `"delete"`
- `diff`: Dict of changes (optional)

**When to use:**
- Custom transaction handling
- Complex multi-document operations
- External API integration
- Standard workflow doesn't fit

**Note:** Responsible for handling dry run mode yourself. Check `sync_job.get("dry_run")`.

**Example:**
```python
def execute(sync_job, source_doc):
    import requests
    
    context = sync_job.get_context()
    
    # Check dry run
    if sync_job.get("dry_run"):
        # Return without making changes
        return {
            "target_doc": None,
            "operation": "update",
            "diff": {"would_sync": True}
        }
    
    # Call external API
    response = requests.post(
        "https://api.example.com/customers",
        json={
            "name": source_doc.customer_name,
            "email": source_doc.email_id
        }
    )
    
    if response.ok:
        external_id = response.json()["id"]
        
        # Update tracking record
        target_doc = frappe.get_doc("External Customer", source_doc.name)
        target_doc.external_id = external_id
        target_doc.last_synced = frappe.utils.now()
        target_doc.save()
        
        return {
            "target_doc": target_doc,
            "operation": "update",
            "diff": {"external_id": {"old": None, "new": external_id}}
        }
    else:
        frappe.throw(f"API Error: {response.text}")
```

## Handling Deleted Sources

When source document is deleted, `source_doc` parameter is `None`. Use context to pass necessary data.

**Example:**

```python
# Enqueueing when deleting
def on_trash_product_bundle(doc, method):
    component_names = [item.item_code for item in doc.get("items", [])]
    
    enqueue_sync_job(
        sync_job_type="Clear Bundle Properties",
        source_document_type="Product Bundle",
        # No source_document_name since deleting
        context={"component_names": component_names},
        trigger_type="Document Hook"
    )

# Controller handling None source
def get_multiple_target_documents(sync_job, source_doc):
    context = sync_job.get_context()
    component_names = context.get("component_names", [])
    
    targets = []
    for name in component_names:
        targets.append({
            "target_document_type": "Item",
            "target_document_name": name,
            "operation": "update",
            "context": {"clear_properties": True}
        })
    return targets

def update_target_doc(sync_job, source_doc, target_doc):
    # source_doc is None
    context = sync_job.get_context()
    if context.get("clear_properties"):
        target_doc.is_bundle_component = 0
        target_doc.parent_bundle = None
```

## Using Context

Context passes custom data to controller functions.

**Example:**

```python
# Enqueue with context
enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    context={
        "force_update": True,
        "sync_addresses": True,
        "batch_id": "BATCH-001"
    }
)

# Access in controller
def get_target_document(sync_job, source_doc):
    context = sync_job.get_context()
    
    # Conditional logic
    if not source_doc.disabled or context.get("force_update"):
        target_name = frappe.db.get_value(
            "SAP Customer",
            {"erp_customer": source_doc.name}
        )
        return {
            "operation": "update" if target_name else "insert",
            "target_document_name": target_name
        }
    
    # Skip sync
    return {"operation": "insert", "target_document_type": None}

def update_target_doc(sync_job, source_doc, target_doc):
    context = sync_job.get_context()
    
    target_doc.customer_name = source_doc.customer_name
    
    # Conditional field mapping
    if context.get("sync_addresses"):
        sync_addresses(source_doc, target_doc)
```

## Testing

### Manual Testing

```python
# Create sync job without queuing
from tweaks.utils.sync_job import create_sync_job

sync_job = create_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    queue_on_insert=False  # Keep in Pending status
)

# Execute manually
sync_job.execute_sync()
```

### Dry Run Testing

```python
sync_job = enqueue_sync_job(
    sync_job_type="SAP Customer Sync",
    source_document_name="CUST-00001",
    dry_run=True  # Calculate diff without saving
)

# Check diff_summary after execution
print(sync_job.diff_summary)
```

### Unit Testing

```python
def test_sync_job_type():
    # Create test source
    source = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": "Test Customer"
    }).insert()
    
    # Create sync job
    sync_job = create_sync_job(
        sync_job_type="SAP Customer Sync",
        source_document_name=source.name,
        queue_on_insert=False
    )
    
    # Execute
    sync_job.execute_sync()
    
    # Verify
    assert sync_job.status == "Finished"
    target = frappe.get_doc("SAP Customer", {"erp_customer": source.name})
    assert target.customer_name == source.customer_name
```
