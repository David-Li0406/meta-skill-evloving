# Testing and Debugging

## Run Tests

### Run All Tests for App
```bash
bench --site development.localhost run-tests --app soldamundo
bench --site development.localhost run-tests --app tweaks
```

Runs the complete test suite for the specified app.

### Run Specific Test File
```bash
bench --site development.localhost run-tests \
    --module soldamundo.soldamundo.doctype.doctype_name.test_doctype_name
```

**Module path format:** `app_name.module_path.test_file_name` (without .py)

### Run Specific Test Class or Method
```bash
# Run specific test class
bench --site development.localhost run-tests \
    --module soldamundo.soldamundo.doctype.item.test_item \
    --test-case TestItem

# Run specific test method
bench --site development.localhost run-tests \
    --module soldamundo.soldamundo.doctype.item.test_item \
    --test-case TestItem.test_item_creation
```

### Run Tests with Coverage
```bash
bench --site development.localhost run-tests --app soldamundo --coverage
```

Generates code coverage report showing which lines are tested.

**Coverage output:** `coverage.xml` and HTML report in `htmlcov/`

### Run Tests Verbosely
```bash
bench --site development.localhost run-tests --app soldamundo --verbose
```

Shows detailed test output for debugging.

## Python Console

### Open Interactive Console
```bash
bench --site development.localhost console
```

Opens IPython console with full Frappe context loaded.

### Common Console Commands

#### Document Operations
```python
# Get a document
doc = frappe.get_doc("Item", "ITEM-001")
print(doc.as_dict())

# Create a document
new_doc = frappe.get_doc({
    "doctype": "Item",
    "item_code": "TEST-001",
    "item_name": "Test Item"
})
new_doc.insert()
frappe.db.commit()

# Update a document
doc = frappe.get_doc("Item", "ITEM-001")
doc.item_name = "Updated Name"
doc.save()
frappe.db.commit()

# Delete a document
frappe.delete_doc("Item", "ITEM-001")
frappe.db.commit()
```

#### Database Queries
```python
# Run SQL query
results = frappe.db.sql("""
    SELECT name, item_name, item_code
    FROM `tabItem`
    WHERE disabled = 0
    LIMIT 5
""", as_dict=True)

for row in results:
    print(row.name, row.item_name)

# Get single value
count = frappe.db.sql("SELECT COUNT(*) FROM `tabItem`")[0][0]

# Get list
items = frappe.get_list("Item",
    filters={"disabled": 0},
    fields=["name", "item_name", "item_code"],
    limit=10
)
```

#### Context Information
```python
# Current site
print(frappe.local.site)

# Current user
print(frappe.session.user)

# Installed apps
print(frappe.get_installed_apps())

# Site path
print(frappe.get_site_path())
```

#### Debugging Helpers
```python
# Enable query debugging
frappe.db.debug = 1

# Disable query debugging
frappe.db.debug = 0

# Print last query
print(frappe.db.last_query)

# Reload module
import importlib
import soldamundo.utils.some_module
importlib.reload(soldamundo.utils.some_module)
```

#### Commit and Rollback
```python
# Commit changes
frappe.db.commit()

# Rollback changes
frappe.db.rollback()

# Auto-rollback (for testing)
frappe.db.begin()
# ... make changes ...
frappe.db.rollback()  # Undo everything
```

## Execute Python Code

### Execute Single Command
```bash
bench --site development.localhost execute "frappe.db.commit()"
```

Runs Python code without opening console.

### Execute Script
```bash
bench --site development.localhost execute "app_name.path.to.script.function"
```

**Use cases:**
- Run migrations manually
- Execute maintenance scripts
- Trigger background jobs
- Data cleanup

## Test Development Workflow

### 1. Write Tests
```python
# soldamundo/soldamundo/doctype/my_doctype/test_my_doctype.py
import frappe
from frappe.tests.utils import FrappeTestCase

class TestMyDoctype(FrappeTestCase):
    def test_creation(self):
        doc = frappe.get_doc({
            "doctype": "My Doctype",
            "field1": "value1"
        })
        doc.insert()
        self.assertEqual(doc.field1, "value1")
```

### 2. Run Tests
```bash
bench --site development.localhost run-tests \
    --module soldamundo.soldamundo.doctype.my_doctype.test_my_doctype
```

### 3. Debug Failures
```bash
# Run with verbose output
bench --site development.localhost run-tests \
    --module soldamundo.soldamundo.doctype.my_doctype.test_my_doctype \
    --verbose

# Or use console to test interactively
bench --site development.localhost console
>>> from soldamundo.soldamundo.doctype.my_doctype.test_my_doctype import TestMyDoctype
>>> test = TestMyDoctype()
>>> test.test_creation()
```

## Debugging Tips

### Print Debugging
```python
# In code
print("Debug:", value)
frappe.log_error("Error message", "Error Title")

# In console
import json
print(json.dumps(doc.as_dict(), indent=2))
```

### Query Debugging
```python
# Enable in console or code
frappe.db.debug = 1

# All queries will be printed
doc = frappe.get_doc("Item", "ITEM-001")

# Disable
frappe.db.debug = 0
```

### Profiling
```python
# In console
import cProfile
cProfile.run('frappe.get_list("Item", limit=100)')
```

## Testing Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Use Fixtures**: Create reusable test data
3. **Clean Up**: Delete test records after tests
4. **Test Edge Cases**: Not just happy paths
5. **Mock External Calls**: Don't hit real APIs in tests
6. **Run Regularly**: Run tests before committing code

## Common Testing Patterns

### Setup and Teardown
```python
class TestMyDoctype(FrappeTestCase):
    def setUp(self):
        # Run before each test
        self.test_doc = frappe.get_doc({
            "doctype": "My Doctype",
            "field1": "test"
        }).insert()

    def tearDown(self):
        # Run after each test
        frappe.delete_doc("My Doctype", self.test_doc.name)

    def test_something(self):
        self.assertIsNotNone(self.test_doc.name)
```

### Testing Permissions
```python
frappe.set_user("test@example.com")
# ... test operations as user ...
frappe.set_user("Administrator")
```

### Testing Validation
```python
with self.assertRaises(frappe.ValidationError):
    doc = frappe.get_doc({
        "doctype": "My Doctype",
        "invalid_field": "value"
    })
    doc.insert()
```
