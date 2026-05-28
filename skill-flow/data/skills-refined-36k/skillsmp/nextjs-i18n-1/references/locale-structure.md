# Locale Structure for LucidData

Translation file organization and JSON schema patterns.

## Namespace Organization

```json
{
  "common": {},      // Shared across all pages
  "nav": {},         // Navigation menu
  "auth": {},        // Login, signup, logout
  "vault": {},       // Vault feature
  "consent": {},     // Consent management
  "audit": {},       // Audit log
  "errors": {},      // Error messages
  "validation": {}   // Form validation
}
```

## Naming Conventions

- **Namespaces**: camelCase (`common`, `vault`, `consentManagement`)
- **Keys**: camelCase (`save`, `deleteEntry`, `grantedTo`)
- **Nested objects**: Represent hierarchy (`actions.save`, `labels.email`)
- **Plurals**: Use ICU format (`items`, not `item` and `items`)

## Variable Interpolation

```json
{
  "welcome": "Welcome, {name}!",
  "itemCount": "You have {count} {count, plural, one {item} other {items}}"
}
```

**Usage**:
```tsx
t('welcome', { name: 'John' }) // "Welcome, John!"
t('itemCount', { count: 1 })   // "You have 1 item"
t('itemCount', { count: 5 })   // "You have 5 items"
```

## Pluralization (ICU MessageFormat)

```json
{
  "items": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

**Spanish**:
```json
{
  "items": "{count, plural, =0 {Ningún elemento} one {# elemento} other {# elementos}}"
}
```

## Date/Time Formatting

Don't include dates in JSON; use `useFormatter`:

```tsx
const format = useFormatter();

// In translation
"createdAt": "Created on {date}"

// In component
t('createdAt', { date: format.dateTime(entry.createdAt) })
```

## Complete Structure Template

```json
{
  "common": {
    "appName": "Lucid",
    "tagline": "Your Personal Data Bank",
    "loading": "Loading...",
    "error": "An error occurred",
    "success": "Success",
    "actions": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete",
      "edit": "Edit",
      "create": "Create",
      "view": "View",
      "close": "Close",
      "back": "Back",
      "next": "Next",
      "submit": "Submit",
      "confirm": "Confirm"
    }
  },
  "nav": {
    "dashboard": "Dashboard",
    "vault": "Vault",
    "consent": "Consent",
    "audit": "Audit Log",
    "settings": "Settings",
    "help": "Help",
    "signOut": "Sign Out"
  },
  "auth": {
    "login": {
      "title": "Sign In",
      "subtitle": "Access your personal data bank",
      "email": "Email",
      "password": "Password",
      "submit": "Sign In",
      "noAccount": "Don't have an account?",
      "signUpLink": "Sign up"
    },
    "signup": {
      "title": "Create Account",
      "subtitle": "Start securing your data",
      "submit": "Create Account",
      "hasAccount": "Already have an account?",
      "loginLink": "Sign in"
    },
    "errors": {
      "invalidCredentials": "Invalid email or password",
      "emailTaken": "Email already in use",
      "weakPassword": "Password must be at least 8 characters"
    }
  },
  "vault": {
    "title": "Data Vault",
    "description": "Securely store your personal information",
    "empty": "No entries yet. Create your first one!",
    "create": "Create Entry",
    "edit": "Edit Entry",
    "view": "View Entry",
    "delete": "Delete Entry",
    "confirmDelete": "Are you sure you want to delete this entry?",
    "labels": {
      "label": "Label",
      "category": "Category",
      "metadata": "Metadata (JSON)",
      "createdAt": "Created",
      "updatedAt": "Updated"
    },
    "categories": {
      "identity": "Identity",
      "financial": "Financial",
      "health": "Health",
      "contact": "Contact",
      "employment": "Employment",
      "education": "Education"
    },
    "placeholders": {
      "label": "e.g., Passport",
      "metadata": "Enter JSON data"
    },
    "validation": {
      "labelRequired": "Label is required",
      "categoryRequired": "Category is required",
      "invalidJson": "Invalid JSON format"
    }
  },
  "consent": {
    "title": "Consent Management",
    "description": "Control who accesses your data",
    "empty": "No consents granted yet",
    "grant": "Grant Consent",
    "revoke": "Revoke Consent",
    "extend": "Extend Consent",
    "view": "View Consent",
    "confirmRevoke": "Are you sure you want to revoke this consent?",
    "labels": {
      "grantedTo": "Granted To",
      "purpose": "Purpose",
      "accessLevel": "Access Level",
      "startDate": "Start Date",
      "endDate": "End Date",
      "status": "Status",
      "dataLabel": "Data Entry"
    },
    "accessLevels": {
      "READ": "Read Only",
      "EXPORT": "Export",
      "VERIFY": "Verify"
    },
    "status": {
      "active": "Active",
      "expired": "Expired",
      "revoked": "Revoked"
    },
    "legal": {
      "agreement": "I consent to share this data for the stated purpose and duration.",
      "withdrawal": "I understand I can withdraw consent at any time.",
      "gdprNotice": "You have the right to withdraw consent at any time without affecting the lawfulness of processing based on consent before its withdrawal.",
      "dataProcessing": "Your data will be processed according to our privacy policy and applicable data protection laws."
    },
    "validation": {
      "grantedToRequired": "Recipient is required",
      "purposeRequired": "Purpose is required",
      "endDateFuture": "End date must be in the future",
      "endDateAfterStart": "End date must be after start date"
    }
  },
  "audit": {
    "title": "Audit Log",
    "description": "Track all data access and changes",
    "empty": "No audit events yet",
    "labels": {
      "eventType": "Event Type",
      "timestamp": "Timestamp",
      "actor": "Actor",
      "entity": "Entity",
      "details": "Details"
    },
    "events": {
      "DATA_CREATED": "Data Created",
      "DATA_UPDATED": "Data Updated",
      "DATA_DELETED": "Data Deleted",
      "DATA_ACCESSED": "Data Accessed",
      "DATA_EXPORTED": "Data Exported",
      "CONSENT_GRANTED": "Consent Granted",
      "CONSENT_REVOKED": "Consent Revoked",
      "CONSENT_EXPIRED": "Consent Expired",
      "USER_LOGIN": "User Login",
      "USER_LOGOUT": "User Logout"
    },
    "actors": {
      "user": "User",
      "system": "System",
      "buyer": "Data Buyer"
    }
  },
  "errors": {
    "generic": "An error occurred. Please try again.",
    "network": "Network error. Check your connection.",
    "unauthorized": "You are not authorized to perform this action.",
    "notFound": "The requested resource was not found.",
    "validationFailed": "Please check your input and try again.",
    "serverError": "Server error. Please try again later."
  },
  "validation": {
    "required": "This field is required",
    "email": "Please enter a valid email address",
    "minLength": "Must be at least {min} characters",
    "maxLength": "Must be at most {max} characters",
    "passwordMatch": "Passwords must match"
  }
}
```

## Best Practices

1. **Keep keys consistent across locales**: All locales should have same structure
2. **Avoid hardcoded text in components**: Always use translation keys
3. **Use descriptive keys**: `vault.labels.createdAt` not `vault.label1`
4. **Group related translations**: Use namespaces (`vault`, `consent`)
5. **Don't translate technical terms**: API keys, error codes stay in English
6. **Use ICU format for plurals**: Better than separate keys
7. **Extract common patterns**: Reuse `common.actions.*` across features

## Validation

```bash
# Check all locales have same keys (future script)
node scripts/validate-translations.js

# Expected output:
# ✓ All locales have matching keys
# ✓ No missing translations
# ✓ Valid JSON format
```

---

**For more information:**
- [next-intl Setup](next-intl-setup.md)
- [ICU MessageFormat](https://formatjs.io/docs/core-concepts/icu-syntax/)
