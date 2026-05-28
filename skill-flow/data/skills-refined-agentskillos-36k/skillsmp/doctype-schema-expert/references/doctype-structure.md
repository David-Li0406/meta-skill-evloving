# DocType Structure Reference

Complete reference for DocType JSON structure and properties.

## Minimal DocType Structure

```json
{
  "actions": [],
  "creation": "2024-01-01 00:00:00.000000",
  "doctype": "DocType",
  "engine": "InnoDB",
  "field_order": [],
  "fields": [],
  "modified": "2024-01-01 00:00:00.000000",
  "modified_by": "Administrator",
  "module": "Module Name",
  "name": "DocType Name",
  "owner": "Administrator",
  "permissions": [],
  "sort_field": "modified",
  "sort_order": "DESC",
  "states": [],
  "links": []
}
```

## Core Properties

### Required Properties

| Property | Type | Description |
|----------|------|-------------|
| `doctype` | String | Always "DocType" |
| `name` | String | DocType name (PascalCase, spaces allowed) |
| `module` | String | Module name (links to Module Def) |
| `fields` | Array | Array of field definitions |
| `permissions` | Array | Array of permission definitions |

### Type Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `istable` | Int | 0 | Child table (1) or regular DocType (0) |
| `issingle` | Int | 0 | Single DocType (1) or table-based (0) |
| `is_submittable` | Int | 0 | Enable Submit/Cancel workflow |
| `is_tree` | Int | 0 | Hierarchical tree structure |
| `is_virtual` | Int | 0 | Virtual DocType (no database table) |
| `custom` | Int | 0 | Custom DocType (created via UI) |

### Naming Properties

| Property | Type | Description |
|----------|------|-------------|
| `naming_rule` | String | Options: "Set by user", "By fieldname", "By Script", "Expression", "Random", "Autoincrement", "By parent field" |
| `autoname` | String | Naming pattern (e.g., "PROJ-.####", "field:customer_name", "Prompt") |
| `allow_rename` | Int | Allow renaming documents |

### Form Settings

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `editable_grid` | Int | 1 | Enable inline editing (for child tables) |
| `quick_entry` | Int | 0 | Enable quick entry dialog |
| `hide_toolbar` | Int | 0 | Hide toolbar in form view |
| `allow_copy` | Int | 0 | Allow copying documents |
| `allow_import` | Int | 0 | Enable data import |
| `allow_auto_repeat` | Int | 0 | Enable recurring documents |
| `track_changes` | Int | 0 | Track document changes |
| `track_seen` | Int | 0 | Track when document is viewed |
| `track_views` | Int | 0 | Track all document views |
| `max_attachments` | Int | null | Maximum allowed attachments |
| `make_attachments_public` | Int | 0 | Make attachments publicly accessible |

### View Settings

| Property | Type | Description |
|----------|------|-------------|
| `title_field` | String | Field to use as document title |
| `show_title_field_in_link` | Int | Show title in link fields |
| `image_field` | String | Field containing image URL |
| `timeline_field` | String | Field to link in timeline |
| `search_fields` | String | Comma-separated fields for search. These fields are used for searching in Link field dropdowns and also appear in the displayed records when using the default Link field implementation. |
| `default_print_format` | String | Default print format name |
| `sort_field` | String | Default sort field |
| `sort_order` | String | "ASC" or "DESC" |
| `default_view` | String | "List", "Report", "Dashboard", "Calendar", "Gantt", "Image", "Inbox", "Tree", "Kanban", "Map" |
| `icon` | String | Icon name |
| `color` | String | Color for UI elements |
| `show_preview_popup` | Int | Show preview on hover |
| `show_name_in_global_search` | Int | Include in global search |

### Email Settings

| Property | Type | Description |
|----------|------|-------------|
| `email_append_to` | Int | Allow email replies to create comments |
| `sender_field` | String | Field containing sender email |
| `sender_name_field` | String | Field containing sender name |
| `recipient_account_field` | String | Email account for sending |
| `subject_field` | String | Field to use as email subject |
| `default_email_template` | String | Default email template |

### Web/Portal Settings

| Property | Type | Description |
|----------|------|-------------|
| `has_web_view` | Int | Enable web portal view |
| `allow_guest_to_view` | Int | Allow public access |
| `route` | String | URL route field |
| `is_published_field` | String | Field indicating published status |
| `website_search_field` | String | Field to use in website search |
| `index_web_pages_for_search` | Int | Index for search engines |

### Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `engine` | String | Database engine (usually "InnoDB") |
| `document_type` | String | "Document", "Setup", "System", "Other" |
| `beta` | Int | Mark as beta feature |
| `queue_in_background` | Int | Queue operations in background |
| `restrict_to_domain` | String | Domain restriction |
| `read_only` | Int | Make DocType read-only |
| `in_create` | Int | Show in "New" dropdown |
| `migration_hash` | String | Hash for migration tracking |

### Tree Settings (when is_tree = 1)

| Property | Type | Description |
|----------|------|-------------|
| `nsm_parent_field` | String | Field name for parent reference |

### Calendar/Gantt Settings (when is_calendar_and_gantt = 1)

| Property | Type | Description |
|----------|------|-------------|
| `is_calendar_and_gantt` | Int | Enable calendar/gantt views |

### Grid Settings

| Property | Type | Description |
|----------|------|-------------|
| `grid_page_length` | Int | Number of rows per page in grid |
| `rows_threshold_for_grid_search` | Int | Min rows before search is shown |

## Array Properties

### fields

Array of field definitions. Each field is an object with properties defined in field-properties.md.

### permissions

Array of permission definitions:

```json
{
  "create": 1,
  "delete": 1,
  "email": 1,
  "export": 1,
  "print": 1,
  "read": 1,
  "report": 1,
  "role": "System Manager",
  "share": 1,
  "write": 1,
  "if_owner": 0,
  "permlevel": 0,
  "submit": 0,
  "cancel": 0,
  "amend": 0
}
```

### actions

Array of custom actions:

```json
{
  "label": "Action Label",
  "action": "action_function",
  "action_type": "Server Action",
  "hidden": 0
}
```

### links

Array of dashboard links to related doctypes:

```json
{
  "link_doctype": "Related DocType",
  "link_fieldname": "field_name",
  "group": "Group Name"
}
```

### states

Array of workflow states:

```json
{
  "title": "State Title",
  "color": "Blue"
}
```

## Field Order

The `field_order` array controls the sequence of fields in the form. It contains fieldnames in the desired order:

```json
"field_order": [
  "section_break_1",
  "customer",
  "customer_name",
  "column_break_2",
  "posting_date",
  "items_section",
  "items"
]
```

If `field_order` is empty or missing, fields appear in the order they're defined in the `fields` array.

## Complete Example

```json
{
  "actions": [],
  "allow_import": 1,
  "allow_rename": 1,
  "autoname": "PROJ-.####",
  "creation": "2024-01-01 12:00:00.000000",
  "custom": 0,
  "doctype": "DocType",
  "document_type": "Document",
  "editable_grid": 1,
  "engine": "InnoDB",
  "field_order": [
    "project_name",
    "status",
    "section_break_1",
    "description",
    "column_break_2",
    "start_date",
    "end_date"
  ],
  "fields": [
    {
      "fieldname": "project_name",
      "fieldtype": "Data",
      "label": "Project Name",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "status",
      "fieldtype": "Select",
      "label": "Status",
      "options": "Open\nIn Progress\nCompleted\nCancelled",
      "default": "Open"
    },
    {
      "fieldname": "section_break_1",
      "fieldtype": "Section Break"
    },
    {
      "fieldname": "description",
      "fieldtype": "Text Editor",
      "label": "Description"
    },
    {
      "fieldname": "column_break_2",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "start_date",
      "fieldtype": "Date",
      "label": "Start Date",
      "reqd": 1
    },
    {
      "fieldname": "end_date",
      "fieldtype": "Date",
      "label": "End Date"
    }
  ],
  "is_submittable": 0,
  "issingle": 0,
  "istable": 0,
  "links": [],
  "modified": "2024-01-01 12:00:00.000000",
  "modified_by": "Administrator",
  "module": "Projects",
  "name": "Project",
  "naming_rule": "Expression",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "delete": 1,
      "email": 1,
      "export": 1,
      "print": 1,
      "read": 1,
      "report": 1,
      "role": "System Manager",
      "share": 1,
      "write": 1
    }
  ],
  "quick_entry": 1,
  "search_fields": "project_name,status",
  "sort_field": "modified",
  "sort_order": "DESC",
  "states": [],
  "title_field": "project_name",
  "track_changes": 1
}
```
