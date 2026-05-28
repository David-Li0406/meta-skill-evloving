# Migration: Categories → Classes

**Date:** 2025-11-19
**Status:** ✅ Complete
**Migration ID:** 010

---

## Overview

This migration moves TheHUB from the simple `categories` table to the more advanced `classes` system. The classes system provides better granularity, discipline support, and automatic class assignment based on rider age and gender.

## Why Migrate?

### Problems with Categories
- **Too Broad:** Categories like "Herr Elite" covered ages 19-34, too wide for competitive racing
- **Limited Discipline Support:** No way to have different categories per discipline (Road vs MTB)
- **No Point Scales:** Couldn't assign different point scales to different categories
- **Manual Only:** Required manual category assignment

### Benefits of Classes
- **Fine-Grained:** Classes like M17, M19, M23, M30, M40 match actual age groups
- **Discipline-Specific:** Can have different classes for ROAD, MTB, XC, DH, ENDURO
- **Point Scale Integration:** Each class can have its own point scale
- **Automatic Assignment:** Riders are automatically assigned to classes based on birth_year and event date

## What Changed

### Database Schema

#### Tables Updated
1. **categories** - Marked as DEPRECATED, active set to 0 by default
2. **results** - Now uses `class_id` instead of `category_id`
3. **Database Views** - Updated to use classes:
   - `results_complete` - Now includes `class_name` and `class_display_name`
   - `cyclist_stats` - Now uses `class_position` and `class_points`

#### New Columns Used
- `results.class_id` - Foreign key to classes table
- `results.class_position` - Position within class
- `results.class_points` - Points earned in class

### PHP Files Updated

1. **event.php** - Displays results by class instead of category
2. **results.php** - Uses class_position and class_display_name
3. **admin/edit-results.php** - Groups results by class
4. **database/schema.sql** - Views updated, categories deprecated

### Files NOT Changed (Already Using Classes)
- `includes/class-calculations.php` - Already implements class logic
- `admin/classes.php` - Admin interface for managing classes
- `admin/import-results.php` - Already supports class assignment

## Migration Files

### 1. SQL Migration
**File:** `database/migrations/010_migrate_categories_to_classes.sql`

**What it does:**
- Maps existing `results.category_id` to `results.class_id`
- Uses rider's birth_year and event date to determine correct class
- Creates fallback generic classes (M_GENERIC, K_GENERIC, OPEN_GENERIC) for unmapped results
- Creates audit log table `category_class_migration_log`
- Generates summary statistics

### 2. PHP Migration Runner
**File:** `database/migrations/run_010_migration.php`

**What it does:**
- Runs the SQL migration
- Enables classes for all affected events
- Recalculates class positions for all events
- Recalculates class points for all events
- Generates detailed report

## How to Run the Migration

### Prerequisites
- Backup your database
- Ensure all riders have `birth_year` and `gender` filled in
- Verify classes exist in the `classes` table

### Steps

1. **Backup Database**
   ```bash
   mysqldump -u user -p database_name > backup_before_migration.sql
   ```

2. **Run Migration**
   ```bash
   cd /path/to/TheHUB
   php database/migrations/run_010_migration.php
   ```

3. **Review Report**
   - Check the generated report file
   - Verify migration statistics
   - Look for any warnings or unmigrated results

4. **Test Application**
   - View event results pages
   - Check admin edit results page
   - Verify class standings in series

5. **If Everything Works:**
   ```bash
   git add .
   git commit -m "feat: Migrate from categories to classes system"
   git push
   ```

### Rollback (If Needed)

If something goes wrong:

```sql
-- Restore from backup
mysql -u user -p database_name < backup_before_migration.sql

-- Or manually clear class assignments
UPDATE results SET class_id = NULL WHERE category_id IS NOT NULL;
UPDATE events SET enable_classes = 0;
```

## Migration Statistics (Example)

After running the migration, you'll see stats like:

```
Results migrated: 1,247
Events affected: 15
Riders affected: 342

Top 10 Classes:
  M30                Män 30-39 år                                 287 results
  M40                Män 40-49 år                                 201 results
  K30                Kvinnor 30-39 år                             156 results
  M17                Män 17-18 år                                 143 results
  ...
```

## Verification Checklist

After migration, verify:

- [ ] All event result pages display correctly
- [ ] Class names show properly (e.g., "Män 30-39 år")
- [ ] Positions are correct within each class
- [ ] Points are calculated correctly
- [ ] Series standings use class-based points
- [ ] Admin edit results page works
- [ ] No errors in application logs

## Data Mapping Examples

### Category → Class Mapping

| Old Category       | Rider Age | New Class | Class Display Name    |
|-------------------|-----------|-----------|----------------------|
| Herr Elite        | 25        | M23       | Män 23-29 år        |
| Herr Elite        | 32        | M30       | Män 30-39 år        |
| Dam Elite         | 27        | K23       | Kvinnor 23-29 år    |
| Herr Junior       | 17        | M17       | Män 17-18 år        |
| Herr Veteran 35-44| 38        | M30       | Män 30-39 år        |
| Herr Veteran 45-54| 47        | M40       | Män 40-49 år        |

## Known Issues & Solutions

### Issue: Some results have no class_id
**Cause:** Rider missing birth_year or gender
**Solution:** Update rider data, then re-run migration

### Issue: Wrong class assigned
**Cause:** Incorrect birth_year or event date
**Solution:** Fix data, then use admin interface to reassign class

### Issue: Point scales not working
**Cause:** Events don't have enable_classes = 1
**Solution:** Migration script enables it automatically

## Future Improvements

After this migration:
- [ ] Remove `category_id` column from `results` table (after 6 months)
- [ ] Drop `categories` table (after 12 months)
- [ ] Update import scripts to only use classes
- [ ] Add class-based filtering to reports

## Support

If you encounter issues:

1. Check the migration log: `database/migrations/010_migration_report_*.txt`
2. Review audit log: `SELECT * FROM category_class_migration_log WHERE new_class_id IS NULL`
3. Check application logs for errors
4. Contact development team

## References

- Migration 008: `database/migrations/008_classes_system.sql` - Original classes system
- Migration 009: `database/migrations/009_add_class_and_split_times.sql` - Added split times
- Class Calculations: `includes/class-calculations.php` - Class logic implementation
- Admin Interface: `admin/classes.php` - Manage classes

---

**Migration completed by:** Claude Code
**Date:** 2025-11-19
**Approved by:** [Pending User Approval]
