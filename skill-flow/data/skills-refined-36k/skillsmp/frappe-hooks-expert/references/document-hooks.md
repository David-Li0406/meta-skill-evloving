# Document Hooks (doc_events)

Document hooks allow you to execute custom code at various points in a document's lifecycle.

## Hook Structure

```python
doc_events = {
    "DocType Name": {
        "event_name": "app_name.module.function",
        "another_event": [
            "app_name.module.function1",
            "app_name.module.function2",
        ],
    },
    "*": {  # Wildcard - applies to all doctypes
        "on_update": "app_name.utils.log_all_updates",
    },
}
```

## Available Events

### Insert Events

**before_insert** - Before document is inserted into database
- Use for: Pre-insert validation, setting default values
- Database: Not yet inserted
- Example: Generate custom IDs, validate unique constraints

```python
def before_insert(doc, method=None):
    if not doc.custom_id:
        doc.custom_id = generate_custom_id(doc)
```

**after_insert** - After document is inserted into database
- Use for: Creating related records, sending notifications
- Database: Inserted, has `doc.name`
- Example: Create linked records, log creation

```python
def after_insert(doc, method=None):
    # Create related document
    frappe.get_doc({
        "doctype": "Activity Log",
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "action": "Created"
    }).insert(ignore_permissions=True)
```

### Save Events

**before_save** - Before document is saved (insert or update)
- Use for: Validation that applies to both insert and update
- Database: May or may not exist yet
- Note: Runs for both new and existing docs

```python
def before_save(doc, method=None):
    # Validate business rules
    if doc.start_date > doc.end_date:
        frappe.throw("Start date cannot be after end date")
```

**after_save** - After document is saved
- Use for: Post-save processing for both insert and update
- Database: Saved with latest changes

**validate** (controller method, not hook) - Runs before save/submit
- Use for: Core validation logic
- Location: In DocType controller class, not hooks.py

### Update Events

**on_update** - After document is updated
- Use for: General post-update processing
- Fires after: insert, save, submit, update_after_submit
- Most commonly used document hook

```python
def on_update(doc, method=None):
    # Update related documents
    update_linked_records(doc)
```

**before_update_after_submit** - Before updating a submitted document
- Use for: Validating changes to submitted docs
- Only fires when: docstatus=1 and fields are updated

**after_update_after_submit** - After updating a submitted document
- Use for: Processing changes to submitted docs

### Submit Events

**before_submit** - Before document is submitted
- Use for: Pre-submission validation
- Database: docstatus still 0

```python
def before_submit(doc, method=None):
    if not doc.approver:
        frappe.throw("Approver is required before submission")
```

**after_submit** - After document is submitted
- Use for: Workflow actions, creating accounting entries
- Database: docstatus = 1

```python
def after_submit(doc, method=None):
    # Create accounting entries
    create_journal_entry(doc)
    
    # Send notification
    frappe.sendmail(
        recipients=doc.approver,
        subject=f"{doc.doctype} {doc.name} submitted",
        message=f"Please review {doc.name}"
    )
```

### Cancel Events

**before_cancel** - Before document is cancelled
- Use for: Pre-cancellation validation
- Database: docstatus still 1

```python
def before_cancel(doc, method=None):
    # Check if dependent records exist
    if frappe.db.exists("Dependent DocType", {"reference": doc.name}):
        frappe.throw("Cannot cancel: dependent records exist")
```

**after_cancel** - After document is cancelled
- Use for: Reversing related entries, cleanup
- Database: docstatus = 2

```python
def after_cancel(doc, method=None):
    # Reverse accounting entries
    reverse_journal_entry(doc)
    
    # Cancel related documents
    for child in doc.items:
        cancel_related_doc(child.reference)
```

**on_cancel** - After cancel (similar to after_cancel)
- Use for: General post-cancel processing

### Delete Events

**on_trash** - Before document is deleted
- Use for: Cleanup, deleting related records
- Note: Called before database DELETE
- Can prevent deletion by throwing error

```python
def on_trash(doc, method=None):
    # Delete related records
    frappe.db.delete("Child DocType", {"parent": doc.name})
    
    # Or prevent deletion
    if doc.is_system_record:
        frappe.throw("Cannot delete system records")
```

**before_trash** (controller method, not hook)
- Use for: Controller-level trash logic
- Location: In DocType controller class

**after_delete** - After document is deleted
- Use for: Final cleanup after deletion
- Database: Record no longer exists

### Change Events

**on_change** - When document changes are detected
- Use for: Tracking field changes, triggering on specific changes
- Fires: After save when any field value changes
- Check changes: `doc.has_value_changed("fieldname")`

```python
def on_change(doc, method=None):
    if doc.has_value_changed("status"):
        log_status_change(doc)
    
    if doc.has_value_changed("assigned_to"):
        notify_new_assignee(doc)
```

### Rename Events

**before_rename** - Before document is renamed
- Use for: Validate rename operation
- Can prevent rename by throwing error

```python
def before_rename(doc, method=None, old_name=None, new_name=None, merge=False):
    if not can_rename(doc, new_name):
        frappe.throw(f"Cannot rename to {new_name}")
```

**after_rename** - After document is renamed
- Use for: Update references, log rename

```python
def after_rename(doc, method=None, old_name=None, new_name=None, merge=False):
    # Update custom references
    frappe.db.set_value("Related DocType", 
        {"reference": old_name}, 
        "reference", new_name
    )
```

### Print Events

**before_print** - Before generating print format
- Use for: Modify document before printing
- Note: Changes not saved to database

**after_print** - After print format generated
- Use for: Logging print events

## Examples by Use Case

### 1. Audit Trail

```python
doc_events = {
    "*": {
        "on_update": "app.audit.log_update",
        "on_trash": "app.audit.log_deletion",
    }
}

def log_update(doc, method=None):
    frappe.get_doc({
        "doctype": "Audit Log",
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "action": method,
        "user": frappe.session.user,
    }).insert(ignore_permissions=True)
```

### 2. Workflow Automation

```python
doc_events = {
    "Sales Order": {
        "after_submit": "app.sales.create_delivery_note",
    },
    "Delivery Note": {
        "after_submit": "app.sales.create_sales_invoice",
    }
}

def create_delivery_note(doc, method=None):
    if doc.status == "Approved":
        dn = frappe.get_doc({
            "doctype": "Delivery Note",
            "sales_order": doc.name,
            # Copy items
        })
        dn.insert()
```

### 3. Data Validation

```python
doc_events = {
    "Purchase Order": {
        "before_save": "app.purchase.validate_budget",
        "before_submit": "app.purchase.check_approval",
    }
}

def validate_budget(doc, method=None):
    budget = get_available_budget(doc.cost_center)
    if doc.total_amount > budget:
        frappe.throw(f"Exceeds budget by {doc.total_amount - budget}")
```

### 4. Notification System

```python
doc_events = {
    "Task": {
        "on_update": "app.notifications.task_updated",
    }
}

def task_updated(doc, method=None):
    if doc.has_value_changed("status"):
        notify_assignee(
            doc.assigned_to,
            f"Task {doc.name} status changed to {doc.status}"
        )
```

### 5. Integration with External Systems

```python
doc_events = {
    "Customer": {
        "after_insert": "app.integrations.sync_to_crm",
        "on_update": "app.integrations.sync_to_crm",
    }
}

def sync_to_crm(doc, method=None):
    try:
        crm_api.sync_customer({
            "id": doc.name,
            "name": doc.customer_name,
            "email": doc.email_id,
        })
    except Exception as e:
        frappe.log_error(f"CRM sync failed: {str(e)}")
```

### 6. Cascading Updates

```python
doc_events = {
    "Item": {
        "on_update": "app.inventory.update_item_prices",
    }
}

def update_item_prices(doc, method=None):
    if doc.has_value_changed("standard_rate"):
        # Update all price lists
        frappe.db.sql("""
            UPDATE `tabItem Price`
            SET price_list_rate = %s
            WHERE item_code = %s
        """, (doc.standard_rate, doc.name))
```

### 7. Auto-numbering

```python
doc_events = {
    "Custom DocType": {
        "before_insert": "app.utils.generate_serial",
    }
}

def generate_serial(doc, method=None):
    if not doc.serial_no:
        last_serial = frappe.db.get_value(
            doc.doctype,
            filters={"creation": ["<", doc.creation]},
            fieldname="serial_no",
            order_by="serial_no desc"
        ) or 0
        doc.serial_no = int(last_serial) + 1
```

## Hook Execution Order

When multiple hooks are registered:

1. Hooks execute in the order apps are listed in `apps.txt`
2. Within an app, hooks execute in list order
3. Controller methods run before hooks
4. `on_update` fires after most other events

## Important Notes

- **Avoid Recursion**: Be careful with hooks that save/update documents
- **Performance**: Hooks run synchronously; keep them fast
- **Errors**: Uncaught exceptions in hooks will fail the operation
- **Permissions**: Hooks run with current user permissions unless `ignore_permissions=True`
- **Database State**: Know whether document is already in database
- **method Parameter**: Contains event name (e.g., "on_update")

## Common Patterns

### Check if Field Changed

```python
if doc.has_value_changed("fieldname"):
    # Handle change
```

### Get Old Value

```python
old_value = doc.get_db_value("fieldname")  # Value from database
```

### Conditional Hook Execution

```python
def my_hook(doc, method=None):
    # Only for specific doctype
    if doc.doctype != "Target DocType":
        return
    
    # Only when specific field changes
    if not doc.has_value_changed("status"):
        return
    
    # Your logic here
```

### Error Handling

```python
def my_hook(doc, method=None):
    try:
        # Risky operation
        external_api_call(doc)
    except Exception as e:
        # Log but don't fail
        frappe.log_error(f"Hook failed: {str(e)}")
        # Or re-raise to fail the operation
        # raise
```

## Troubleshooting

**Hook not firing:**
- Check `hooks.py` syntax
- Verify function path is correct
- Restart bench: `bench restart`
- Check for errors in console

**Hook causing errors:**
- Check function signature
- Verify document state (inserted vs not)
- Check permissions
- Add error handling

**Performance issues:**
- Profile hook execution time
- Avoid expensive operations in hooks
- Consider background jobs for slow tasks
- Use bulk operations instead of loops
