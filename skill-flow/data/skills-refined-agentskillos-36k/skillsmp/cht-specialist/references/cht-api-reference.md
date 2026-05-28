# CHT API Reference (3.12.0+)

The `cht` object is available in `tasks.js`, `targets.js`, and `contact-summary.templated.js`. It provides access to CHT platform APIs.

## Availability

| File | `cht` available | Version |
|------|-----------------|---------|
| tasks.js | Yes | 3.12.0+ |
| targets.js | Yes | 3.12.0+ |
| contact-summary.templated.js | Yes | 3.12.0+ |
| XForms (via xpath) | No | - |

## API Reference

### cht.v1.hasPermissions(permissions)

Check if the current user has specific permission(s). Returns boolean.

**Parameters:**
- `permissions` - String or array of strings

**Returns:** `true` if user has ALL specified permissions

```javascript
// Single permission
const canEdit = cht.v1.hasPermissions('can_edit');

// Multiple permissions (ALL must be present)
const canManagePlaces = cht.v1.hasPermissions([
  'can_create_places',
  'can_update_places'
]);

// Use in task appliesIf
appliesIf: function(contact) {
  return cht.v1.hasPermissions('can_view_tasks');
}
```

### cht.v1.hasAnyPermission(permissionGroups)

Check if user has ANY of the specified permission groups. Each group is an array of permissions that must ALL be present.

**Parameters:**
- `permissionGroups` - Array of permission arrays

**Returns:** `true` if user has ALL permissions in at least ONE group

```javascript
// User needs EITHER (view_messages AND view_message_action)
// OR (view_reports AND verify_reports)
const hasAccess = cht.v1.hasAnyPermission([
  ['can_view_messages', 'can_view_message_action'],
  ['can_view_reports', 'can_verify_reports']
]);
```

### cht.v1.getExtensionLib(filename)

Load and execute a custom JavaScript extension library. Returns the exported function.

**Parameters:**
- `filename` - Name of the extension library file (from app_settings)

**Returns:** The function exported by the extension library

```javascript
// Load extension and call with parameters
const myLibrary = cht.v1.getExtensionLib('mylib.js');
const result = myLibrary(param1, param2);

// One-liner
const calculated = cht.v1.getExtensionLib('calculations.js')(contact, reports);
```

**Setting up extension libraries:**

1. Create the library file (e.g., `extension-libs/mylib.js`):
```javascript
module.exports = function(param1, param2) {
  // Your logic here
  return result;
};
```

2. Register in `app_settings.json`:
```json
{
  "extension_libs": {
    "mylib.js": "extension-libs/mylib.js"
  }
}
```

### cht.v1.analytics.getTargetDocs() (4.11.0+)

Get the current user's target documents for analytics calculations.

**Returns:** Array of target documents

```javascript
const targetDocs = cht.v1.analytics.getTargetDocs();

// Find specific target
const birthsTarget = targetDocs.find(t => t.id === 'births-this-month');
if (birthsTarget) {
  const currentCount = birthsTarget.value.total;
}
```

## Common Patterns

### Permission-based task visibility

```javascript
// tasks.js
{
  name: 'supervisor-review',
  appliesTo: 'reports',
  appliesToType: ['assessment'],
  appliesIf: function(contact, report) {
    // Only show to supervisors
    return cht.v1.hasPermissions('can_view_all_reports');
  },
  // ...
}
```

### Role-based target filtering

```javascript
// targets.js
{
  id: 'chw-visits',
  appliesTo: 'reports',
  appliesToType: ['home_visit'],
  appliesIf: function(contact, report) {
    // Only count for CHWs, not supervisors
    return !cht.v1.hasPermissions('can_view_all_reports');
  },
  // ...
}
```

### Shared logic via extension libraries

```javascript
// extension-libs/risk-assessment.js
module.exports = function(contact, reports) {
  const pregnancyReport = reports.find(r => r.form === 'pregnancy');
  if (!pregnancyReport) return { isHighRisk: false, factors: [] };

  const factors = [];
  if (pregnancyReport.fields.age < 18) factors.push('young_mother');
  if (pregnancyReport.fields.previous_complications) factors.push('history');

  return {
    isHighRisk: factors.length > 0,
    factors: factors
  };
};

// Usage in tasks.js or targets.js
const riskInfo = cht.v1.getExtensionLib('risk-assessment.js')(contact, contact.reports);
if (riskInfo.isHighRisk) {
  // High risk logic
}
```

### Context in contact summary

```javascript
// contact-summary.templated.js
module.exports = {
  context: {
    isSupervisor: cht.v1.hasPermissions('can_view_all_reports'),
    canEdit: cht.v1.hasPermissions('can_edit')
  },
  fields: [
    {
      label: 'admin.internal_id',
      value: contact._id,
      appliesIf: function() {
        // Only show to supervisors
        return cht.v1.hasPermissions('can_view_all_reports');
      }
    }
  ]
};
```

## Version Requirements

| Feature | Minimum Version |
|---------|-----------------|
| `cht.v1.hasPermissions` | 3.12.0 |
| `cht.v1.hasAnyPermission` | 3.12.0 |
| `cht.v1.getExtensionLib` | 3.12.0 |
| `cht.v1.analytics.getTargetDocs` | 4.11.0 |
