---
name: data-seeding
description: Guide to seeding initial data using SCL instance blocks.
---
# Data Seeding Skill

> [!IMPORTANT]
> **NEVER** use Actions, Scripts, or SDK calls to seed initial static data.
> You must use SCL `instance` blocks for all static data (dictionaries, fixed records, configuration).

## 1. The `instance` Strategy
Simple Platform treats data defined in SCL as "Configuration as Data". This guarantees that:
1.  IDs are consistent across environments (Dev -> Stage -> Prod).
2.  Data is version-controlled.
3.  Deployments are idempotent (no duplicate inserts).

## 2. Syntax: The `instance` Block
Use the `instance` keyword to define records in your `*.scl` files.

### Format
```scl
instance "<app>.<model>" "<human_readable_id>" {
  <field_name> = <value>
  <relation_field> = <relation_id>
}
```

### Example: Seeding Room Types
File: `apps/com.acme.crm/records/50_data_room_types.scl`

```scl
instance "com.acme.crm.room_type" "kng" {
  code = "KNG"
  name = "King Room"
  base_rate = 250.00
  max_occupancy = 2
}

instance "com.acme.crm.room_type" "ste" {
  code = "STE"
  name = "Grand Suite"
  base_rate = 650.00
  max_occupancy = 4
}
```

### Example: Seeding with Relations
File: `apps/com.acme.crm/records/50_data_rooms.scl`

```scl
instance "com.acme.crm.room" "101" {
  room_number = "101"
  floor = "1"
  property = "hq_grand_palace"  # References instance "com.acme.crm.property" "hq_grand_palace"
  room_type = "kng"             # References instance "com.acme.crm.room_type" "kng"
  housekeeping_status = "Clean" # Enum String
}
```

## 3. Rules for Values
*   **Strings**: Double quotes `"Value"`.
*   **Numbers**: Direct `123` or `12.50`.
*   **Booleans**: `true` or `false`.
*   **Enums**: Use the exact string value `"Clean"`.
*   **Relations**: Use the **string ID** (the second argument of the `instance` definition) of the target record.

> [!TIP]
> Place your seed data in `apps/<app>/records/` with a prefix like `50_data_` to organize them.
