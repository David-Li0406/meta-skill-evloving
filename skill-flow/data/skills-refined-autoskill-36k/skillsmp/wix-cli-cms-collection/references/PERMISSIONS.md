# Permissions Reference

Complete documentation of access levels for CMS collection permissions in Wix CLI apps.

## Access Levels

### UNDEFINED

Not set. No explicit permission configured.

**Use cases:**

- When permissions should be inherited from parent/default settings
- Temporary state during development
- When explicit permission is not needed

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "UNDEFINED",
    "itemInsert": "UNDEFINED",
    "itemUpdate": "UNDEFINED",
    "itemRemove": "UNDEFINED"
  }
}
```

### ANYONE

Any subject, including visitors (public access).

**Use cases:**

- Public content that anyone can read
- Public data that doesn't require authentication
- Content visible to all site visitors

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Security note:** Use with caution for write operations. Typically used for `itemRead` only.

### SITE_MEMBER

Any signed-in user (both site members and collaborators).

**Use cases:**

- Content accessible to all logged-in users
- Member-only content
- Data that requires authentication but not special roles

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "SITE_MEMBER",
    "itemInsert": "SITE_MEMBER",
    "itemUpdate": "SITE_MEMBER",
    "itemRemove": "SITE_MEMBER"
  }
}
```

### SITE_MEMBER_AUTHOR

Any signed-in user, but site members only have access to their own items.

**Use cases:**

- User-generated content where users manage their own items
- Personal data that users can edit but not others'
- Content ownership model

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "SITE_MEMBER_AUTHOR",
    "itemInsert": "SITE_MEMBER",
    "itemUpdate": "SITE_MEMBER_AUTHOR",
    "itemRemove": "SITE_MEMBER_AUTHOR"
  }
}
```

**Behavior:**

- Site members can only read/update/remove items they created
- Collaborators (site owners/admins) have full access
- Useful for user-generated content with ownership

### CMS_EDITOR

Site collaborator that has a role with CMS Access permission.

**Use cases:**

- Content managed by CMS editors
- Editorial workflows
- Content that requires CMS editing permissions

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "CMS_EDITOR",
    "itemInsert": "CMS_EDITOR",
    "itemUpdate": "CMS_EDITOR",
    "itemRemove": "CMS_EDITOR"
  }
}
```

### PRIVILEGED

CMS administrators and users or roles granted with special access.

**Use cases:**

- Administrative data
- Sensitive information
- System configuration
- Default for write operations in Wix CLI apps

**Example:**

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Security note:** Most restrictive level. Only administrators and privileged users can perform operations.

## Permission Operations

Each collection defines permissions for four operations:

### itemRead

Who can read/query items from the collection.

**Common patterns:**

- `ANYONE` - Public content
- `SITE_MEMBER` - Member-only content
- `PRIVILEGED` - Administrative data

### itemInsert

Who can create new items in the collection.

**Common patterns:**

- `PRIVILEGED` - Default in Wix CLI apps, administrative control
- `SITE_MEMBER` - User-generated content
- `SITE_MEMBER_AUTHOR` - Users create their own items

### itemUpdate

Who can modify existing items.

**Common patterns:**

- `PRIVILEGED` - Default in Wix CLI apps, administrative control
- `SITE_MEMBER_AUTHOR` - Users edit their own items
- `CMS_EDITOR` - Editorial workflows

### itemRemove

Who can delete items from the collection.

**Common patterns:**

- `PRIVILEGED` - Default in Wix CLI apps, administrative control
- `SITE_MEMBER_AUTHOR` - Users delete their own items
- `CMS_EDITOR` - Editorial control

## Default Patterns and Recommendations

### Default Pattern (Recommended)

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Rationale:**

- Read: Public access for most content
- Write: Administrative control by default for security

### Public Content Pattern

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Use when:** Content should be publicly readable but only admins can modify.

### User-Generated Content Pattern

```json
{
  "dataPermissions": {
    "itemRead": "SITE_MEMBER",
    "itemInsert": "SITE_MEMBER",
    "itemUpdate": "SITE_MEMBER_AUTHOR",
    "itemRemove": "SITE_MEMBER_AUTHOR"
  }
}
```

**Use when:** Users create and manage their own content (e.g., user posts, comments).

### Editorial Workflow Pattern

```json
{
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "CMS_EDITOR",
    "itemUpdate": "CMS_EDITOR",
    "itemRemove": "CMS_EDITOR"
  }
}
```

**Use when:** Content is managed by CMS editors with editorial workflows.

### Private/Administrative Pattern

```json
{
  "dataPermissions": {
    "itemRead": "PRIVILEGED",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

**Use when:** Sensitive data that only administrators should access.

## Security Best Practices

1. **Principle of Least Privilege:** Grant minimum permissions needed
2. **Read vs Write:** Public read is often safe; restrict writes
3. **Default to PRIVILEGED for writes:** Wix CLI apps default to `PRIVILEGED` for insert/update/remove
4. **Use SITE_MEMBER_AUTHOR for user content:** When users manage their own items
5. **Avoid ANYONE for writes:** Rarely appropriate for security reasons
6. **Review permissions:** Ensure permissions match the use case

## Automatic Permission Forcing

The codegen system automatically overrides all data permissions to `ANYONE` for collections with INSERT or UPDATE operations. This happens regardless of what permissions are specified in the plan.

**Affected Collections:**

- Collections with `operation: "INSERT"` - New collections being created
- Collections with `operation: "UPDATE"` - Existing collections being modified

**What Gets Overridden:**

All four permission fields are automatically set to `ANYONE`:

- `itemRead: "ANYONE"`
- `itemInsert: "ANYONE"`
- `itemUpdate: "ANYONE"`
- `itemRemove: "ANYONE"`

**Important Notes:**

- This automatic override happens during plan processing, before collections are generated
- The specified permissions in the plan are ignored for INSERT and UPDATE operations
- Collections with DELETE operations are not affected by this automatic forcing
- This ensures all collections being created or updated have open permissions set to `ANYONE`

**Security Implications:**

This automatic forcing means that all collections created or updated will have public access permissions. Site owners should review and adjust permissions after generation if more restrictive access is needed.

## Permission Hierarchy

From most restrictive to least restrictive:

1. **PRIVILEGED** - Administrators only
2. **CMS_EDITOR** - CMS editors with permissions
3. **SITE_MEMBER_AUTHOR** - Members (own items) / Collaborators (all)
4. **SITE_MEMBER** - All signed-in users
5. **ANYONE** - Public access
6. **UNDEFINED** - Not set (inherits defaults)

## Complete Example

```json
{
  "idSuffix": "blog-posts",
  "displayName": "Blog Posts",
  "fields": [
    {
      "key": "title",
      "displayName": "Title",
      "type": "TEXT"
    }
  ],
  "dataPermissions": {
    "itemRead": "ANYONE",
    "itemInsert": "PRIVILEGED",
    "itemUpdate": "PRIVILEGED",
    "itemRemove": "PRIVILEGED"
  }
}
```

This example shows:

- Public can read blog posts
- Only administrators can create, update, or delete posts
- Follows Wix CLI default pattern
