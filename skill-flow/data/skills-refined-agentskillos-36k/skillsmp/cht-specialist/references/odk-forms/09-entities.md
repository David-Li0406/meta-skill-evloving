# Entities (Longitudinal Data)

Entities enable multi-step workflows where data persists between forms.

## Overview

An **Entity** represents a "thing" (person, place, case) that needs to be:
- Shared between forms
- Tracked over time
- Updated by multiple submissions

**Entity List**: Collection of related entities (like a shared database).

## When to Use Entities

- Site inspections with follow-ups
- Baseline and follow-up studies
- Case management (healthcare, crisis response)
- Any workflow needing data flow between forms

---

## Creating Entities

### 1. Add Entities Sheet

| list_name | label |
|-----------|-------|
| patients | concat(${first_name}, ' ', ${last_name}) |

### 2. Add save_to Column in Survey Sheet

| type | name | label | save_to |
|------|------|-------|---------|
| text | first_name | First Name | first_name |
| text | last_name | Last Name | last_name |
| date | dob | Date of Birth | date_of_birth |
| text | phone | Phone Number | phone |

### How It Works

1. Form creates an entity in the specified list
2. `save_to` maps form fields to entity properties
3. `label` expression defines display name
4. Central automatically creates the Entity List

---

## Using Entities in Forms

### Select Entity

| type | name | label |
|------|------|-------|
| select_one_from_file patients.csv | patient | Select Patient |

**Note:** Use `.csv` extension even for Entity Lists.

### Access Entity Properties

```
instance("patients")/root/item[name = ${patient}]/first_name
instance("patients")/root/item[name = ${patient}]/phone
```

### Pre-populate from Entity

| type | name | label | calculation |
|------|------|-------|-------------|
| select_one_from_file patients.csv | patient | Select Patient | |
| calculate | patient_name | | instance("patients")/root/item[name = ${patient}]/first_name |
| calculate | patient_phone | | instance("patients")/root/item[name = ${patient}]/phone |

---

## Updating Entities

Add `entity_id` to entities sheet:

| list_name | label | entity_id |
|-----------|-------|-----------|
| patients | | ${patient} |

### Update Specific Properties

| type | name | label | save_to |
|------|------|-------|---------|
| select_one_from_file patients.csv | patient | Select Patient | |
| text | new_phone | Updated Phone | phone |
| select_one status | status | Current Status | status |

---

## Conditional Create/Update

### Create Only When New

| list_name | label | create_if |
|-----------|-------|-----------|
| patients | concat(${first_name}, ' ', ${last_name}) | ${patient} = '' |

### Update Only When Condition Met

| list_name | label | entity_id | update_if |
|-----------|-------|-----------|-----------|
| patients | | ${patient} | ${status} = 'approved' |

### Combined Create/Update Pattern

| list_name | label | entity_id | create_if | update_if |
|-----------|-------|-----------|-----------|-----------|
| patients | concat(${first_name}, ' ', ${last_name}) | coalesce(${patient}, uuid()) | ${patient} = '' | ${patient} != '' |

---

## Filtering Entities

Use `choice_filter` to show relevant entities:

| type | name | label | choice_filter |
|------|------|-------|---------------|
| select_one_from_file patients.csv | patient | Select Patient | status != 'closed' |
| select_one_from_file patients.csv | patient | Active Patients | status = 'active' and assigned_to = ${username} |

---

## Entity Structure

### System Properties

| Property | Description |
|----------|-------------|
| `name` / `__id` | Unique UUID |
| `label` | Display name |
| `__version` | Update counter |
| `__createdAt` | Creation timestamp |
| `__updatedAt` | Last update timestamp |
| `__createdBy` | Creator identity |

### Accessing System ID

In calculations:
```
/data/meta/entity/@id
```

---

## Workflow Example: Patient Follow-Up

### Registration Form (creates entity)

**entities sheet:**

| list_name | label |
|-----------|-------|
| patients | concat(${first_name}, ' ', ${last_name}) |

**survey sheet:**

| type | name | label | save_to |
|------|------|-------|---------|
| text | first_name | First Name | first_name |
| text | last_name | Last Name | last_name |
| date | dob | Date of Birth | dob |
| geopoint | location | Home Location | location |

### Follow-Up Form (uses and updates entity)

**entities sheet:**

| list_name | label | entity_id |
|-----------|-------|-----------|
| patients | | ${patient} |

**survey sheet:**

| type | name | label | save_to |
|------|------|-------|---------|
| select_one_from_file patients.csv | patient | Select Patient | |
| date | visit_date | Visit Date | last_visit |
| select_one status | status | Status | status |
| text | notes | Notes | last_notes |

---

## Managing Entities in Central

### Creating Entity Lists

1. **Via form upload:** Automatic when publishing form
2. **Manually:** Entity Lists tab → New
3. **CSV import:** Upload CSV with `label` column

### Entity Settings

- **Create on receive:** Immediate creation
- **Create on approval:** After manager approval

### Conflict Resolution

Conflicts occur with parallel updates. Central applies all updates in order received. Review and resolve manually in Central UI.

---

## Limitations

| Limitation | Details |
|------------|---------|
| Single entity per submission | Can only create/update one entity |
| All entities downloaded | Cannot subset per user |
| String properties only | No native numbers/dates |
| No file attachments | Cannot attach media to entities |
| Offline support | Requires Central 2024.3.0+ |

---

## Best Practices

### Entity Labels

- Make labels unique and identifiable
- Include key information (name, ID)
- Keep reasonably short

### Property Names

- Use consistent naming across forms
- Avoid reserved names (`name`, `label`, `__*`)
- Document property meanings

### Performance

- Don't create too many entities
- Use filters to reduce selection lists
- Consider data retention policies
