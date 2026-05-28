# Troubleshooting Patterns for DocuGen

Common issue templates for auto-generated troubleshooting sections.

## Pattern Categories

### 1. Permission/Access Issues

**Template:**
```markdown
**"[Action] button is disabled/grayed out"**
This indicates insufficient permissions for this action. Contact your
organization administrator to request [specific role/permission] access.
```

**Variations:**
- "You don't have permission to..."
- "Access denied"
- "Unauthorized"
- Element not visible at all

**Common Causes:**
- User role doesn't include required permissions
- Feature is disabled for the account tier
- Organization policy restriction

---

### 2. Not Found Errors

**Template:**
```markdown
**"[Resource] not found" or blank page**
Verify the URL is correct and you have access to this [resource type].
The [resource] may have been deleted, moved, or you may need to be
added as a collaborator.
```

**Variations:**
- 404 error pages
- "This page doesn't exist"
- Empty search results
- Missing menu items

**Common Causes:**
- Typo in URL or resource name
- Resource was deleted or archived
- User not added to project/team

---

### 3. Validation Errors

**Template:**
```markdown
**"[Field] is invalid" or red error message**
Check that your input matches the required format: [format description].
[Specific constraint, e.g., "Project names can only contain letters,
numbers, and hyphens."]
```

**Variations:**
- "Invalid format"
- "This field is required"
- "Value must be between X and Y"
- Field highlighted in red

**Common Causes:**
- Special characters not allowed
- Length constraints (min/max)
- Required field left empty
- Duplicate value (already exists)

---

### 4. Naming Conflicts

**Template:**
```markdown
**"[Name] already exists" error**
[Resource] names must be unique within [scope]. Try adding a date suffix
(e.g., "project-name-2024") or department prefix to differentiate.
```

**Variations:**
- "Duplicate entry"
- "This name is taken"
- "Already in use"

**Common Causes:**
- Previous attempt created partial resource
- Someone else used the same name
- Name conflicts with system reserved words

---

### 5. Loading/Timeout Issues

**Template:**
```markdown
**Page loads slowly or times out**
This may be due to temporary server issues or network problems. Try:
1. Refresh the page
2. Clear your browser cache
3. Try again in a few minutes

If the problem persists, check [service status page] for outages.
```

**Variations:**
- Spinning loader that never completes
- "Request timed out"
- Partial page loads
- "Service unavailable"

**Common Causes:**
- High server load
- Large data set being processed
- Network connectivity issues
- Browser cache conflicts

---

### 6. Browser Compatibility

**Template:**
```markdown
**Features not working or display incorrectly**
[Application] works best with modern browsers. Ensure you're using the
latest version of Chrome, Firefox, Safari, or Edge. Try clearing your
browser cache and disabling extensions that might interfere.
```

**Variations:**
- Buttons don't respond to clicks
- Layout appears broken
- JavaScript errors in console
- Missing UI elements

**Common Causes:**
- Outdated browser version
- Browser extension conflicts
- Cached outdated assets
- Unsupported browser

---

### 7. Session/Authentication Issues

**Template:**
```markdown
**Unexpectedly logged out or "Session expired"**
Your session may have timed out due to inactivity. Log in again to continue.
If this happens frequently, check that your browser accepts cookies from
[application domain].
```

**Variations:**
- Redirected to login page
- "Please log in to continue"
- Actions fail silently
- "Token expired"

**Common Causes:**
- Inactivity timeout
- Browser blocking cookies
- Multiple tabs with different sessions
- Account accessed from another location

---

### 8. File Upload Issues

**Template:**
```markdown
**File upload fails or "Invalid file type"**
Check that your file meets the requirements:
- Maximum size: [size limit]
- Supported formats: [formats]
- File name should not contain special characters

Try compressing large files or converting to a supported format.
```

**Variations:**
- "File too large"
- Upload progress stuck
- "Unsupported file type"
- Upload completes but file missing

**Common Causes:**
- File exceeds size limit
- Wrong file format
- Network interruption during upload
- File name contains unsupported characters

---

## Workflow-Specific Patterns

### Form Submission
```markdown
**Form submission fails without error message**
1. Check all required fields are completed (marked with *)
2. Verify any email or phone fields are in correct format
3. Scroll up to check for error messages at the top of the form
4. Try submitting in a different browser
```

### Data Not Saving
```markdown
**Changes not saving or reverting**
1. Look for a "Save" button that needs to be clicked
2. Wait for any "Saving..." indicator to complete
3. Check if you have edit permissions for this content
4. Refresh the page and verify if changes persisted
```

### Search Not Finding Results
```markdown
**Search returns no results when data exists**
1. Check spelling and try partial matches
2. Remove filters that might be limiting results
3. Try different search terms or synonyms
4. Verify the item hasn't been archived or deleted
```

---

## Auto-Detection Rules

DocuGen can automatically suggest troubleshooting content based on:

| UI Pattern | Suggested Issue |
|------------|-----------------|
| Disabled button | Permission issue |
| Required field indicator (*) | Validation may fail |
| File input element | File upload issues |
| Search/filter UI | No results scenario |
| Form with submit | Submission failures |
| External link | Not found errors |

## Customization

Users can:
1. Override auto-detected issues
2. Add application-specific troubleshooting
3. Exclude certain patterns
4. Provide custom resolution steps
