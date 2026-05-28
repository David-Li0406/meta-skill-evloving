---
name: document-review-expert
description: Expert guidance for creating, implementing, and troubleshooting Document Review Rules in Frappe Tweaks - a flexible document review/approval system. Use when working with Document Review Rules, Document Reviews, implementing review/approval workflows, creating validation scripts, debugging review issues, understanding review evaluation and lifecycle, or integrating reviews with workflows and submissions.
---

# Document Review Expert

Expert guidance for working with the Document Review system in Frappe Tweaks, a flexible document review/approval framework.

## Overview

The Document Review system provides a rule-based approach to document validation and approval workflows:

- **Document Review Rules** define validation checks via Python scripts
- **Document Reviews** track approval state as submittable records
- Rules are evaluated automatically on document changes
- **Automatic banner** displays pending reviews at the top of forms
- Mandatory reviews block document submission (with auto-approval before submit)
- Reviews integrate with workflows and timeline
- **Permission-aware** - users only see reviews for documents they can access

This system enables dynamic approval requirements based on document content, bypassing the need for complex workflow configurations.

## Core Concepts

### Document Review Rule

A rule that defines when a document needs review via a Python script. The script:
- Has access to `doc` variable (the document being checked)
- Returns `None` if no review needed
- Returns a dict with `message` and optional `data` if review is required

**Key properties:**
- `title`: Human-readable rule name
- `reference_doctype`: DocType this rule applies to
- `script`: Python code to evaluate (see [Script Writing Guide](references/script-examples.md))
- `mandatory`: If checked, blocks submission until review is approved
- `disabled`: Temporarily disable the rule
- `users`: Child table listing users to auto-assign to created reviews (each user has an `ignore_permissions` checkbox)

### Document Review

A submittable record representing a required review. Created automatically when a rule returns a result.

**Lifecycle:**
1. **Draft (docstatus=0)**: Pending review, blocks submission if mandatory
2. **Submitted (docstatus=1)**: Approved, allows submission
3. **Cancelled (docstatus=2)**: Rejected

**Key properties:**
- `reference_doctype` + `reference_name`: Link to the document being reviewed
- `review_rule`: Link to the rule that created this review
- `title`: Optional custom title for the review
- `message`: Explanation of why review is needed
- `review_data`: Additional structured data (JSON)
- `mandatory`: Whether this review blocks submission

### Evaluation Lifecycle

Rules are evaluated automatically via hooks:

1. **on_change**: Evaluates all rules for the doctype when document changes
2. **refresh**: Automatic banner displays pending review count with "See Pending Reviews" button
3. **before_submit**: Auto-approves all pending reviews, then blocks if mandatory reviews remain
4. **Timeline integration**: Displays reviews in document timeline with action buttons (permission-aware)
5. **bootinfo**: Tracks doctypes with rules for efficient banner display

## Quick Start

### Creating a Basic Review Rule

1. Navigate to **Document Review Rule** list
2. Create new rule with:
   - **Title**: Descriptive name (e.g., "Check Minimum Price")
   - **Reference DocType**: Target DocType (e.g., "Sales Order")
   - **Script**: Python code that returns `None` or review dict
   - **Mandatory**: Check if submission should be blocked
   - **Assign Users** (optional): List users who should be auto-assigned to reviews
     - Each user row has an **Ignore Permissions** checkbox for per-user control

Example script:
```python
# Check if total is above threshold
if doc.grand_total > 100000:
    result = {
        "title": "High Value Order",
        "message": "Order exceeds approval threshold of $100,000",
        "data": {
            "grand_total": doc.grand_total,
            "threshold": 100000
        }
    }
```

3. Save the rule - it takes effect immediately

### Auto-Assignment of Reviewers

You can configure a Document Review Rule to automatically assign specific users when a review is created:

1. In the **Assign Users** table, add users who should be assigned
2. For each user, set **Ignore Permissions** checkbox:
   - **Unchecked** (default): User will only be assigned if they have:
     - Submit permission on Document Review doctype
     - Read permission on the referenced document
   - **Checked**: User will be assigned regardless of permissions

**Why use this instead of Assignment Rules?**

1. **Permission-aware**: Can filter users based on dual permission checks on a per-user basis (Assignment Rules always ignore permissions)
2. **Multiple assignments**: Can assign to multiple users per document (Assignment Rules assign only one user)
3. **Context-specific**: Assignments are tied to specific review rules and their evaluation context
4. **No notification spam**: Differential assignment logic only notifies new users, never re-notifies existing assignees
5. **Personalized descriptions**: Each assignment uses the review message as the todo description

**How it works:**

- Assignments are created on the **referenced document** (e.g., Sales Order), not the Document Review
- When multiple reviews exist for the same document, the system calculates the **union of users** from all pending reviews
- **Differential logic** compares desired users with current assignments:
  - **New users**: Assigned with personalized description from review message (notification sent)
  - **Existing users**: No action taken (no notification)
  - **Removed users**: Closed for submitter, cancelled for others
- Users see the assignment in their ToDo list with the review message as description (e.g., "Price exceeds approval threshold")
- On review submission, assignments are automatically recalculated based on remaining pending reviews

### Reviewing a Document

When a Document Review is created:

1. **Automatic banner** appears at top of form showing pending review count
2. Click "See Pending Reviews" button to scroll to reviews in timeline
3. Reviews displayed in timeline with "Review" button (if user has submit permission)
4. Click "Review" button to open dialog with approval/rejection options
5. Add optional comments and choose Approve or Reject
6. Review is submitted/cancelled, form reloads to update status

**Note:** If reviews remain pending at submission, they are auto-approved first. Only mandatory reviews that fail to approve will block submission.

## Common Use Cases

### 1. Price Approval

Require manager approval for items below minimum price.

See [references/script-examples.md](references/script-examples.md) for complete example.

### 2. Credit Limit Check

Flag orders that exceed customer credit limit.

### 3. Discount Approval

Require approval for discounts above certain percentage.

### 4. Compliance Checks

Verify required fields, attachments, or certifications.

### 5. Multi-level Approvals

Different rules for different approval thresholds.

## Integration Patterns

### With Workflows

Use reviews as workflow transition conditions. A helper function is available in workflow conditions:

```python
# In Workflow Transition condition (preferred method)
# Returns: "Approved", "Pending Review", "Can Approve", or "Can Submit"
status = document_review.get_document_review_status(doc.doctype, doc.name)
return status == "Approved"
```

**Alternative - Direct query:**
```python
frappe.db.count("Document Review", {
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "docstatus": 0
}) == 0
```

See [references/integration-patterns.md](references/integration-patterns.md) for detailed examples.

### With Form Banners

**Automatic banner** is provided out-of-the-box for all doctypes with Document Review Rules. No custom code needed!

The banner:
- Displays at the top of the form when reviews are pending
- Shows review count with orange styling
- Includes "See Pending Reviews" button to scroll to timeline
- Only appears when document is saved and has active rules

**Custom banner (if needed):**
```javascript
// Only use if you need custom banner behavior
frappe.call({
    method: "frappe.client.get_count",
    args: {
        doctype: "Document Review",
        filters: {
            reference_doctype: frm.doctype,
            reference_name: frm.docname,
            docstatus: 0
        }
    },
    callback: (r) => {
        if (r.message > 0) {
            frm.dashboard.add_indicator(
                __("Pending Reviews: {0}", [r.message]),
                "orange"
            );
        }
    }
});
```

### With Server Scripts

Create or check reviews programmatically. See [references/integration-patterns.md](references/integration-patterns.md).

## Rule Writing Guide

### Script Context

The rule script has access to:
- `doc`: The document instance being evaluated
- Standard Frappe API: `frappe.db.get_value()`, `frappe.get_all()`, etc.
- All standard Python functions

### Return Format

Document Review Rule scripts support two ways to indicate that a review is needed:

**Option 1: Using `result` variable (traditional approach)**
```python
result = {
    "message": "Explanation of why review is needed",
    "data": {
        # Optional structured data for reviewers
        "field1": value1,
        "field2": value2
    }
}
```

**Option 2: Using direct `message` and `data` variables (new approach)**
```python
message = "Explanation of why review is needed"
data = {
    # Optional structured data for reviewers
    "field1": value1,
    "field2": value2
}
```

**No review needed:**
```python
result = None
# or simply don't set message or result
```

**Note:** The `result` variable takes precedence if both approaches are used. If neither `result` nor `message` is set, no review will be created.

### Best Practices

1. **Early exit**: Return `None` as soon as possible when no review needed
2. **Clear messages**: Explain why review is needed and what to check
3. **Include data**: Provide context in `data` field for reviewers
4. **Handle errors**: Use try-except to prevent script failures
5. **Performance**: Minimize database queries, use caching when appropriate

See [references/script-examples.md](references/script-examples.md) for complete examples.

## Reference Files

Detailed guides for specific topics:

- **[references/document-review-system.md](references/document-review-system.md)**: Complete system architecture and lifecycle
- **[references/rule-creation-guide.md](references/rule-creation-guide.md)**: Step-by-step guide to creating rules
- **[references/script-examples.md](references/script-examples.md)**: Working script examples for common scenarios
- **[references/integration-patterns.md](references/integration-patterns.md)**: Workflow, form, and programmatic integration
- **[references/troubleshooting.md](references/troubleshooting.md)**: Common issues and debugging techniques

## Key Features

### Automatic Evaluation

Rules run automatically on document save via `on_change` hook. No manual triggering required.

### Smart Review Management

- Draft reviews auto-created when rule returns result
- Auto-deleted when rule no longer applies (returns `None`)
- Prevents duplicate reviews for same data
- Reuses submitted reviews if data hasn't changed
- **Auto-approval on submit**: Pending reviews are automatically approved during submission

### Automatic Banner System

- **Zero-configuration**: Works automatically for all doctypes with rules
- Displays pending review count at top of form
- "See Pending Reviews" button scrolls to timeline
- Only shown when document has active rules and saved
- Tracked via bootinfo for efficient display

### Timeline Integration

Reviews appear in document timeline with:
- Status indicators (Pending/Approved/Rejected)
- Review messages with formatted data
- **Permission-aware action buttons**: Only shown to users with submit permission
- Review dialog with Approve/Reject options
- Full audit trail with comments

### Permission Control

Reviews respect standard Frappe permissions:
- **Permission query conditions**: Users only see reviews for documents they can access
- Only users with submit permission can approve reviews
- System Managers have full access by default
- Custom roles can be configured

### Workflow Integration

- **Helper function** available in workflow conditions: `document_review.get_document_review_status()`
- Returns status: "Approved", "Pending Review", "Can Approve", or "Can Submit"
- Use in transition conditions, action conditions, or state messages

## Troubleshooting

**Rule not triggering:**
- Check if rule is disabled
- Verify `reference_doctype` matches document type
- Clear cache: `frappe.cache.delete_value(f"document_review_rules:{doctype}")`

**Script errors:**
- Check error log: `bench --site [site] logs`
- Use try-except in script for debugging
- Test script logic in Python console first

**Review not blocking submission:**
- Verify `mandatory` is checked on rule
- Check review `docstatus` (must be 0 to block)
- Ensure `before_submit` hook is configured

See [references/troubleshooting.md](references/troubleshooting.md) for comprehensive debugging guide.

## API Reference

### Functions

**`get_rules_for_doctype(doctype)`**
Get all active rules for a doctype (cached).

**`evaluate_document_reviews(doc, method=None)`**
Evaluate all rules for a document (called by `on_change` hook).

**`check_mandatory_reviews(doc, method=None)`**
Auto-approve all pending reviews, then block submission if mandatory reviews remain (called by `before_submit` hook).

**`submit_document_review(review_name, review=None, action="approve")`**
Whitelist function to submit/cancel a single review.
- `review_name`: Document Review name
- `review`: Optional comments
- `action`: "approve" or "reject"

**`submit_all_document_reviews(doctype, docname, review=None, action="approve")`**
Whitelist function to submit/cancel all pending reviews for a document.
- Returns: Dict with `total`, `successful`, `failed`, and `errors`

**`get_document_review_status(doctype, docname)`**
Whitelist function to get review status for a document.
- Returns: "Approved", "Pending Review", "Can Approve", or "Can Submit"
- Available in workflow conditions via `document_review.get_document_review_status()`

**`add_document_review_bootinfo(bootinfo)`**
Add doctypes with rules to bootinfo (for banner display).

**`get_document_reviews_for_timeline(doctype, docname)`**
Get reviews for timeline display with action buttons.

**`get_document_review_permission_query_conditions(user=None, doctype=None)`**
Permission query conditions - filters reviews to only show those for accessible documents.

### Hooks Configuration

```python
doc_events = {
    "*": {
        "on_change": ["tweaks.utils.document_review.evaluate_document_reviews"],
        "before_submit": ["tweaks.utils.document_review.check_mandatory_reviews"],
    }
}

additional_timeline_content = {
    "*": ["tweaks.utils.document_review.get_document_reviews_for_timeline"]
}

get_additional_bootinfo = [
    "tweaks.utils.document_review.add_document_review_bootinfo"
]

permission_query_conditions = {
    "Document Review": "tweaks.utils.document_review.get_document_review_permission_query_conditions"
}

workflow_safe_eval_globals = [
    "tweaks.utils.safe_exec.workflow_safe_eval_globals"
]

ignore_links_on_delete = ["Document Review"]
```

## Performance Considerations

- Rules cached per doctype (invalidated on rule changes)
- Evaluation runs only on document change
- Timeline queries optimized with proper indexes
- Review data comparison prevents duplicate reviews

## Security Notes

- Scripts run with full permissions in safe_exec context
- Reviews created with `ignore_permissions=True`
- Always validate user input in scripts
- Be cautious with database modifications in scripts
