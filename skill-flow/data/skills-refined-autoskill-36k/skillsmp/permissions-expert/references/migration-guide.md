# Migration Guide: Adding Permissions to Existing DocTypes

This guide provides step-by-step instructions for adding custom permissions to existing DocTypes.

## Table of Contents

- [Step 1: Plan Permission Rules](#step-1-plan-permission-rules)
- [Step 2: Choose Appropriate Hooks](#step-2-choose-appropriate-hooks)
- [Step 3: Implement Permission Hooks](#step-3-implement-permission-hooks)
- [Step 4: Test Your Implementation](#step-4-test-your-implementation)
- [Step 5: Add More Complex Logic](#step-5-add-more-complex-logic-if-needed)
- [Step 6: Update Role Permissions](#step-6-update-role-permissions)
- [Step 7: Setup User Permissions](#step-7-setup-user-permissions-if-needed)
- [Step 8: Write Tests](#step-8-write-tests)
- [Step 9: Document Your Changes](#step-9-document-your-changes)
- [Step 10: Deploy and Monitor](#step-10-deploy-and-monitor)
- [Common Migration Patterns](#common-migration-patterns)
- [Rollback Plan](#rollback-plan)
- [Tips for Smooth Migration](#tips-for-smooth-migration)

## Step 1: Plan Permission Rules

Before implementing, document your permission requirements:

### Questions to Answer

1. **Who should access what documents?**
   - All users in the same company?
   - Only owners?
   - Department members?
   - Role-based access?

2. **Are there different levels of access?**
   - Read vs write
   - View some fields but not others (permission levels)
   - Submit/cancel permissions

3. **Should access be based on role, user, or document fields?**
   - Role-based (Sales Manager vs Sales User)
   - User-specific (User Permissions)
   - Document fields (company, territory, status)

4. **Are there time-based or status-based restrictions?**
   - Only current fiscal year
   - Only draft documents
   - Only approved documents

### Document Your Requirements

Example documentation:

```markdown
## Sales Order Permissions

### Requirements:
1. Users can only see orders from their company
2. Sales Users see only their territory
3. Sales Managers see their entire region
4. Sales Directors see everything
5. Users can edit only draft orders
6. Only managers can approve orders
```

## Step 2: Choose Appropriate Hooks

Based on your requirements, select the right hooks:

| Requirement | Hook to Use |
|------------|-------------|
| Filter list views | `permission_query_conditions` |
| Complex document-specific logic | `has_permission` |
| Validate writes before commit | `write_permission_query_conditions` |
| Portal/website access | `has_website_permission` |
| Quick prototyping | Server Script (Permission Query) |
| Filter workflow transitions | `filter_workflow_transitions` |
| Control workflow action permissions | `has_workflow_action_permission` |

### Decision Tree

```
Need to filter list views?
├─ Yes → Use permission_query_conditions
└─ No
   │
   Need document-specific logic?
   ├─ Yes → Use has_permission
   └─ No
      │
      Need to validate writes?
      ├─ Yes → Use write_permission_query_conditions
      └─ No
         │
         Need workflow-specific logic?
         ├─ Yes (transition filtering) → Use filter_workflow_transitions
         ├─ Yes (action permissions) → Use has_workflow_action_permission
         └─ No → Use role permissions only
```

## Step 3: Implement Permission Hooks

### Example: Company-Based Filtering

**Requirement**: Users can only see documents from their company

#### Step 3.1: Create the Hook Function

Create or edit `your_doctype.py`:

```python
# your_app/your_module/doctype/your_doctype/your_doctype.py

def get_permission_query_conditions(user=None):
    """Filter documents by user's company."""
    if not user:
        user = frappe.session.user
    
    # Administrator sees everything
    if user == "Administrator":
        return ""
    
    # Get user's company
    user_company = frappe.db.get_value("User", user, "company")
    
    if not user_company:
        # No company assigned, show nothing
        return "1=0"
    
    # Return SQL condition
    return f"`tabYour DocType`.`company` = {frappe.db.escape(user_company)}"
```

#### Step 3.2: Register the Hook

Edit `hooks.py`:

```python
# your_app/hooks.py

permission_query_conditions = {
    "Your DocType": "your_app.your_module.doctype.your_doctype.your_doctype.get_permission_query_conditions"
}
```

#### Step 3.3: Clear Cache

```bash
bench --site your-site clear-cache
bench restart
```

## Step 4: Test Your Implementation

### Test 1: Test as Administrator

```python
# In bench console
import frappe

frappe.set_user("Administrator")
docs = frappe.get_all("Your DocType")
print(f"Admin sees {len(docs)} documents")
```

### Test 2: Test as Regular User

```python
# Create test user
user = frappe.get_doc({
    "doctype": "User",
    "email": "test@company-a.com",
    "first_name": "Test",
    "company": "Company A"
})
user.insert()
user.add_roles("Sales User")

# Test as this user
frappe.set_user("test@company-a.com")
docs = frappe.get_all("Your DocType")
print(f"User sees {len(docs)} documents")

# Verify only Company A documents
for doc in docs:
    full_doc = frappe.get_doc("Your DocType", doc.name)
    print(f"Document company: {full_doc.company}")
```

### Test 3: Test Different Scenarios

```python
# Test with no company assigned
frappe.db.set_value("User", "test@company-a.com", "company", None)
frappe.clear_cache()
frappe.set_user("test@company-a.com")
docs = frappe.get_all("Your DocType")
assert len(docs) == 0, "User with no company should see no documents"

# Test direct document access
doc = frappe.get_doc("Your DocType", "DOC-001")
can_read = frappe.has_permission("Your DocType", "read", doc)
print(f"Can read DOC-001: {can_read}")
```

## Step 5: Add More Complex Logic (If Needed)

### Example: Adding Role-Based Exceptions

```python
def get_permission_query_conditions(user=None):
    """Filter documents by company, but managers see all."""
    if not user:
        user = frappe.session.user
    
    if user == "Administrator":
        return ""
    
    roles = frappe.get_roles(user)
    
    # Managers see everything
    if "Sales Manager" in roles:
        return ""
    
    # Regular users see only their company
    user_company = frappe.db.get_value("User", user, "company")
    if not user_company:
        return "1=0"
    
    return f"`tabYour DocType`.`company` = {frappe.db.escape(user_company)}"
```

### Example: Adding Document-Specific Logic

```python
def has_permission(doc, ptype=None, user=None, debug=False):
    """Allow edit only for draft documents."""
    if not user:
        user = frappe.session.user
    
    # Check if trying to edit
    if ptype in ("write", "delete"):
        # Only drafts can be edited
        if doc.status != "Draft":
            # Only admins can edit non-drafts
            return user == "Administrator"
    
    return None  # Defer to other permission checks
```

## Step 6: Update Role Permissions

Configure role permissions via UI:

1. Go to Role Permission Manager
2. Select your DocType
3. For each role, set appropriate permissions:
   - Read, Write, Create, Delete
   - Submit, Cancel (if submittable)
   - Permission Levels (if using field-level access)

### Example Configuration

| Role | Level | Read | Write | Create | Delete | Submit |
|------|-------|------|-------|--------|--------|--------|
| Sales User | 0 | ✓ | ✓ | ✓ | ✗ | ✗ |
| Sales Manager | 0 | ✓ | ✓ | ✓ | ✓ | ✓ |
| Sales Manager | 1 | ✓ | ✓ | - | - | - |

## Step 7: Setup User Permissions (If Needed)

If using User Permissions for document-level restrictions:

```python
# Add user permissions programmatically
from frappe.permissions import add_user_permission

# Restrict user to Company A
add_user_permission(
    doctype="Company",
    name="Company A",
    user="user@example.com",
    applicable_for="Your DocType"
)

# Or via UI:
# 1. Go to User Permission List
# 2. Click New
# 3. Select User, DocType (Allow), and Document (For Value)
# 4. Save
```

## Step 8: Write Tests

Create comprehensive tests:

```python
# In test_your_doctype.py

def test_company_filtering(self):
    """Test users only see documents from their company."""
    # Create documents in different companies
    doc_a = create_test_document("Your DocType", company="Company A")
    doc_b = create_test_document("Your DocType", company="Company B")
    
    # Create user for Company A
    user = create_test_user("user@company-a.com", ["Sales User"])
    frappe.db.set_value("User", user, "company", "Company A")
    
    # Test list view
    frappe.set_user(user)
    docs = frappe.get_all("Your DocType", fields=["name", "company"])
    
    # Should only see Company A documents
    self.assertEqual(len(docs), 1)
    self.assertEqual(docs[0].name, doc_a.name)
    
    # Test direct access
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc_a))
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc_b))
```

## Step 9: Document Your Changes

### Code Comments

```python
def get_permission_query_conditions(user=None):
    """
    Filter documents by user's company.
    
    Rules:
    - Administrators see all documents
    - Sales Managers see all documents in all companies
    - Regular users see only documents from their company
    - Users without a company see no documents
    
    Args:
        user: User to check permissions for
        
    Returns:
        str: SQL WHERE condition
    """
    # Implementation...
```

### User Documentation

Create documentation for end users:

```markdown
## Sales Order Permissions

### Access Rules

1. **Company Filtering**: You can only see Sales Orders from your company
2. **Territory Access**: Sales Users see only their territory
3. **Edit Restrictions**: Only draft orders can be edited

### For Administrators

- Admins can see and edit all Sales Orders
- To grant access to another company, add User Permission

### Troubleshooting

If you can't see expected documents:
1. Check your company is set in User settings
2. Check you have Sales User role
3. Contact your administrator to verify User Permissions
```

## Step 10: Deploy and Monitor

### Deployment Checklist

- [ ] Code changes committed to version control
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Hooks registered in hooks.py
- [ ] Role permissions configured
- [ ] User permissions set up (if needed)
- [ ] Tested in development environment
- [ ] Tested with different roles and users
- [ ] Performance tested with large datasets

### Post-Deployment Monitoring

```python
# Monitor permission errors
# In hooks.py
doc_events = {
    "*": {
        "on_update": "your_app.utils.log_permission_usage"
    }
}

# In your_app/utils.py
def log_permission_usage(doc, method):
    """Log permission checks for monitoring."""
    if frappe.session.user != "Administrator":
        frappe.log_error(
            f"User {frappe.session.user} updated {doc.doctype} {doc.name}",
            "Permission Usage"
        )
```

## Common Migration Patterns

### Pattern 1: Adding Permissions to Existing DocType

1. Analyze current access patterns
2. Implement permission_query_conditions
3. Test with existing data
4. Roll out to staging
5. Monitor and adjust

### Pattern 2: Migrating from No Restrictions to Restricted

1. Communicate changes to users
2. Implement permissions in test environment
3. Set up User Permissions for all users
4. Verify everyone can access their documents
5. Deploy to production
6. Monitor for issues

### Pattern 3: Tightening Existing Permissions

1. Document current permission logic
2. Identify gaps or issues
3. Implement stricter rules
4. Test thoroughly
5. Communicate changes
6. Deploy with monitoring

## Rollback Plan

If permissions cause issues:

### Immediate Rollback

```python
# In hooks.py - comment out the hook
# permission_query_conditions = {
#     "Your DocType": "your_app.your_module.doctype.your_doctype.your_doctype.get_permission_query_conditions"
# }

# Clear cache and restart
```

```bash
bench --site your-site clear-cache
bench restart
```

### Temporary Fix

```python
# Return empty condition to disable filtering
def get_permission_query_conditions(user=None):
    return ""  # Temporarily disable filtering
```

## Tips for Smooth Migration

1. **Start with read permissions**: Get filtering right before restricting writes
2. **Test with real users**: Use actual user accounts, not just test accounts
3. **Communicate early**: Let users know about upcoming changes
4. **Monitor closely**: Watch for permission errors in the first days
5. **Have a rollback plan**: Be ready to revert if needed
6. **Document everything**: Code comments, user docs, and technical docs
7. **Train power users**: Help key users understand new permissions
8. **Iterate gradually**: Start with basic rules, add complexity later
