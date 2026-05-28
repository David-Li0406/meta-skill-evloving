# Document Review System Overview

Complete architecture, lifecycle, and technical details of the Document Review system in Frappe Tweaks.

## Architecture

### Components

**1. Document Review Rule (DocType)**
- Defines validation logic via Python scripts
- Applies to specific DocTypes
- Can be mandatory or optional
- Cacheable for performance

**2. Document Review (DocType)**
- Submittable record tracking approval state
- Links to source document and rule
- Contains review message and data
- Follows standard Frappe submission workflow

**3. Evaluation Engine (Python Module)**
- `tweaks/utils/document_review.py`
- Automatic rule evaluation on document changes
- Review record management (create/update/delete)
- Submission blocking for mandatory reviews

**4. Hooks Integration**
- `on_change`: Triggers rule evaluation
- `before_submit`: Validates mandatory reviews
- `additional_timeline_content`: Timeline display
- `get_additional_bootinfo`: Client-side data

### Database Schema

**Document Review Rule**
```
name (hash) PK
title (Data)
reference_doctype (Link to DocType) - indexed
script (Code)
mandatory (Check)
disabled (Check)
```

**Document Review**
```
name (naming_series: DR-.YYYY.-) PK
reference_doctype (Link to DocType) - indexed
reference_name (Dynamic Link) - indexed
review_rule (Link to Document Review Rule) - indexed
message (Text Editor)
review_data (JSON)
review (Text Editor)
mandatory (Check)
docstatus (0=Draft, 1=Submitted, 2=Cancelled)
```

### Caching Strategy

Rules are cached per DocType:
- Cache key: `document_review_rules:{doctype}`
- Cached data: List of rule dicts with name, title, script, mandatory
- Invalidation: On rule save/delete via `clear_cache()` method
- Benefits: Reduces DB queries on every document save

## Evaluation Lifecycle

### 1. Document Change Event

When any document is saved:

```python
# Hook: doc_events["*"]["on_change"]
evaluate_document_reviews(doc, method=None)
```

**Process:**
1. Check if rules exist for doctype (from cache)
2. If no rules, exit early
3. For each rule:
   - Execute script with `safe_exec()`
   - Pass `doc` variable to script context
   - Get `result` from execution context
   - If result is `None`: Delete any draft reviews for this rule
   - If result is dict: Create or update draft review

### 2. Rule Script Execution

```python
exec_context = {"doc": doc, "result": None}
safe_exec(rule["script"], None, exec_context)
result = exec_context.get("result")
```

**Script expectations:**
- Access document via `doc` variable
- Set `result` variable to `None` or dict
- Return format: `{"message": str, "data": dict}`

**Error handling:**
- Script errors throw validation error with rule title
- User sees clear error message
- Document save is blocked on script error

### 3. Review Record Management

**When result is None (no review needed):**
```python
_delete_draft_reviews(doc.doctype, doc.name, rule["name"])
```
- Finds all draft reviews for this document + rule
- Deletes them with `ignore_permissions=True`
- Cleans up reviews that are no longer applicable

**When result is dict (review needed):**
```python
_create_or_update_review(doc, rule, result)
```

**Smart deduplication logic:**
1. Serialize result data to JSON (for comparison)
2. Check if submitted review exists with identical data
3. If identical submitted review exists:
   - Delete any draft reviews (already approved)
   - Exit early (no new review needed)
4. Check if draft review exists
5. If draft exists: Update message, data, mandatory flag
6. If no draft: Create new review record

**Why this matters:**
- Prevents duplicate approvals for same issue
- Allows reuse of prior approvals when data unchanged
- Auto-updates pending reviews when issue details change

### 4. Submission Validation

When document is submitted:

```python
# Hook: doc_events["*"]["before_submit"]
check_mandatory_reviews(doc, method=None)
```

**Process:**
1. Check if rules exist for doctype (from cache)
2. If no rules, exit early
3. Query pending mandatory reviews:
   - `reference_doctype` = doc.doctype
   - `reference_name` = doc.name
   - `docstatus` = 0
   - `mandatory` = 1
4. If any found:
   - Get rule titles for error message
   - Throw ValidationError with rule list
   - Block submission

### 5. Timeline Display

When document form loads:

```python
# Hook: additional_timeline_content["*"]
get_document_reviews_for_timeline(doctype, docname)
```

**Process:**
1. Verify user has read permission
2. Query all reviews for document (all statuses)
3. For each review:
   - Build status indicator (orange/green/grey)
   - Format message as markdown
   - Add "Review" button for draft reviews
   - Return timeline template data
4. Reviews appear chronologically in timeline

**Timeline features:**
- Status pills (Pending/Approved/Rejected)
- Formatted review messages
- Clickable links to review records
- Action buttons for pending reviews

## Review Approval Process

### Client-Side Flow

User clicks "Review" button in timeline:

```javascript
// Button calls form trigger
cur_frm.trigger('document_review_approve', review_name)
```

Form script should implement:
```javascript
frappe.ui.form.on(doctype, {
    document_review_approve: function(frm, review_name) {
        // Show dialog with approve/reject options
        // Call submit_document_review API
    }
});
```

### Server-Side API

```python
@frappe.whitelist()
def submit_document_review(review_name, review=None, action="approve"):
    doc = frappe.get_doc("Document Review", review_name)
    doc.review = review
    doc.submit()
    if action == "reject":
        doc.cancel()
    return doc
```

**Actions:**
- `action="approve"`: Submit review (docstatus=1)
- `action="reject"`: Submit then cancel review (docstatus=2)

**Permissions:**
- User must have submit permission on Document Review
- Standard Frappe permission rules apply

### Post-Approval

After review is submitted/cancelled:

```python
# Document Review on_change method
def on_change(self):
    reference_doc = frappe.get_doc(self.reference_doctype, self.reference_name)
    reference_doc.notify_update()
```

**Effects:**
- Source document receives update notification
- Timeline refreshes to show new status
- Submission becomes allowed if all mandatory reviews cleared

## Bootinfo Integration

On user login:

```python
# Hook: get_additional_bootinfo
def add_document_review_bootinfo(bootinfo):
    bootinfo["doctypes_with_document_review_rules"] = frappe.get_all(
        "Document Review Rule",
        filters={"disabled": 0},
        pluck="reference_doctype",
        distinct=True,
    )
```

**Purpose:**
- Client-side code knows which doctypes have review rules
- Enables conditional UI elements
- Avoids unnecessary server calls

## Performance Considerations

### Optimization Strategies

**1. Rule Caching**
- Rules loaded once per doctype
- Cache shared across requests
- Invalidated only on rule changes

**2. Early Exits**
- Check for rules before any processing
- Skip evaluation during migration/install
- Return early from scripts when possible

**3. Efficient Queries**
- Proper indexes on reference fields
- Pluck for single-column results
- Limit results when appropriate

**4. Smart Deduplication**
- JSON comparison to detect identical data
- Reuse submitted reviews when possible
- Avoid creating unnecessary review records

### Performance Characteristics

**Rule evaluation overhead:**
- Negligible when no rules exist (single cache check)
- O(n) where n = number of rules for doctype
- Script execution time varies by complexity

**Database impact:**
- Review queries use indexed fields
- Timeline queries optimized with proper ordering
- Cache reduces rule loading to near-zero

## Security Model

### Script Execution

**safe_exec() context:**
- Restricted Python environment
- No access to dangerous modules (os, sys, etc.)
- Full access to Frappe API
- Can read/query any data
- Cannot write/modify other documents

**Best practices:**
- Validate user input in scripts
- Use parameterized queries
- Avoid exposing sensitive data in messages
- Don't rely on client-side validation

### Permission Model

**Review creation:**
- Always uses `ignore_permissions=True`
- System creates reviews automatically
- Users don't need create permission

**Review approval:**
- Requires submit permission on Document Review
- Standard Frappe permissions apply
- Can be customized via role permissions

**Timeline visibility:**
- Respects read permission on source document
- Users must have read access to see reviews
- Review details visible if document is accessible

## Error Handling

### Script Errors

```python
try:
    # Execute rule script
    exec_context = {"doc": doc, "result": None}
    safe_exec(rule["script"], None, exec_context)
    result = exec_context.get("result")
    # ... process result
except Exception as e:
    frappe.throw(
        _("Error evaluating Document Review Rule '{0}': {1}").format(
            rule["title"], str(e)
        )
    )
```

**Behavior:**
- Script errors block document save
- Error message includes rule title and exception
- User sees clear feedback

### Missing Data Handling

**Reference title population:**
```python
def before_save(self):
    if self.reference_doctype and self.reference_name:
        try:
            meta = frappe.get_meta(self.reference_doctype)
            title_field = meta.get_title_field()
            if title_field:
                self.reference_title = frappe.get_value(...)
            else:
                self.reference_title = self.reference_name
        except Exception:
            self.reference_title = self.reference_name
```

**Fallback strategy:**
- Try to get proper title field
- Fall back to document name
- Gracefully handle errors

## Extension Points

### Custom Timeline Actions

Implement custom buttons in Document Review client script:

```javascript
frappe.ui.form.on("Your DocType", {
    document_review_approve: function(frm, review_name) {
        // Custom approval dialog
        // Custom validation
        // Custom post-approval actions
    }
});
```

### Custom Notification

Add email/notification on review creation:

```python
# In Document Review controller
def after_insert(self):
    # Send notification to approver
    frappe.sendmail(...)
```

### Workflow Integration

Use reviews in workflow conditions:

```python
def workflow_condition(doc):
    return frappe.db.count("Document Review", {
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "docstatus": 0
    }) == 0
```

### Custom Review Actions

Extend submit_document_review for custom actions:

```python
@frappe.whitelist()
def custom_review_action(review_name, action_type):
    review = frappe.get_doc("Document Review", review_name)
    # Custom logic based on action_type
    # Update additional records
    # Send notifications
    review.submit()
    return review
```
