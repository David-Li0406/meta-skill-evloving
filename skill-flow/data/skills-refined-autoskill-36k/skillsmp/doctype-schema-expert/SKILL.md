---
name: doctype-schema-expert
description: Expert guidance on Frappe DocType schemas including JSON structure, field types, properties, naming conventions, and best practices. Use when creating, modifying, or analyzing DocType JSON files, understanding DocType structure, working with field definitions, configuring DocType properties, or troubleshooting schema-related issues.
---

# DocType Schema Expert

This skill provides comprehensive guidance for working with Frappe DocType schemas, their JSON structure, field definitions, and best practices.

## Overview

DocTypes are the fundamental building blocks of a Frappe application. Each DocType defines:

- **Database Table Structure**: Fields and their types
- **UI Form Layout**: How data is displayed and edited
- **Business Logic**: Controllers and validation rules
- **Permissions**: Who can access and modify data

Every DocType is defined by a JSON file (e.g., `doctype_name.json`) that specifies the complete schema.

**Note**: Custom DocTypes created via the UI do not have a .json file on disk. Their definition is stored in the database only. Standard DocTypes (shipped with apps) have JSON files in the codebase.

## Quick Reference

### Core DocType Properties

Essential properties that define a DocType's behavior:

- **doctype**: Always "DocType"
- **name**: The DocType name (e.g., "Sales Order")
- **module**: Module this DocType belongs to
- **istable**: Set to 1 for child tables (used in Table fields)
- **issingle**: Set to 1 for single doctypes (no table, one instance only)
- **is_submittable**: Set to 1 to enable Submit/Cancel workflow
- **is_tree**: Set to 1 for hierarchical/tree structures
- **editable_grid**: Set to 1 for inline editing in child tables
- **custom**: Set to 1 for custom doctypes
- **fields**: Array of field definitions
- **permissions**: Array of permission definitions

### Field Types Categories

**Data Fields** (store values):
- Text: `Data`, `Text`, `Small Text`, `Long Text`, `Code`, `Text Editor`, `HTML Editor`, `Markdown Editor`
- Numeric: `Int`, `Long Int`, `Float`, `Currency`, `Percent`
- Date/Time: `Date`, `Datetime`, `Time`, `Duration`
- Special: `Link`, `Dynamic Link`, `Select`, `Check`, `Attach`, `Attach Image`, `JSON`, `Password`, `Color`, `Barcode`, `Geolocation`, `Rating`, `Signature`, `Phone`, `Autocomplete`, `Icon`, `Read Only`

**Layout Fields** (UI structure only):
- `Section Break`, `Column Break`, `Tab Break`, `HTML`, `Button`, `Image`, `Fold`, `Heading`

**Relationship Fields**:
- `Table`: Child table (one-to-many)
- `Table MultiSelect`: Multiple selection from child table
- `Link`: Foreign key to another DocType
- `Dynamic Link`: Foreign key determined by another field

## Common Tasks

### Creating a New DocType

1. Create JSON file: `frappe/module_name/doctype/doctype_name/doctype_name.json`
2. Define basic structure with required properties
3. Add fields in the `fields` array
4. Define permissions in the `permissions` array
5. Run `bench migrate` to create database table

See [references/doctype-structure.md](references/doctype-structure.md) for complete structure.

### Adding Fields

Add field objects to the `fields` array with these essential properties:

```json
{
  "fieldname": "field_name",
  "fieldtype": "Data",
  "label": "Field Label",
  "reqd": 0,
  "hidden": 0,
  "read_only": 0
}
```

See [references/field-types.md](references/field-types.md) for all field types and their properties.

### Child Tables

Child tables require:

1. Parent DocType: Field with `fieldtype: "Table"` and `options` pointing to child DocType
2. Child DocType: Set `istable: 1` and include parent tracking fields

The framework automatically adds `parent`, `parenttype`, and `parentfield` fields to child tables.

### Single DocTypes

Single doctypes (settings, configurations) have only one instance:

- Set `issingle: 1`
- Data stored in `tabSingles` table, not a dedicated table
- No `name` field needed (automatically set to DocType name)
- Cannot be renamed or have multiple instances

## Reference Files

For detailed information on specific topics:

### Structure and Properties
- **[references/doctype-structure.md](references/doctype-structure.md)**: Complete DocType JSON structure with all properties
- **[references/field-types.md](references/field-types.md)**: All field types with descriptions and use cases
- **[references/field-properties.md](references/field-properties.md)**: All field properties and their effects

### Best Practices
- **[references/naming-conventions.md](references/naming-conventions.md)**: Naming rules for DocTypes, fields, and fieldnames
- **[references/best-practices.md](references/best-practices.md)**: Schema design patterns and recommendations

### Common Patterns
- **[references/common-patterns.md](references/common-patterns.md)**: Frequently used DocType patterns and configurations

## Key Principles

1. **Naming**: Use PascalCase for DocType names, snake_case for fieldnames
2. **Required Fields**: Mark mandatory fields with `reqd: 1`
3. **Field Order**: Use `field_order` array to control field sequence
4. **Layout**: Use Section/Column Breaks for organized forms
5. **Validation**: Set properties like `unique`, `non_negative`, `precision` for data integrity
6. **Performance**: Add `search_index: 1` to frequently queried fields
7. **User Experience**: Use appropriate field types and provide helpful labels/descriptions

## Standard Fields

Every DocType automatically includes these fields (don't add manually):

- `name`: Unique identifier
- `owner`: User who created the document
- `creation`: Creation timestamp
- `modified`: Last modification timestamp
- `modified_by`: User who last modified
- `docstatus`: Document status (0=Draft, 1=Submitted, 2=Cancelled)
- `idx`: Index for sorting

Optional fields (added automatically when used):
- `_user_tags`: User tags
- `_comments`: Comments
- `_assign`: Assigned users
- `_liked_by`: Users who liked
- `_seen`: Users who viewed

## Usage

When working with DocType schemas:

1. **Identify the task**: Creating new DocType, modifying existing, adding fields, etc.
2. **Reference appropriate guide**: Use reference files for detailed information
3. **Follow conventions**: Adhere to naming and structure guidelines
4. **Validate schema**: Ensure all required properties are present
5. **Test changes**: Run migrations and verify functionality

## Important Notes

- JSON files must be valid JSON (use double quotes, no trailing commas)
- Changes to DocType schema require running `bench migrate`
- Renaming fields or changing field types can cause data loss
- Always backup before making schema changes
- Test schema changes in development before production
- Field names cannot be changed after data exists (requires migration)
