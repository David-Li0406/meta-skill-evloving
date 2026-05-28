# Rule Creation Guide

Step-by-step guide to creating effective Document Review Rules.

## Before You Start

### Understanding Rule Triggers

Rules are evaluated on the `on_change` event, which triggers when:
- Document is saved (both new and existing)
- Any field value changes
- Child table rows are added/modified/deleted
- Document is loaded and saved (even without changes)

**Not triggered on:**
- Document load (read-only)
- Form field changes before save
- Draft to submitted transition (before_submit runs instead)

### Planning Your Rule

Ask these questions:

1. **What condition triggers the need for review?**
   - Field value exceeds threshold
   - Required data is missing
   - Combination of conditions met
   - External data check fails

2. **Who should review?**
   - Specific role (handled by permissions)
   - Document owner's manager
   - Department head
   - External approver

3. **Is the review mandatory?**
   - Must be approved before submission
   - Optional recommendation only

4. **What information does the reviewer need?**
   - Context about the issue
   - Related data for decision-making
   - Comparison values

## Step 1: Create the Rule

### Via UI

1. Navigate to **Document Review Rule** list
2. Click **New**
3. Fill in basic information:
   - **Title**: Clear, descriptive name (e.g., "High Value Order Approval")
   - **Reference DocType**: The DocType to monitor (e.g., "Sales Order")
   - **Mandatory**: Check if submission should be blocked
   - **Disabled**: Leave unchecked (check to temporarily disable)
4. Configure auto-assignment (optional):
   - In **Assign Users** table, add users who should be auto-assigned to reviews
   - For each user, set **Ignore Permissions** checkbox:
     - Unchecked: User will only be assigned if they have submit permission on Document Review AND read permission on referenced document
     - Checked: User will be assigned regardless of permissions
   - Assignments are created on the referenced document with the review message as the todo description
   - Multiple reviews for the same document use union logic - users are only notified once

### Via Code

```python
rule = frappe.get_doc({
    "doctype": "Document Review Rule",
    "title": "High Value Order Approval",
    "reference_doctype": "Sales Order",
    "mandatory": 1,
    "disabled": 0,
    "users": [
        {"user": "approver1@example.com", "ignore_permissions": 0},  # Check permissions
        {"user": "approver2@example.com", "ignore_permissions": 1}   # Ignore permissions
    ],
    "script": """
# Script goes here
"""
})
rule.insert()
```

## Step 2: Write the Script

### Basic Template

```python
# Access document via 'doc' variable
# Set 'result' variable to None or dict

# Check condition
if doc.some_field > threshold:
    # Review needed
    result = {
        "message": "Clear explanation of why review is needed",
        "data": {
            "field1": doc.field1,
            "field2": doc.field2
        }
    }
else:
    # No review needed
    result = None
```

### Script Checklist

- [ ] Accessed document via `doc` variable
- [ ] Set `result` to `None` or dict (not return statement)
- [ ] Provided clear `message` field
- [ ] Included relevant `data` for reviewers
- [ ] Handled edge cases (None values, empty lists, etc.)
- [ ] Tested logic in console before saving rule

## Step 3: Test the Rule

### Manual Testing

1. **Save the rule**
   - Creates cache entry
   - Takes effect immediately

2. **Open a document of the target DocType**
   - Create new or edit existing

3. **Trigger the condition**
   - Set fields to values that should require review

4. **Save the document**
   - Check timeline for Document Review

5. **Verify review details**
   - Message is clear and helpful
   - Data is formatted correctly
   - Status shows as pending

6. **Test approval flow**
   - Click "Review" button
   - Submit the review
   - Verify document can now be submitted (if mandatory)

7. **Test condition removal**
   - Change document to not meet condition
   - Save again
   - Verify review is deleted automatically

### Console Testing

Test script logic before saving rule:

```python
# Get a test document
doc = frappe.get_doc("Sales Order", "SO-00001")

# Test your script logic
if doc.grand_total > 100000:
    result = {
        "message": f"Order total {doc.grand_total} exceeds threshold",
        "data": {"total": doc.grand_total}
    }
else:
    result = None

print(result)
```

### Automated Testing

Create test case:

```python
def test_review_rule():
    # Create test document
    doc = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": "Test Customer",
        "grand_total": 150000
    })
    doc.insert()
    
    # Verify review was created
    reviews = frappe.get_all("Document Review", {
        "reference_doctype": "Sales Order",
        "reference_name": doc.name,
        "docstatus": 0
    })
    
    assert len(reviews) == 1, "Review not created"
    
    # Change to not require review
    doc.grand_total = 50000
    doc.save()
    
    # Verify review was deleted
    reviews = frappe.get_all("Document Review", {
        "reference_doctype": "Sales Order",
        "reference_name": doc.name,
        "docstatus": 0
    })
    
    assert len(reviews) == 0, "Review not deleted"
```

## Step 4: Refine and Deploy

### Optimization

**Early exits:**
```python
# Good: Exit early when no review needed
if not doc.items:
    result = None
else:
    # Check items...
```

**Cache external lookups:**
```python
# Good: Cache repeated queries
threshold = frappe.cache.get_value("approval_threshold")
if not threshold:
    threshold = frappe.db.get_single_value("Settings", "approval_threshold")
    frappe.cache.set_value("approval_threshold", threshold, expires_in_sec=3600)
```

**Minimize queries:**
```python
# Bad: Query in loop
for item in doc.items:
    price = frappe.db.get_value("Item Price", item.item_code, "price_list_rate")

# Good: Single query
prices = frappe._dict(frappe.get_all("Item Price", 
    filters={"item_code": ["in", [i.item_code for i in doc.items]]},
    fields=["item_code", "price_list_rate"],
    as_list=1
))
for item in doc.items:
    price = prices.get(item.item_code)
```

### Error Handling

**Handle missing data:**
```python
# Check for None/empty values
if doc.customer and doc.grand_total:
    credit_limit = frappe.db.get_value("Customer", doc.customer, "credit_limit")
    if credit_limit and doc.grand_total > credit_limit:
        result = {"message": "..."}
```

**Catch exceptions:**
```python
try:
    # External API call or complex logic
    response = external_api.check(doc)
    if not response.ok:
        result = {"message": "External validation failed"}
except Exception as e:
    # Log error but don't block save
    frappe.log_error(f"Review rule error: {str(e)}")
    result = None
```

### Documentation

Add helpful comments in the script:

```python
# Check if order exceeds customer's credit limit
# Requires: Customer has credit_limit set
# Triggers: When grand_total > credit_limit

credit_limit = frappe.db.get_value("Customer", doc.customer, "credit_limit")

if credit_limit and doc.grand_total > credit_limit:
    result = {
        "message": f"Order total exceeds credit limit by {doc.grand_total - credit_limit}",
        "data": {
            "grand_total": doc.grand_total,
            "credit_limit": credit_limit,
            "excess_amount": doc.grand_total - credit_limit
        }
    }
else:
    result = None
```

## Common Patterns

### Threshold Check

```python
threshold = 100000

if doc.grand_total > threshold:
    result = {
        "message": f"Order value {doc.grand_total} exceeds approval threshold {threshold}",
        "data": {
            "total": doc.grand_total,
            "threshold": threshold,
            "excess": doc.grand_total - threshold
        }
    }
else:
    result = None
```

### Required Field Check

```python
missing_fields = []

if not doc.tax_id:
    missing_fields.append("Tax ID")
if not doc.delivery_date:
    missing_fields.append("Delivery Date")

if missing_fields:
    result = {
        "message": f"Required fields missing: {', '.join(missing_fields)}",
        "data": {"missing_fields": missing_fields}
    }
else:
    result = None
```

### Child Table Validation

```python
issues = []

for item in doc.items:
    min_price = frappe.db.get_value("Item Price", {
        "item_code": item.item_code,
        "price_list": doc.selling_price_list
    }, "min_price")
    
    if min_price and item.rate < min_price:
        issues.append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "rate": item.rate,
            "min_price": min_price
        })

if issues:
    result = {
        "message": f"{len(issues)} items are below minimum price",
        "data": {"items": issues}
    }
else:
    result = None
```

### External Data Check

```python
# Check if customer is blacklisted
is_blacklisted = frappe.db.get_value("Customer", doc.customer, "is_blacklisted")

if is_blacklisted:
    result = {
        "message": "Customer is blacklisted - requires approval",
        "data": {
            "customer": doc.customer,
            "customer_name": doc.customer_name
        }
    }
else:
    result = None
```

### Percentage-Based Check

```python
# Check discount percentage
for item in doc.items:
    if item.discount_percentage > 20:
        result = {
            "message": f"Item {item.item_name} has discount above 20%",
            "data": {
                "item_code": item.item_code,
                "item_name": item.item_name,
                "discount": item.discount_percentage
            }
        }
        break  # Only flag first occurrence
else:
    result = None
```

### Multi-Condition Check

```python
# Complex approval logic
requires_review = False
reasons = []

# Check 1: High value
if doc.grand_total > 100000:
    requires_review = True
    reasons.append("High value order")

# Check 2: New customer
customer_age_days = (frappe.utils.today() - 
    frappe.db.get_value("Customer", doc.customer, "creation")).days
if customer_age_days < 30:
    requires_review = True
    reasons.append("New customer")

# Check 3: Unusual payment terms
if doc.payment_terms_template != "Standard":
    requires_review = True
    reasons.append("Non-standard payment terms")

if requires_review:
    result = {
        "message": f"Review required: {', '.join(reasons)}",
        "data": {
            "reasons": reasons,
            "total": doc.grand_total,
            "customer_age": customer_age_days
        }
    }
else:
    result = None
```

## Best Practices Summary

### Do's

✓ Write clear, specific messages explaining why review is needed
✓ Include relevant data for reviewer decision-making
✓ Exit early when condition not met (return `result = None`)
✓ Handle None/empty values gracefully
✓ Test thoroughly before deploying
✓ Use caching for repeated lookups
✓ Document complex logic with comments

### Don'ts

✗ Don't use `return` statement (set `result` variable instead)
✗ Don't modify the document in the script
✗ Don't raise exceptions for business logic (use `result` dict)
✗ Don't query in loops (batch queries instead)
✗ Don't expose sensitive data in messages
✗ Don't write overly complex scripts (break into helper functions if needed)

## Troubleshooting

**Rule not evaluating:**
- Check if rule is disabled
- Verify reference_doctype matches exactly
- Clear cache: `frappe.cache.delete_value(f"document_review_rules:{doctype}")`

**Script errors:**
- Test logic in console first
- Add try-except for debugging
- Check error log: `bench --site [site] logs`

**Review not appearing:**
- Verify `result` variable is set (not returned)
- Check timeline in source document
- Look for Document Review records manually

**Performance issues:**
- Reduce database queries
- Cache external lookups
- Exit early when possible
- Simplify complex logic
