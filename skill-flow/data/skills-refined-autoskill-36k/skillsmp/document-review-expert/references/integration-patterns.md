# Integration Patterns

How to integrate Document Reviews with workflows, forms, and custom code.

## Workflow Integration

### Transition Condition

Block workflow transitions until reviews are cleared.

**Use Case:** Only allow "Submit for Approval" → "Approved" transition when all reviews are cleared.

**Implementation:**

1. Create Document Review Rules for your DocType
2. Add workflow transition condition:

**Recommended approach (uses helper function):**
```python
# Workflow Transition Condition Script
# Returns True to allow transition, False to block

# get_document_review_status is available via workflow_safe_eval_globals hook
status = document_review.get_document_review_status(doc.doctype, doc.name)

# Returns one of: "Approved", "Pending Review", "Can Approve", "Can Submit"
return status == "Approved"
```

**Alternative approach (direct query):**
```python
# Direct database query
pending_reviews = frappe.db.count("Document Review", {
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "docstatus": 0  # Draft = pending
})

# Allow transition only if no pending reviews
return pending_reviews == 0
```

**Alternative - Check Mandatory Only:**

```python
# Only block on mandatory pending reviews
pending_mandatory = frappe.db.count("Document Review", {
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "docstatus": 0,
    "mandatory": 1
})

return pending_mandatory == 0
```

### Action Condition

Show workflow action only when conditions are met.

```python
# Workflow Action Condition
# Show "Clear for Approval" action only when all reviews are cleared

pending_reviews = frappe.db.count("Document Review", {
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "docstatus": 0
})

return pending_reviews == 0
```

### State Message

Display review status in workflow state banner.

```python
# Get pending review count for display
pending_count = frappe.db.count("Document Review", {
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "docstatus": 0
})

if pending_count > 0:
    frappe.msgprint(f"This document has {pending_count} pending review(s)")
```

## Form Integration

### Automatic Banner (Built-in)

**No code needed!** The Document Review system automatically displays a banner at the top of forms when:
- DocType has Document Review Rules configured
- Document is saved (not new/local)
- Pending reviews exist for the document

The banner:
- Shows pending review count with orange styling
- Includes "See Pending Reviews" button to scroll to timeline
- Tracks via bootinfo for efficient display

### Dashboard Indicator (Custom)

For custom indicators beyond the automatic banner:

**Client Script (Form):**

```javascript
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Get pending review count
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
                callback: function(r) {
                    if (r.message > 0) {
                        frm.dashboard.add_indicator(
                            __("Pending Reviews: {0}", [r.message]),
                            "orange"
                        );
                    }
                }
            });
        }
    }
});
```

### Review Button

Add custom button to review documents.

```javascript
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Reviews"), function() {
                frappe.set_route("List", "Document Review", {
                    reference_doctype: frm.doctype,
                    reference_name: frm.docname
                });
            });
        }
    }
});
```

### Inline Review Dialog

Show review dialog directly in the form.

```javascript
frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            // Check for pending reviews
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Document Review",
                    filters: {
                        reference_doctype: frm.doctype,
                        reference_name: frm.docname,
                        docstatus: 0
                    },
                    fields: ["name", "message", "review_rule", "mandatory"]
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        // Add review button for each pending review
                        r.message.forEach(function(review) {
                            frm.add_custom_button(
                                __("Review: {0}", [review.review_rule]),
                                function() {
                                    show_review_dialog(frm, review);
                                },
                                __("Pending Reviews")
                            );
                        });
                    }
                }
            });
        }
    }
});

function show_review_dialog(frm, review) {
    let d = new frappe.ui.Dialog({
        title: __("Document Review"),
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "message",
                options: `<div class="frappe-card">
                    <h5>Review Required</h5>
                    <p>${review.message}</p>
                    ${review.mandatory ? '<p><strong>This is a mandatory review</strong></p>' : ''}
                </div>`
            },
            {
                fieldtype: "Text Editor",
                fieldname: "review_notes",
                label: __("Review Notes")
            }
        ],
        primary_action_label: __("Approve"),
        primary_action: function(values) {
            frappe.call({
                method: "tweaks.utils.document_review.submit_document_review",
                args: {
                    review_name: review.name,
                    review: values.review_notes,
                    action: "approve"
                },
                callback: function(r) {
                    frappe.show_alert({
                        message: __("Review approved"),
                        indicator: "green"
                    });
                    d.hide();
                    frm.reload_doc();
                }
            });
        },
        secondary_action_label: __("Reject"),
        secondary_action: function(values) {
            frappe.call({
                method: "tweaks.utils.document_review.submit_document_review",
                args: {
                    review_name: review.name,
                    review: values.review_notes,
                    action: "reject"
                },
                callback: function(r) {
                    frappe.show_alert({
                        message: __("Review rejected"),
                        indicator: "red"
                    });
                    d.hide();
                    frm.reload_doc();
                }
            });
        }
    });
    d.show();
}
```

### Prevent Save with Warnings

Show warning before save if reviews will be created.

```javascript
frappe.ui.form.on("Sales Order", {
    before_save: function(frm) {
        // Check if conditions would trigger reviews
        if (frm.doc.grand_total > 100000) {
            frappe.msgprint({
                title: __("Review Required"),
                message: __("This order will require approval due to high value"),
                indicator: "orange"
            });
        }
    }
});
```

## Timeline Integration

Timeline integration is automatic via hooks, but you can customize it.

### Custom Timeline Display

Override the default timeline content:

```python
# In hooks.py
additional_timeline_content = {
    "Sales Order": ["your_app.path.custom_timeline_reviews"]
}

# In your_app/path.py
def custom_timeline_reviews(doctype, docname):
    reviews = frappe.get_all("Document Review", {
        "reference_doctype": doctype,
        "reference_name": docname
    }, ["name", "message", "docstatus", "creation"])
    
    timeline_contents = []
    for review in reviews:
        # Custom formatting
        timeline_contents.append({
            "icon": "assignment",
            "is_card": True,
            "creation": review.creation,
            "content": f"<div class='custom-review'>{review.message}</div>"
        })
    
    return timeline_contents
```

### Timeline Action Buttons

Add custom actions to timeline reviews:

```javascript
// In Custom Script for Document Review
frappe.ui.form.on("Document Review", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__("Quick Approve"), function() {
                frm.set_value("review", "Quick approved");
                frm.save("Submit");
            });
        }
    }
});
```

## Server Script Integration

### Check Reviews Programmatically

```python
# Server Script - Check if reviews are cleared
def check_reviews_cleared(doc):
    pending = frappe.db.count("Document Review", {
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "docstatus": 0
    })
    return pending == 0

# Usage in before_submit
if not check_reviews_cleared(doc):
    frappe.throw("Cannot submit with pending reviews")
```

### Create Review Manually

```python
# Server Script - Create custom review
review = frappe.get_doc({
    "doctype": "Document Review",
    "reference_doctype": doc.doctype,
    "reference_name": doc.name,
    "review_rule": "Manual Review",  # Must be existing rule
    "message": "Custom review created by automation",
    "review_data": {
        "reason": "Automated check failed",
        "details": "..."
    },
    "mandatory": 1
})
review.insert(ignore_permissions=True)
```

### Bulk Review Approval

**Using built-in function (recommended):**
```python
# Server Script - Approve all reviews for a document
results = frappe.call(
    "tweaks.utils.document_review.submit_all_document_reviews",
    doctype="Sales Order",
    docname="SO-00001",
    review="Bulk approved",
    action="approve"  # or "reject"
)

# Returns: {"total": 5, "successful": 5, "failed": 0, "errors": []}
frappe.msgprint(f"Approved {results['successful']} of {results['total']} reviews")
```

**Manual implementation:**
```python
# Server Script - Approve multiple reviews manually
def bulk_approve_reviews(doctype, docname, review_notes="Bulk approved"):
    reviews = frappe.get_all("Document Review", {
        "reference_doctype": doctype,
        "reference_name": docname,
        "docstatus": 0
    }, pluck="name")
    
    for review_name in reviews:
        review = frappe.get_doc("Document Review", review_name)
        review.review = review_notes
        review.submit()
    
    return len(reviews)

# Usage
approved_count = bulk_approve_reviews("Sales Order", "SO-00001")
frappe.msgprint(f"Approved {approved_count} reviews")
```

## Business Logic Integration

### After Review Approval

Trigger actions when review is approved.

```python
# In Document Review controller
def on_submit(self):
    # Call after_review_approval hook if defined
    if hasattr(frappe.get_attr(f"{self.reference_doctype}.after_review_approval"), "__call__"):
        reference_doc = frappe.get_doc(self.reference_doctype, self.reference_name)
        frappe.get_attr(f"{self.reference_doctype}.after_review_approval")(
            reference_doc, self
        )
```

### Custom Notifications

Send email when review is created/approved.

```python
# Server Script - Document Review after_insert
if doc.mandatory:
    # Notify approvers
    approvers = frappe.get_all("User", {
        "role": "Approver"
    }, pluck="email")
    
    frappe.sendmail(
        recipients=approvers,
        subject=f"Review Required: {doc.reference_name}",
        message=f"""
            A document requires your review:
            
            Document: {doc.reference_doctype} {doc.reference_name}
            Reason: {doc.message}
            
            Please review at: {frappe.utils.get_url_to_form("Document Review", doc.name)}
        """
    )
```

## Report Integration

### Review Status Report

Query report showing document review status.

```python
# Query Report - Document Review Status
def execute(filters=None):
    columns = [
        {"label": "Document", "fieldname": "reference_name", "fieldtype": "Dynamic Link", "options": "reference_doctype", "width": 150},
        {"label": "DocType", "fieldname": "reference_doctype", "fieldtype": "Link", "options": "DocType", "width": 120},
        {"label": "Review Rule", "fieldname": "review_rule", "fieldtype": "Link", "options": "Document Review Rule", "width": 180},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Created", "fieldname": "creation", "fieldtype": "Datetime", "width": 150},
    ]
    
    data = frappe.db.sql("""
        SELECT 
            reference_name,
            reference_doctype,
            review_rule,
            CASE 
                WHEN docstatus = 0 THEN 'Pending'
                WHEN docstatus = 1 THEN 'Approved'
                ELSE 'Rejected'
            END as status,
            creation
        FROM `tabDocument Review`
        WHERE reference_doctype = %(doctype)s
        ORDER BY creation DESC
    """, {"doctype": filters.get("doctype")}, as_dict=1)
    
    return columns, data
```

## Permission Integration

### Automatic Permission Filtering

The Document Review system automatically filters reviews based on document access:

```python
# Implemented via permission_query_conditions hook
# Users only see Document Reviews for documents they have read access to
```

This is handled automatically by `get_document_review_permission_query_conditions()`:
- Administrator sees all reviews
- Other users only see reviews for documents they can access
- Queries dynamically filter based on user's document permissions

### Custom Permission Checks

Add additional permission checks to review approval:

```python
# Document Review - has_permission
def has_permission(doc, ptype, user):
    if ptype == "submit":
        # Only allow if user has role "Approver"
        return "Approver" in frappe.get_roles(user)
    
    if ptype == "read":
        # Allow if user has access to referenced document
        return frappe.has_permission(
            doc.reference_doctype,
            ptype="read",
            doc=doc.reference_name,
            user=user
        )
    
    return False
```

### Role-Based Review Assignment

Assign reviews to specific roles based on criteria.

```python
# Document Review Rule Script
# Check user role before creating review
if doc.grand_total > 500000:
    # High value - needs executive approval
    result = {
        "message": "Executive approval required",
        "data": {
            "required_role": "Executive",
            "grand_total": doc.grand_total
        }
    }
else:
    result = None
```

## API Integration

### REST API Access

Access reviews via REST API.

```python
# Get reviews for document
GET /api/resource/Document Review?filters=[["reference_name","=","SO-00001"]]

# Create review manually (if allowed)
POST /api/resource/Document Review
{
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001",
    "review_rule": "Manual Review",
    "message": "API created review"
}

# Submit review
PUT /api/resource/Document Review/{name}
{
    "docstatus": 1,
    "review": "Approved via API"
}
```

### Webhook Integration

Trigger webhooks on review events.

```python
# In Document Review controller
def after_insert(self):
    # Trigger webhook
    frappe.enqueue(
        "frappe.integrations.doctype.webhook.webhook.trigger_webhooks",
        doc=self,
        method="after_insert"
    )
```

Configure webhook in Webhook DocType:
- Document Type: Document Review
- Webhook Event: after_insert
- Request URL: Your endpoint

## Dashboard Integration

### Widget for Pending Reviews

Create dashboard widget showing pending reviews.

```python
# Dashboard Widget
frappe.dashboard.add_widget({
    "name": "Pending Reviews",
    "type": "number_card",
    "label": "Pending Reviews",
    "function": "count",
    "doctype": "Document Review",
    "filters": {"docstatus": 0}
})
```

### Chart for Review Trends

Chart showing review approval rate over time.

```python
# Dashboard Chart
{
    "chart_type": "Line",
    "doctype": "Document Review",
    "filters_json": "{}",
    "time_interval": "Daily",
    "timespan": "Last Month",
    "value_based_on": "docstatus",
    "chart_name": "Review Approval Trend"
}
```

## Automation Integration

### Auto-Approve Based on Criteria

Automatically approve reviews meeting certain criteria.

```python
# Server Script - Document Review after_insert
# Auto-approve if amount is small and customer is trusted
if doc.reference_doctype == "Sales Order":
    sales_order = frappe.get_doc("Sales Order", doc.reference_name)
    customer = frappe.get_doc("Customer", sales_order.customer)
    
    if sales_order.grand_total < 10000 and customer.get("is_trusted"):
        doc.review = "Auto-approved: Trusted customer, low value"
        doc.submit()
```

### Scheduled Review Cleanup

Clean up old approved/rejected reviews.

```python
# Scheduled task - runs daily
def cleanup_old_reviews():
    # Delete reviews older than 90 days
    old_date = frappe.utils.add_days(frappe.utils.today(), -90)
    
    old_reviews = frappe.get_all("Document Review", {
        "creation": ["<", old_date],
        "docstatus": [">", 0]  # Submitted or cancelled
    }, pluck="name")
    
    for review_name in old_reviews:
        frappe.delete_doc("Document Review", review_name)
```

## Best Practices

### Do's

✓ Use workflow conditions for complex approval flows
✓ Display review status prominently in forms
✓ Provide inline review capabilities
✓ Send notifications for urgent reviews
✓ Track review metrics in reports
✓ Clean up old reviews periodically

### Don'ts

✗ Don't bypass review checks in custom code
✗ Don't create duplicate review records
✗ Don't allow submission with pending mandatory reviews
✗ Don't expose sensitive data in review messages
✗ Don't create overly complex review workflows
✗ Don't forget to test permission checks
