# Database Migrations

This folder contains SQL migration files for TheHUB database.

## Running Migrations

### Option 1: phpMyAdmin
1. Log in to phpMyAdmin
2. Select `if0_40400950_THEHUB` database
3. Go to "SQL" tab
4. Copy and paste the migration SQL
5. Click "Go"

### Option 2: Command line (if you have MySQL access)
```bash
mysql -u if0_40400950 -p if0_40400950_THEHUB < database/migrations/002_add_license_fields.sql
```

## Migration 002: Add License Fields

**File:** `002_add_license_fields_with_table_creation.sql`

**Description:** Creates cyclists table (if needed) and adds license management fields:
- `license_type` - Type of license (Elite, Youth, Hobby, etc)
- `license_category` - Specific category (Elite Men, Master Women 35+, etc)
- `discipline` - Cycling discipline (MTB, Road, Track, etc)
- `license_valid_until` - License expiry date

**Features:**
- ✅ Creates `clubs` table if it doesn't exist (required for foreign key)
- ✅ Creates `cyclists` table with all fields if it doesn't exist
- ✅ Adds missing license fields to existing `cyclists` table
- ✅ Safe to run multiple times - checks before adding columns

**Required:** Run this before using the new license features

**Status:** ⚠️ READY TO RUN - Copy entire file content and paste in phpMyAdmin SQL tab!

## After Running Migration

1. Test with sample data:
```sql
-- Insert test cyclist with new fields
INSERT INTO cyclists (
    firstname, lastname, birth_year, gender,
    license_type, license_category, discipline, license_valid_until
) VALUES (
    'Test', 'Cyclist', 1990, 'M',
    'Elite', 'Elite Men', 'MTB', '2025-12-31'
);
```

2. Verify fields exist:
```sql
DESCRIBE cyclists;
```

You should see the new columns in the output.

## Troubleshooting

**Error: "Duplicate column name"**
- The migration has already been run
- Check if columns exist: `SHOW COLUMNS FROM cyclists LIKE 'license_%';`

**Error: "Table doesn't exist"**
- Make sure you're in the correct database
- Run the base schema first: `database/schema.sql`
