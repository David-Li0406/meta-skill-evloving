# Troubleshooting Guide

Common issues, debugging techniques, and solutions for Document Review system.

## Rule Not Triggering

### Issue: Rule doesn't evaluate when document is saved

**Symptoms:**
- Document saves successfully
- No Document Review created
- No errors shown

**Common Causes:**

**1. Rule is disabled**
```python
# Check rule status
rule = frappe.get_doc("Document Review Rule", "Rule Name")
print(f"Disabled: {rule.disabled}")
```

**Solution:** Enable the rule in Document Review Rule form.

**2. Wrong reference_doctype**
```python
# Check reference_doctype
print(f"Rule doctype: {rule.reference_doctype}")
print(f"Document doctype: {doc.doctype}")
```

**Solution:** Ensure reference_doctype matches exactly (case-sensitive).

**3. Cache not cleared**
```python
# Clear cache manually
cache_key = f"document_review_rules:{doctype}"
frappe.cache.delete_value(cache_key)

# Or clear all cache
frappe.cache.delete_keys("document_review_rules:*")
```

**Solution:** Cache clears automatically on rule save, but manual clear may help.

**4. Script returns nothing**
```python
# Bad - doesn't set result
if condition:
    return {"message": "..."}  # Wrong!

# Good - sets result variable
if condition:
    result = {"message": "..."}
else:
    result = None
```

**Solution:** Always set `result` variable, don't use `return`.

**5. In migration/install mode**
```python
# Check flags
print(f"In migrate: {frappe.flags.in_migrate}")
print(f"In install: {frappe.flags.in_install}")
```

**Solution:** Rules don't evaluate during migration. This is expected behavior.

### Debugging Steps

**1. Verify rule exists and is active:**
```python
rules = frappe.get_all("Document Review Rule", {
    "reference_doctype": "Sales Order",
    "disabled": 0
}, ["name", "title", "script"])

for rule in rules:
    print(f"Active rule: {rule.name} - {rule.title}")
```

**2. Test rule script manually:**
```python
# Get document
doc = frappe.get_doc("Sales Order", "SO-00001")

# Get rule
rule = frappe.get_doc("Document Review Rule", "Rule Name")

# Execute script
from frappe.utils.safe_exec import safe_exec
exec_context = {"doc": doc, "result": None}
safe_exec(rule.script, None, exec_context)

# Check result
print(f"Result: {exec_context.get('result')}")
```

**3. Check on_change hook:**
```python
# Verify hook is configured
import tweaks.hooks
print(tweaks.hooks.doc_events)
```

**4. Manually trigger evaluation:**
```python
from tweaks.utils.document_review import evaluate_document_reviews
doc = frappe.get_doc("Sales Order", "SO-00001")
evaluate_document_reviews(doc)
```

## Script Errors

### Issue: Script fails with error message

**Symptoms:**
- Document save fails
- Error message: "Error evaluating Document Review Rule '...'"
- Stack trace in error log

**Common Causes:**

**1. Syntax error**
```python
# Bad syntax
if doc.field = "value":  # Assignment, not comparison

# Good syntax
if doc.field == "value":  # Comparison
```

**Solution:** Check Python syntax, test in console first.

**2. Undefined variable**
```python
# Bad - field doesn't exist
if doc.non_existent_field:
    result = {...}

# Good - check field exists
if doc.get("non_existent_field"):
    result = {...}
```

**Solution:** Use `doc.get("fieldname")` for optional fields.

**3. Query error**
```python
# Bad - no filters
value = frappe.db.get_value("Item Price", "price_list_rate")  # Error!

# Good - with filters
value = frappe.db.get_value("Item Price", 
    {"item_code": doc.item_code},
    "price_list_rate"
)
```

**Solution:** Always provide filters for get_value.

**4. Type error**
```python
# Bad - comparing string to number
if doc.text_field > 100:  # Error if text_field is string

# Good - convert types
from frappe.utils import flt
if flt(doc.text_field) > 100:
```

**Solution:** Use frappe.utils converters (flt, cint, etc.).

**5. Missing import**
```python
# Bad - datetime not imported
order_date = datetime.now()  # Error!

# Good - import from frappe.utils
from frappe.utils import now_datetime
order_date = now_datetime()
```

**Solution:** Import required functions within script.

### Debugging Steps

**1. Check error log:**
```bash
# View error log
bench --site [site] logs

# Or in frappe
frappe.get_all("Error Log", 
    filters={"creation": [">", frappe.utils.add_days(None, -1)]},
    limit=10
)
```

**2. Add try-except for debugging:**
```python
try:
    # Your logic here
    if doc.field > threshold:
        result = {"message": "..."}
except Exception as e:
    # Log error for debugging
    frappe.log_error(f"Review rule error: {str(e)}", "Document Review Debug")
    result = None  # Don't block save
```

**3. Test script in console:**
```python
# Python console
doc = frappe.get_doc("Sales Order", "SO-00001")

# Test logic step by step
print(f"Field value: {doc.grand_total}")
if doc.grand_total > 100000:
    print("Condition met")
else:
    print("Condition not met")
```

**4. Check field values:**
```python
# Print all field values
doc = frappe.get_doc("Sales Order", "SO-00001")
for field in doc.meta.fields:
    print(f"{field.fieldname}: {doc.get(field.fieldname)}")
```

## Review Not Appearing

### Issue: Review created but not visible

**Symptoms:**
- Script executes successfully
- Document Review record exists
- Not visible in timeline or dashboard

**Common Causes:**

**1. Permission issue**
```python
# Check if user can see review
frappe.has_permission("Document Review", ptype="read", doc=review_name)
```

**Solution:** Grant read permission to appropriate roles.

**2. Timeline not refreshing**

**Solution:** Reload the document form (Ctrl+R or F5).

**3. Wrong reference link**
```python
# Verify review links to correct document
review = frappe.get_doc("Document Review", "DR-2024-00001")
print(f"Reference: {review.reference_doctype} - {review.reference_name}")
```

**Solution:** Ensure reference_doctype and reference_name are correct.

**4. Timeline hook not configured**

**Solution:** Verify hook in hooks.py:
```python
additional_timeline_content = {
    "*": ["tweaks.utils.document_review.get_document_reviews_for_timeline"]
}
```

### Debugging Steps

**1. Check if review exists:**
```python
reviews = frappe.get_all("Document Review", {
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001"
}, ["name", "docstatus", "message"])

print(f"Found {len(reviews)} reviews")
for r in reviews:
    print(f"  {r.name} - Status: {r.docstatus}")
```

**2. Manually load timeline:**
```python
from tweaks.utils.document_review import get_document_reviews_for_timeline
timeline = get_document_reviews_for_timeline("Sales Order", "SO-00001")
print(timeline)
```

**3. Check bootinfo:**
```python
# Verify doctype is in bootinfo
bootinfo = frappe.cache.get_value("bootinfo")
print(bootinfo.get("doctypes_with_document_review_rules"))
```

## Submission Not Blocked

### Issue: Document submits despite pending mandatory review

**Symptoms:**
- Document Review exists with mandatory=1, docstatus=0
- Document submission succeeds
- No error shown

**Important:** Since version with auto-approval feature, the `check_mandatory_reviews` function now attempts to auto-approve all pending reviews before blocking submission. This means:
- Non-mandatory reviews are auto-approved during submission
- Mandatory reviews that can't be auto-approved will still block
- This ensures smoother workflow while maintaining approval requirements

**Common Causes:**

**1. before_submit hook not configured**

**Solution:** Verify hook in hooks.py:
```python
doc_events = {
    "*": {
        "before_submit": ["tweaks.utils.document_review.check_mandatory_reviews"]
    }
}
```

**2. Review not marked mandatory**
```python
# Check mandatory flag
review = frappe.get_doc("Document Review", "DR-2024-00001")
print(f"Mandatory: {review.mandatory}")
```

**Solution:** Ensure rule has mandatory=1 checked.

**3. Review is cancelled or already submitted**
```python
# Check docstatus
print(f"Docstatus: {review.docstatus}")
# 0 = Draft (pending), 1 = Submitted (approved), 2 = Cancelled (rejected)
```

**Solution:** Only draft reviews (docstatus=0) block submission.

**4. Submission bypassing hooks**
```python
# Bad - bypasses hooks
doc.db_set("docstatus", 1)

# Good - triggers hooks (including auto-approval)
doc.submit()
```

**Solution:** Always use doc.submit(), not direct DB updates.

### Debugging Steps

**1. Check pending mandatory reviews:**
```python
pending = frappe.get_all("Document Review", {
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001",
    "docstatus": 0,
    "mandatory": 1
}, ["name", "review_rule"])

print(f"Pending mandatory: {len(pending)}")
```

**2. Test check function:**
```python
from tweaks.utils.document_review import check_mandatory_reviews
doc = frappe.get_doc("Sales Order", "SO-00001")
try:
    check_mandatory_reviews(doc)
    print("Check passed - no pending reviews")
except Exception as e:
    print(f"Check failed: {str(e)}")
```

**3. Verify hook execution:**
```python
# Add debug logging in check_mandatory_reviews
def check_mandatory_reviews(doc, method=None):
    frappe.log_error("check_mandatory_reviews called", "Debug")
    # ... rest of function
```

## Performance Issues

### Issue: Document saves are slow

**Symptoms:**
- Document save takes several seconds
- Noticeable delay on every save
- Multiple documents affected

**Common Causes:**

**1. Inefficient script**
```python
# Bad - query in loop
for item in doc.items:
    price = frappe.db.get_value("Item Price", 
        {"item_code": item.item_code}, 
        "price_list_rate"
    )

# Good - batch query
item_codes = [item.item_code for item in doc.items]
prices = frappe._dict(frappe.get_all("Item Price",
    filters={"item_code": ["in", item_codes]},
    fields=["item_code", "price_list_rate"],
    as_list=1
))
for item in doc.items:
    price = prices.get(item.item_code)
```

**Solution:** Batch database queries outside loops.

**2. No early exit**
```python
# Bad - checks everything
for item in doc.items:
    if item.qty > threshold:
        has_issue = True

# Good - exit early
for item in doc.items:
    if item.qty > threshold:
        result = {"message": "..."}
        break  # Stop checking
else:
    result = None
```

**Solution:** Exit loops early when condition is met.

**3. Too many rules**
```python
# Check rule count
rules = frappe.get_all("Document Review Rule", {
    "reference_doctype": "Sales Order",
    "disabled": 0
})
print(f"Active rules: {len(rules)}")
```

**Solution:** Combine related rules, disable unused rules.

**4. Complex computation**
```python
# Bad - complex calculation every save
result = expensive_api_call(doc)

# Good - cache results
cache_key = f"review_check:{doc.name}"
result = frappe.cache.get_value(cache_key)
if result is None:
    result = expensive_api_call(doc)
    frappe.cache.set_value(cache_key, result, expires_in_sec=300)
```

**Solution:** Cache expensive operations.

### Debugging Steps

**1. Profile script execution:**
```python
import time

start = time.time()
# Your script logic
end = time.time()

frappe.log_error(f"Script took {end - start:.2f} seconds", "Performance")
```

**2. Identify slow queries:**
```python
# Enable query logging
frappe.db.sql("SET profiling = 1")

# Run your script
# ...

# View query times
queries = frappe.db.sql("SHOW PROFILES", as_dict=1)
for q in queries:
    print(f"Query took {q.Duration} seconds")
```

**3. Optimize database queries:**
```python
# Check if indexes exist
frappe.db.sql("""
    SHOW INDEX FROM `tabDocument Review`
    WHERE Column_name IN ('reference_doctype', 'reference_name', 'review_rule')
""")
```

## Review Not Deleting

### Issue: Draft review persists when condition no longer met

**Symptoms:**
- Document changed to not meet rule condition
- Draft review still exists
- Expected: Review should be auto-deleted

**Common Causes:**

**1. Script still returns result**
```python
# Debug: Check what script returns
doc = frappe.get_doc("Sales Order", "SO-00001")
rule = frappe.get_doc("Document Review Rule", "Rule Name")

from frappe.utils.safe_exec import safe_exec
exec_context = {"doc": doc, "result": None}
safe_exec(rule.script, None, exec_context)

print(f"Script result: {exec_context.get('result')}")
# Should be None if condition not met
```

**Solution:** Ensure script sets `result = None` when condition not met.

**2. Different rule name**
```python
# Check which rule created the review
review = frappe.get_doc("Document Review", "DR-2024-00001")
print(f"Created by rule: {review.review_rule}")

# Check if rule still exists
if frappe.db.exists("Document Review Rule", review.review_rule):
    print("Rule exists")
else:
    print("Rule was deleted")
```

**Solution:** Reviews from deleted rules must be manually deleted.

**3. Review already submitted**
```python
# Check docstatus
review = frappe.get_doc("Document Review", "DR-2024-00001")
print(f"Docstatus: {review.docstatus}")
# 0 = Draft (can be deleted), 1/2 = Submitted/Cancelled (can't be deleted)
```

**Solution:** Only draft reviews (docstatus=0) are auto-deleted.

### Debugging Steps

**1. Manually delete draft reviews:**
```python
# Delete specific review
frappe.delete_doc("Document Review", "DR-2024-00001")

# Delete all draft reviews for document
reviews = frappe.get_all("Document Review", {
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001",
    "docstatus": 0
}, pluck="name")

for review_name in reviews:
    frappe.delete_doc("Document Review", review_name)
```

**2. Test delete function:**
```python
from tweaks.utils.document_review import _delete_draft_reviews
_delete_draft_reviews("Sales Order", "SO-00001", "Rule Name")
```

## Data Not Updating

### Issue: Review data doesn't update when document changes

**Symptoms:**
- Document values changed
- Review still shows old data
- Expected: Review should update with new data

**Common Causes:**

**1. Submitted review with same data**
```python
# Check for submitted reviews
submitted = frappe.get_all("Document Review", {
    "reference_doctype": "Sales Order",
    "reference_name": "SO-00001",
    "review_rule": "Rule Name",
    "docstatus": 1
}, ["name", "review_data"])

print(f"Submitted reviews: {len(submitted)}")
```

**Solution:** If identical submitted review exists, no new draft is created.

**2. Data not included in result**
```python
# Bad - no data field
result = {
    "message": "Review needed"
}

# Good - includes data
result = {
    "message": "Review needed",
    "data": {
        "field1": doc.field1,
        "field2": doc.field2
    }
}
```

**Solution:** Include relevant data in `data` field.

**3. Data comparison issue**
```python
# Data is compared as JSON strings
# Different field order = different JSON = new review

# Prefer consistent field order
result = {
    "message": "...",
    "data": {
        "field1": value1,  # Always same order
        "field2": value2
    }
}
```

**Solution:** Maintain consistent field order in data dict.

### Debugging Steps

**1. Check review data:**
```python
review = frappe.get_doc("Document Review", "DR-2024-00001")
print(f"Review data: {review.review_data}")
```

**2. Compare data:**
```python
import json
old_data = json.loads(review.review_data)
new_data = {"field1": "new_value"}

print(f"Old: {old_data}")
print(f"New: {new_data}")
print(f"Same: {old_data == new_data}")
```

## Best Practices for Debugging

### Development Environment

**1. Enable debug mode:**
```python
# site_config.json
{
    "developer_mode": 1,
    "logging": 2
}
```

**2. Use frappe.log_error:**
```python
# In rule script
try:
    # Logic
    frappe.log_error(f"Debug info: {doc.field}", "Review Debug")
except Exception as e:
    frappe.log_error(str(e), "Review Error")
```

**3. Console testing:**
```python
# Test in bench console
bench console

>>> doc = frappe.get_doc("Sales Order", "SO-00001")
>>> # Test logic here
```

### Logging

**Add debug logging to rules:**
```python
# At start of script
frappe.log_error(f"Evaluating rule for {doc.name}", "Review Start")

# Before returning result
frappe.log_error(f"Result: {result}", "Review Result")
```

### Testing Checklist

- [ ] Rule is enabled
- [ ] reference_doctype matches exactly
- [ ] Script syntax is valid
- [ ] Script sets `result` variable (not return)
- [ ] Script handles None/empty values
- [ ] Hooks are configured in hooks.py
- [ ] Permissions allow review creation/viewing
- [ ] Cache is cleared if needed
- [ ] Error log checked for issues

### Common Gotchas

1. **Use `result =` not `return`** - Scripts must set variable
2. **Check `doc.get("field")` not `doc.field`** - Handles missing fields
3. **Clear cache after rule changes** - Cache may be stale
4. **Hooks apply to all doctypes** - Use `"*"` in doc_events
5. **Reviews are cached per doctype** - Changes may not be immediate
6. **Timeline needs page refresh** - F5 to see new reviews
7. **Submitted reviews block deletion** - Only drafts auto-delete
8. **Data comparison is exact** - Same data = no new review

### Getting Help

If still stuck:

1. Check error logs: `bench --site [site] logs`
2. Test in console: `bench console`
3. Enable debug logging in scripts
4. Check hooks.py configuration
5. Verify permissions on Document Review
6. Clear all caches: `bench --site [site] clear-cache`
7. Review this troubleshooting guide
8. Check Frappe forums or documentation
