# Script Examples

Working examples of Document Review Rule scripts for common scenarios.

## Script Return Formats

Document Review Rule scripts support two ways to indicate that a review is needed:

### Option 1: Using `result` variable (traditional approach)
```python
result = {
    "title": "Review Title",  # Optional
    "message": "Review message here",
    "data": {"key": "value"}  # Optional
}
```

### Option 2: Using direct `title`, `message`, and `data` variables (new approach)
```python
title = "Review Title"  # Optional
message = "Review message here"
data = {"key": "value"}  # Optional
```

**Note:** The `result` variable takes precedence if both are set. If neither `result` nor `message` is set, no review will be created.

## Example 1: Simple Threshold Check

**Scenario:** Orders above $100,000 require manager approval.

```python
# High Value Order Approval
threshold = 100000

if doc.grand_total and doc.grand_total > threshold:
    result = {
        "title": "High Value Order",
        "message": f"Order value ${doc.grand_total:,.2f} exceeds approval threshold of ${threshold:,.2f}",
        "data": {
            "grand_total": doc.grand_total,
            "threshold": threshold,
            "excess_amount": doc.grand_total - threshold
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "High Value Order Approval"
- Reference DocType: "Sales Order"
- Mandatory: Yes

### Alternative using direct variables:
```python
# High Value Order Approval (using direct variables)
threshold = 100000

if doc.grand_total and doc.grand_total > threshold:
    message = f"Order value ${doc.grand_total:,.2f} exceeds approval threshold of ${threshold:,.2f}"
    data = {
        "grand_total": doc.grand_total,
        "threshold": threshold,
        "excess_amount": doc.grand_total - threshold
    }
```

## Example 2: Credit Limit Check

**Scenario:** Flag orders that exceed customer's credit limit.

```python
# Credit Limit Check
if not doc.customer:
    result = None
else:
    customer = frappe.get_doc("Customer", doc.customer)
    credit_limit = customer.credit_limit or 0
    
    if credit_limit > 0 and doc.grand_total > credit_limit:
        result = {
            "message": f"Order total ${doc.grand_total:,.2f} exceeds customer credit limit ${credit_limit:,.2f}",
            "data": {
                "customer": doc.customer,
                "customer_name": doc.customer_name,
                "grand_total": doc.grand_total,
                "credit_limit": credit_limit,
                "excess": doc.grand_total - credit_limit
            }
        }
    else:
        result = None
```

**Rule Configuration:**
- Title: "Credit Limit Exceeded"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 3: Discount Approval

**Scenario:** Items with discount above 15% require approval.

```python
# Discount Approval
high_discount_items = []

for item in doc.items:
    discount_pct = item.discount_percentage or 0
    
    if discount_pct > 15:
        high_discount_items.append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "rate": item.rate,
            "discount_percentage": discount_pct,
            "discounted_amount": item.amount
        })

if high_discount_items:
    result = {
        "message": f"{len(high_discount_items)} item(s) have discount above 15% - requires approval",
        "data": {
            "items": high_discount_items,
            "total_items": len(high_discount_items)
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "High Discount Approval"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 4: Below Minimum Price

**Scenario:** Items sold below minimum price require approval.

```python
# Below Minimum Price Check
below_min_items = []

# Get all item codes from the order
item_codes = [item.item_code for item in doc.items]

# Batch query for minimum prices
min_prices = frappe._dict(
    frappe.get_all("Item Price",
        filters={
            "item_code": ["in", item_codes],
            "price_list": doc.selling_price_list
        },
        fields=["item_code", "min_price"],
        as_list=1
    )
)

# Check each item
for item in doc.items:
    min_price = min_prices.get(item.item_code)
    
    if min_price and item.rate < min_price:
        below_min_items.append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "selling_rate": item.rate,
            "min_price": min_price,
            "difference": min_price - item.rate
        })

if below_min_items:
    result = {
        "message": f"{len(below_min_items)} item(s) priced below minimum - requires approval",
        "data": {
            "items": below_min_items,
            "price_list": doc.selling_price_list
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Below Minimum Price"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 5: Required Fields Check

**Scenario:** Critical fields must be filled before submission.

```python
# Required Fields Check
missing_fields = []
field_labels = {
    "tax_id": "Tax ID",
    "delivery_date": "Delivery Date",
    "payment_terms_template": "Payment Terms",
    "po_no": "Purchase Order Number"
}

for fieldname, label in field_labels.items():
    if not doc.get(fieldname):
        missing_fields.append(label)

if missing_fields:
    result = {
        "message": f"Required fields missing: {', '.join(missing_fields)}",
        "data": {
            "missing_fields": missing_fields,
            "count": len(missing_fields)
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Required Fields Check"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 6: New Customer Approval

**Scenario:** Orders from customers less than 30 days old require approval.

```python
# New Customer Approval
if not doc.customer:
    result = None
else:
    customer_creation = frappe.db.get_value("Customer", doc.customer, "creation")
    
    if customer_creation:
        customer_age_days = (frappe.utils.today_date() - customer_creation.date()).days
        
        if customer_age_days < 30:
            result = {
                "message": f"New customer (registered {customer_age_days} days ago) - requires approval",
                "data": {
                    "customer": doc.customer,
                    "customer_name": doc.customer_name,
                    "registration_date": str(customer_creation),
                    "age_days": customer_age_days
                }
            }
        else:
            result = None
    else:
        result = None
```

**Rule Configuration:**
- Title: "New Customer Approval"
- Reference DocType: "Sales Order"
- Mandatory: No

## Example 7: Multi-Level Approval

**Scenario:** Different approval requirements based on order value.

```python
# Multi-Level Approval
approval_required = False
approval_level = None
approval_message = None

if doc.grand_total > 500000:
    approval_required = True
    approval_level = "Executive"
    approval_message = "Executive approval required for orders above $500,000"
elif doc.grand_total > 250000:
    approval_required = True
    approval_level = "Senior Manager"
    approval_message = "Senior Manager approval required for orders above $250,000"
elif doc.grand_total > 100000:
    approval_required = True
    approval_level = "Manager"
    approval_message = "Manager approval required for orders above $100,000"

if approval_required:
    result = {
        "message": approval_message,
        "data": {
            "grand_total": doc.grand_total,
            "approval_level": approval_level
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Multi-Level Approval"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 8: Blacklist Check

**Scenario:** Orders from blacklisted customers need special approval.

```python
# Blacklist Check
if not doc.customer:
    result = None
else:
    customer = frappe.get_doc("Customer", doc.customer)
    
    if customer.get("is_blacklisted"):
        blacklist_reason = customer.get("blacklist_reason") or "No reason specified"
        
        result = {
            "message": f"Customer is blacklisted - special approval required",
            "data": {
                "customer": doc.customer,
                "customer_name": doc.customer_name,
                "blacklist_reason": blacklist_reason
            }
        }
    else:
        result = None
```

**Rule Configuration:**
- Title: "Blacklisted Customer Check"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 9: Stock Availability Check

**Scenario:** Flag orders with insufficient stock for approval.

```python
# Stock Availability Check
from frappe.utils import flt

insufficient_stock_items = []

for item in doc.items:
    if item.warehouse:
        # Get available stock
        available_stock = frappe.db.get_value("Bin", 
            {"item_code": item.item_code, "warehouse": item.warehouse},
            "actual_qty"
        ) or 0
        
        if flt(item.qty) > flt(available_stock):
            insufficient_stock_items.append({
                "item_code": item.item_code,
                "item_name": item.item_name,
                "ordered_qty": item.qty,
                "available_qty": available_stock,
                "shortage": item.qty - available_stock,
                "warehouse": item.warehouse
            })

if insufficient_stock_items:
    result = {
        "message": f"{len(insufficient_stock_items)} item(s) have insufficient stock - requires approval to proceed",
        "data": {
            "items": insufficient_stock_items,
            "note": "Order fulfillment will be delayed"
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Insufficient Stock Approval"
- Reference DocType: "Sales Order"
- Mandatory: No

## Example 10: Payment Terms Validation

**Scenario:** Non-standard payment terms require approval.

```python
# Payment Terms Validation
standard_terms = ["Immediate", "Net 30", "Net 60"]

if doc.payment_terms_template and doc.payment_terms_template not in standard_terms:
    result = {
        "message": f"Non-standard payment terms '{doc.payment_terms_template}' require approval",
        "data": {
            "payment_terms": doc.payment_terms_template,
            "standard_terms": standard_terms
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Non-Standard Payment Terms"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 11: Shipping Method Validation

**Scenario:** Express shipping on large orders needs approval.

```python
# Express Shipping Approval
if doc.shipping_rule == "Express" and doc.total_qty > 100:
    shipping_cost = frappe.db.get_value("Shipping Rule", "Express", "shipping_amount")
    
    result = {
        "message": f"Express shipping for order with {doc.total_qty} items requires approval due to high cost",
        "data": {
            "shipping_rule": doc.shipping_rule,
            "total_qty": doc.total_qty,
            "estimated_shipping_cost": shipping_cost,
            "suggestion": "Consider standard shipping to reduce costs"
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Express Shipping Approval"
- Reference DocType: "Sales Order"
- Mandatory: No

## Example 12: Territory-Based Approval

**Scenario:** Orders in certain territories require regional manager approval.

```python
# Territory-Based Approval
high_risk_territories = ["International", "South America", "Middle East"]

if doc.territory in high_risk_territories:
    result = {
        "message": f"Orders in {doc.territory} territory require regional manager approval",
        "data": {
            "territory": doc.territory,
            "grand_total": doc.grand_total,
            "customer": doc.customer_name
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Territory Approval Required"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 13: Combined Conditions

**Scenario:** Multiple factors determine if approval is needed.

```python
# Combined Conditions Check
review_reasons = []

# Check 1: High value
if doc.grand_total > 100000:
    review_reasons.append(f"High value order (${doc.grand_total:,.2f})")

# Check 2: New customer
if doc.customer:
    customer_age = frappe.db.sql("""
        SELECT DATEDIFF(CURDATE(), creation) as age_days
        FROM `tabCustomer`
        WHERE name = %s
    """, doc.customer)[0][0]
    
    if customer_age < 30:
        review_reasons.append(f"New customer ({customer_age} days old)")

# Check 3: High discount
max_discount = max([item.discount_percentage or 0 for item in doc.items] or [0])
if max_discount > 15:
    review_reasons.append(f"High discount ({max_discount}%)")

# Check 4: Non-standard payment terms
if doc.payment_terms_template not in ["Immediate", "Net 30"]:
    review_reasons.append(f"Non-standard payment terms ({doc.payment_terms_template})")

if review_reasons:
    result = {
        "message": "Multiple factors require approval: " + "; ".join(review_reasons),
        "data": {
            "reasons": review_reasons,
            "grand_total": doc.grand_total,
            "customer": doc.customer_name
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Combined Risk Factors"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 14: Custom DocType Field Check

**Scenario:** Custom field requires validation.

```python
# Custom Field Validation
# Assumes Sales Order has custom field 'custom_requires_insurance'

if doc.get("custom_requires_insurance") and not doc.get("custom_insurance_certificate"):
    result = {
        "message": "Order requires insurance but certificate is not attached",
        "data": {
            "custom_requires_insurance": doc.custom_requires_insurance,
            "custom_insurance_certificate": doc.custom_insurance_certificate
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "Insurance Certificate Required"
- Reference DocType: "Sales Order"
- Mandatory: Yes

## Example 15: Time-Based Rule

**Scenario:** Orders placed outside business hours need approval.

```python
# After-Hours Order Check
from datetime import datetime

order_time = frappe.utils.get_datetime(doc.creation)
order_hour = order_time.hour

# Business hours: 9 AM to 5 PM
if order_hour < 9 or order_hour >= 17:
    result = {
        "message": f"Order placed outside business hours ({order_time.strftime('%I:%M %p')}) - requires approval",
        "data": {
            "order_time": str(order_time),
            "order_hour": order_hour,
            "note": "Verify order details carefully"
        }
    }
else:
    result = None
```

**Rule Configuration:**
- Title: "After-Hours Order Approval"
- Reference DocType: "Sales Order"
- Mandatory: No

## Script Patterns Summary

### Early Exit Pattern
```python
# Check if condition applies
if not doc.field:
    result = None
else:
    # Validation logic
    if condition:
        result = {...}
    else:
        result = None
```

### List Collection Pattern
```python
# Collect issues
issues = []
for item in doc.items:
    if item.check_fails():
        issues.append({...})

if issues:
    result = {"message": "...", "data": {"issues": issues}}
else:
    result = None
```

### Threshold Pattern
```python
# Define thresholds
thresholds = {
    "high": 500000,
    "medium": 250000,
    "low": 100000
}

# Check against thresholds
for level, amount in thresholds.items():
    if doc.grand_total > amount:
        result = {"message": f"{level} approval", "data": {...}}
        break
else:
    result = None
```

### Batch Query Pattern
```python
# Collect IDs
ids = [item.item_code for item in doc.items]

# Batch query
data = frappe._dict(frappe.get_all("DocType",
    filters={"name": ["in", ids]},
    fields=["name", "field"],
    as_list=1
))

# Use data
for item in doc.items:
    value = data.get(item.item_code)
```

## Testing Scripts

Test in console before saving:

```python
# Get test document
doc = frappe.get_doc("Sales Order", "SO-00001")

# Your script logic here
if doc.grand_total > 100000:
    result = {
        "message": "Test message",
        "data": {"total": doc.grand_total}
    }
else:
    result = None

# Verify result
print(result)
```


## Available Functions in Scripts

Document Review Rule scripts have access to additional functions via safe_exec globals:

### Document Review Functions

Available in rule scripts for advanced use cases:

```python
# Get all rules for a doctype (cached)
rules = document_review.get_rules_for_doctype("Sales Order")

# Get review status for a document
status = document_review.get_document_review_status("Sales Order", "SO-00001")
# Returns: "Approved", "Pending Review", "Can Approve", or "Can Submit"

# Submit all pending reviews for a document
result = document_review.submit_all_document_reviews(
    "Sales Order", 
    "SO-00001",
    review="Auto-approved",
    action="approve"
)
# Returns: {"total": 5, "successful": 5, "failed": 0, "errors": []}

# Submit a specific review
review_doc = document_review.submit_document_review(
    "REV-00001",
    review="Approved",
    action="approve"
)
```

**Note:** These are also available in:
- Workflow transition conditions (via `workflow_safe_eval_globals` hook) - only `get_document_review_status`
- Server Scripts and Business Logic (via `safe_exec_globals`)
- Custom Scripts (via standard Frappe API)

