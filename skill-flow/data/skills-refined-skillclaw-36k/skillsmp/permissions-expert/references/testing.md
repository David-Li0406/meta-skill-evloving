# Testing Permission Hooks

## Table of Contents

- [Unit Tests for Permissions](#unit-tests-for-permissions)
  - [Basic Test Structure](#basic-test-structure)
  - [Test 1: User Can Access Own Company Documents](#test-1-user-can-access-own-company-documents)
  - [Test 2: User Cannot Access Other Company Documents](#test-2-user-cannot-access-other-company-documents)
  - [Test 3: Permission Query Conditions Filter List Views](#test-3-permission-query-conditions-filter-list-views)
  - [Test 4: Write Permissions](#test-4-write-permissions)
  - [Test 5: Share Permissions](#test-5-share-permissions)
  - [Test 6: Role-Based Permissions](#test-6-role-based-permissions)
  - [Test 7: Controller Permission Hook](#test-7-controller-permission-hook)
  - [Test 8: Permission Levels](#test-8-permission-levels)
- [Test Utilities](#test-utilities)
- [Integration Tests](#integration-tests)
- [Performance Tests](#performance-tests)
- [Best Practices for Testing](#best-practices-for-testing)
- [Running Tests](#running-tests)

## Unit Tests for Permissions

### Basic Test Structure

```python
# In test_your_doctype.py
from frappe.tests.utils import FrappeTestCase
from frappe.permissions import add_user_permission, clear_user_permissions_for_doctype

class TestYourDocTypePermissions(FrappeTestCase):
    def setUp(self):
        # Create test users and assign roles
        self.test_user = "test@example.com"
        if not frappe.db.exists("User", self.test_user):
            user = frappe.get_doc({
                "doctype": "User",
                "email": self.test_user,
                "first_name": "Test"
            })
            user.add_roles("Sales User")
            user.insert(ignore_permissions=True)
    
    def tearDown(self):
        # Clean up user permissions
        clear_user_permissions_for_doctype("Company", self.test_user)
```

### Test 1: User Can Access Own Company Documents

```python
def test_user_can_access_own_company_documents(self):
    """Test user can access documents from their company."""
    # Add user permission for Company A
    add_user_permission("Company", "Company A", self.test_user)
    
    # Create test document
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "company": "Company A",
        "title": "Test Doc"
    })
    doc.insert(ignore_permissions=True)
    
    # Check permission
    frappe.set_user(self.test_user)
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc))
    frappe.set_user("Administrator")
```

### Test 2: User Cannot Access Other Company Documents

```python
def test_user_cannot_access_other_company_documents(self):
    """Test user cannot access documents from other companies."""
    add_user_permission("Company", "Company A", self.test_user)
    
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "company": "Company B",  # Different company
        "title": "Test Doc"
    })
    doc.insert(ignore_permissions=True)
    
    frappe.set_user(self.test_user)
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc))
    frappe.set_user("Administrator")
```

### Test 3: Permission Query Conditions Filter List Views

```python
def test_permission_query_conditions(self):
    """Test permission query conditions filter list views."""
    add_user_permission("Company", "Company A", self.test_user)
    
    # Create documents in different companies
    for company in ["Company A", "Company B"]:
        frappe.get_doc({
            "doctype": "Your DocType",
            "company": company,
            "title": f"Doc in {company}"
        }).insert(ignore_permissions=True)
    
    # Check filtered list
    frappe.set_user(self.test_user)
    docs = frappe.get_all("Your DocType", fields=["company"])
    self.assertEqual(len(docs), 1)
    self.assertEqual(docs[0].company, "Company A")
    frappe.set_user("Administrator")
```

### Test 4: Write Permissions

```python
def test_user_can_write_own_documents(self):
    """Test user can write to documents they own."""
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "title": "Test Doc",
        "owner": self.test_user
    })
    doc.insert(ignore_permissions=True)
    
    frappe.set_user(self.test_user)
    self.assertTrue(frappe.has_permission("Your DocType", "write", doc))
    
    # Test actual write
    doc.title = "Updated Title"
    doc.save()  # Should not raise exception
    
    frappe.set_user("Administrator")
```

### Test 5: Share Permissions

```python
def test_share_permissions(self):
    """Test share permissions grant access."""
    # Create document as admin
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "title": "Shared Doc"
    })
    doc.insert()
    
    # User initially has no access
    frappe.set_user(self.test_user)
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc))
    
    # Share with user
    frappe.set_user("Administrator")
    frappe.share.add(
        doctype="Your DocType",
        name=doc.name,
        user=self.test_user,
        read=1,
        write=0
    )
    
    # User now has access
    frappe.set_user(self.test_user)
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc))
    self.assertFalse(frappe.has_permission("Your DocType", "write", doc))
    
    frappe.set_user("Administrator")
```

### Test 6: Role-Based Permissions

```python
def test_role_permissions(self):
    """Test different roles have different permissions."""
    # Create document
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "title": "Test Doc"
    })
    doc.insert(ignore_permissions=True)
    
    # Test as Sales User (read only)
    sales_user = create_test_user("sales@example.com", ["Sales User"])
    frappe.set_user(sales_user)
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc))
    self.assertFalse(frappe.has_permission("Your DocType", "write", doc))
    
    # Test as Sales Manager (read and write)
    manager = create_test_user("manager@example.com", ["Sales Manager"])
    frappe.set_user(manager)
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc))
    self.assertTrue(frappe.has_permission("Your DocType", "write", doc))
    
    frappe.set_user("Administrator")
```

### Test 7: Controller Permission Hook

```python
def test_controller_permission_hook(self):
    """Test custom has_permission hook."""
    # Create document owned by another user
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "title": "Test Doc",
        "owner": "other@example.com"
    })
    doc.insert(ignore_permissions=True)
    
    # Test user cannot access (owner-only permission)
    frappe.set_user(self.test_user)
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc))
    
    # Owner can access
    frappe.set_user("other@example.com")
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc))
    
    frappe.set_user("Administrator")
```

### Test 8: Permission Levels

```python
def test_permission_levels(self):
    """Test permission levels restrict field access."""
    doc = frappe.get_doc({
        "doctype": "Your DocType",
        "title": "Test Doc",
        "discount_percentage": 10  # permlevel 1 field
    })
    doc.insert(ignore_permissions=True)
    
    # User without permlevel 1 access
    frappe.set_user(self.test_user)
    perms = frappe.permissions.get_doc_permissions(doc, user=self.test_user)
    
    meta = frappe.get_meta("Your DocType")
    accessible_permlevels = meta.get_permlevel_access("read", user=self.test_user)
    
    # Should only have access to permlevel 0
    self.assertIn(0, accessible_permlevels)
    self.assertNotIn(1, accessible_permlevels)
    
    frappe.set_user("Administrator")
```

## Test Utilities

### Helper Function: Create Test User

```python
def create_test_user(email, roles):
    """Create a test user with specified roles."""
    if frappe.db.exists("User", email):
        user = frappe.get_doc("User", email)
    else:
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": email.split("@")[0]
        })
        user.insert(ignore_permissions=True)
    
    for role in roles:
        user.add_roles(role)
    
    return email
```

### Helper Function: Create Test Document

```python
def create_test_document(doctype, **kwargs):
    """Create a test document with given fields."""
    doc = frappe.get_doc({
        "doctype": doctype,
        **kwargs
    })
    doc.insert(ignore_permissions=True)
    return doc
```

## Integration Tests

### Test Scenario: Multi-Company Workflow

```python
def test_multi_company_workflow(self):
    """Test complete multi-company permission workflow."""
    # Setup: Create users for different companies
    company_a_user = create_test_user("user.a@example.com", ["Sales User"])
    company_b_user = create_test_user("user.b@example.com", ["Sales User"])
    
    add_user_permission("Company", "Company A", company_a_user)
    add_user_permission("Company", "Company B", company_b_user)
    
    # Create documents in different companies
    doc_a = create_test_document("Your DocType", company="Company A", title="Doc A")
    doc_b = create_test_document("Your DocType", company="Company B", title="Doc B")
    
    # Test Company A user
    frappe.set_user(company_a_user)
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc_a))
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc_b))
    
    docs = frappe.get_all("Your DocType", fields=["name", "company"])
    self.assertEqual(len(docs), 1)
    self.assertEqual(docs[0].company, "Company A")
    
    # Test Company B user
    frappe.set_user(company_b_user)
    self.assertFalse(frappe.has_permission("Your DocType", "read", doc_a))
    self.assertTrue(frappe.has_permission("Your DocType", "read", doc_b))
    
    docs = frappe.get_all("Your DocType", fields=["name", "company"])
    self.assertEqual(len(docs), 1)
    self.assertEqual(docs[0].company, "Company B")
    
    frappe.set_user("Administrator")
```

## Performance Tests

### Test Query Performance

```python
def test_permission_query_performance(self):
    """Test permission query conditions don't cause performance issues."""
    import time
    
    # Create many documents
    for i in range(100):
        create_test_document("Your DocType", title=f"Doc {i}")
    
    # Measure query time
    frappe.set_user(self.test_user)
    start = time.time()
    docs = frappe.get_all("Your DocType", limit=50)
    duration = time.time() - start
    
    # Should complete in reasonable time (adjust threshold as needed)
    self.assertLess(duration, 1.0)  # Less than 1 second
    
    frappe.set_user("Administrator")
```

## Best Practices for Testing

1. **Use setUp and tearDown**: Clean up after tests
2. **Test both positive and negative cases**: Can access AND cannot access
3. **Test list views**: Not just individual document access
4. **Test different roles**: Verify role-based behavior
5. **Test edge cases**: Empty values, None, non-existent users
6. **Use descriptive test names**: Explain what's being tested
7. **Keep tests independent**: Each test should work standalone
8. **Clean up test data**: Remove test users and documents
9. **Test performance**: Ensure permissions don't slow down queries
10. **Document test scenarios**: Add docstrings to tests

## Running Tests

```bash
# Run all tests for a doctype
bench --site your-site run-tests --doctype "Your DocType"

# Run specific test class
bench --site your-site run-tests --test test_your_doctype.TestYourDocTypePermissions

# Run specific test method
bench --site your-site run-tests --test test_your_doctype.TestYourDocTypePermissions.test_user_can_access_own_company_documents

# Run with coverage
bench --site your-site run-tests --doctype "Your DocType" --coverage

# Run in parallel
bench --site your-site run-tests --doctype "Your DocType" --parallel
```
