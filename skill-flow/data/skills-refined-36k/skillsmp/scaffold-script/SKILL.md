---
name: scaffold-script
description: Generate a new data script with proper boilerplate, database connection, error handling, and project conventions. Use when creating new analysis scripts, building migration scripts, implementing data quality checks, or importing external data.
---

# Scaffold Script

**Purpose:** Quickly create new analysis or migration scripts following project patterns.

## Instructions for Claude

When this skill is invoked:

1. **Parse arguments:**
   - `script-name`: name of the script (e.g., "checkMissingCompanies")
   - `description`: what the script does (e.g., "Find people missing company IDs")

2. **Generate script file** at `scripts/<script-name>.js` with:

   **Standard boilerplate:**
   - Mongoose connection using database utility
   - Dotenv config
   - Winston logger (if needed)
   - Proper imports of models
   - Async main function
   - Error handling
   - Graceful disconnect

   **Project conventions:**
   - Use `require('../src/utils/database')` for connection
   - Use `async/await` (never `.then()`)
   - Follow JavaScript rules from `.claude/rules/javascript.md`
   - Add helpful comments
   - Support `--dry-run` flag if modifying data

3. **Template structure:**
   ```javascript
   const mongoose = require('mongoose');
   const path = require('path');
   require('dotenv').config({ path: path.join(__dirname, '..', '.env') });
   const database = require('../src/utils/database');

   // Import models as needed
   const Person = require('../src/models/person');

   /**
    * [Script Name]
    *
    * [Description]
    *
    * Usage:
    *   node scripts/[script-name].js [--dry-run]
    */

   async function main() {
     await database.connect();

     console.log('\n========================================');
     console.log('[SCRIPT NAME]');
     console.log('========================================\n');

     const dryRun = process.argv.includes('--dry-run');
     if (dryRun) {
       console.log('🔍 DRY RUN MODE - No changes will be made\n');
     }

     // TODO: Implement script logic here

     await database.disconnect();
   }

   main().catch((error) => {
     console.error('Error:', error);
     process.exit(1);
   });
   ```

4. **Customize based on description:**
   - If "check" or "analyze": read-only, no dry-run needed
   - If "migrate" or "update": include dry-run, show changes preview
   - If "import": add file reading, CSV parsing if needed
   - If "backfill": include batch processing, progress tracking

5. **Add to package.json scripts** and create permission in `.claude/settings.local.json`

6. **Output to user:**
   ```
   ✓ Created: scripts/[script-name].js
   ✓ Added npm script: npm run [script-name]
   ✓ Added permission to .claude/settings.local.json

   Next steps:
   1. Edit scripts/[script-name].js
   2. Implement your logic in the main() function
   3. Test with: node scripts/[script-name].js --dry-run
   ```

## Examples

```bash
/scaffold-script checkMissingEmails "Find people without email addresses"
/scaffold-script migrateTitles "Normalize job titles to standard format"
```

## Error Handling

- If script already exists: ask whether to overwrite
- If invalid script name: suggest valid format (camelCase, no spaces)
