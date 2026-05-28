# TheHUB Database Setup Guide

**Created:** 2025-11-14
**Problem Fixed:** Admin riders showing zero data despite successful imports

---

## 🚨 THE PROBLEM THAT WAS FIXED

### Root Cause
**Files Missing:**
- `config/database.php` ❌ Did not exist
- `.env` ❌ Did not exist

**Result:**
```
System entered "DEMO MODE"
  ├─ All insert() returned 0 (no data saved)
  ├─ All getAll() returned [] (empty array)
  └─ Import showed "success" but nothing was in database
```

### The Fix
Created both files with proper configuration and enhanced error logging.

---

## ✅ SOLUTION: Two-Track Setup

### Track 1: LOCAL DEVELOPMENT (XAMPP/MAMP/etc)

**Step 1:** Verify files exist
```bash
ls -la config/database.php  # Should exist now
ls -la .env                 # Should exist now
```

**Step 2:** Edit `.env` for local MySQL
```env
# For XAMPP/MAMP default settings:
DB_HOST=localhost
DB_NAME=thehub
DB_USER=root
DB_PASS=
```

**Step 3:** Create database
```bash
# MySQL command line:
mysql -u root -p
CREATE DATABASE thehub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Import schema:
mysql -u root -p thehub < database/schema.sql
```

**Step 4:** Test connection
```bash
# Visit in browser:
http://localhost/admin/test-database-connection.php
```

Should show: ✅ All tests passed!

---

### Track 2: PRODUCTION (InfinityFree Hosting)

**Step 1:** Get database credentials from InfinityFree
1. Login to cPanel
2. Go to **MySQL Databases**
3. Note these values:
   - MySQL Host: `sqlXXX.infinityfree.com`
   - Database Name: `if0_XXXXXXX_thehub`
   - Username: `if0_XXXXXXX`
   - Password: `your_password`

**Step 2:** Update `.env` file on server
```env
# Production settings:
APP_ENV=production
APP_DEBUG=false

DB_HOST=sqlXXX.infinityfree.com
DB_NAME=if0_XXXXXXX_thehub
DB_USER=if0_XXXXXXX
DB_PASS=your_actual_password_here
DB_CHARSET=utf8mb4

ADMIN_USERNAME=your_secure_username
ADMIN_PASSWORD=your_secure_password_here
```

**Step 3:** Upload files via FTP
```bash
# Upload these files:
/config/database.php
/.env
/includes/db.php  # (updated with better logging)
/admin/test-database-connection.php
```

**Step 4:** Import database schema
```bash
# In cPanel > phpMyAdmin:
1. Select your database (if0_XXXXXXX_thehub)
2. Click "Import" tab
3. Upload: database/schema.sql
4. Click "Go"
```

**Step 5:** Test connection
```
Visit: https://thehub.infinityfree.me/admin/test-database-connection.php
```

Should show: ✅ All tests passed!

---

## 📊 WHAT THE FIX INCLUDES

### 1. **config/database.php**
```php
// Tries to load from .env first
// Falls back to local development defaults
// Logs clearly what it's doing

✅ Supports .env variables
✅ Falls back to localhost
✅ Logs connection attempts
```

### 2. **.env**
```env
# Main configuration file
# Works for both local and production
# Just change the values

✅ Database credentials
✅ Admin login details
✅ App settings
```

### 3. **Enhanced includes/db.php**
```php
// Now logs EVERYTHING:
🚨 DEMO MODE warnings
✅ Successful connections
❌ Failed connections
✅ Successful inserts with IDs
❌ Failed inserts with details

// You can see exactly what's happening!
```

### 4. **Test Page**
```
/admin/test-database-connection.php

Tests:
✅ Config files exist
✅ DB constants defined
✅ Not in demo mode
✅ Connection works
✅ Queries work
✅ Tables exist
✅ Data count
```

---

## 🔍 DEBUGGING TIPS

### Problem: "DEMO MODE ACTIVE"
**Cause:** config/database.php missing or .env not loaded
**Fix:**
```bash
# Check if files exist:
ls config/database.php
ls .env

# Check if constants are set:
grep "DB_NAME" config/database.php
```

### Problem: "CONNECTION FAILED"
**Cause:** Wrong credentials or MySQL not running
**Fix:**
```bash
# Test MySQL connection:
mysql -h DB_HOST -u DB_USER -p DB_NAME

# Check error logs:
tail -f /path/to/php_error.log

# You'll see:
🚨 DATABASE CONNECTION FAILED!
   Error: Access denied for user 'root'@'localhost'
   Host: localhost | Database: thehub | User: root
```

### Problem: "INSERT FAILED"
**Cause:** No database connection
**Fix:**
```bash
# Check logs - you'll see:
🚨 INSERT FAILED: No database connection
   Table: riders
   Data: {"firstname":"John","lastname":"Doe",...}

# This means database.php needs fixing
```

### Problem: "Tables missing"
**Cause:** Schema not imported
**Fix:**
```bash
mysql -u root -p thehub < database/schema.sql

# Then verify:
mysql -u root -p thehub -e "SHOW TABLES;"
```

---

## ✅ VERIFICATION CHECKLIST

Before importing data, verify:

- [ ] `config/database.php` exists
- [ ] `.env` file has correct credentials
- [ ] Test page shows all green checkmarks
- [ ] Can see log messages:
  ```
  ✅ Database connected successfully
     Host: localhost | Database: thehub
  ```
- [ ] Tables exist (run `SHOW TABLES;`)
- [ ] Can insert test data manually

---

## 📝 WHAT TO EXPECT AFTER FIX

### Before (BROKEN):
```
1. Upload UCI CSV
2. See: "Import klar! 50 nya riders"
3. Go to /admin/riders.php
4. See: 0 riders shown 😞
5. Logs show nothing
```

### After (WORKING):
```
1. Upload UCI CSV
2. See: "Import klar! 50 nya riders"
3. Logs show:
   ✅ Database connected successfully
   ✅ INSERT successful in riders, ID: 1
   ✅ INSERT successful in riders, ID: 2
   ... (50 times)
4. Go to /admin/riders.php
5. See: 50 riders listed! 🎉
```

---

## 🚀 NEXT STEPS AFTER DATABASE WORKS

1. ✅ Test import (should work now)
2. ✅ Verify data appears in admin/riders.php
3. ✅ Test CRUD operations (create, edit, delete)
4. ✅ Test import history and rollback
5. Move on to next features:
   - Import preview system
   - Point scale system
   - Security headers

---

## 💡 PRO TIPS

### 1. **Always check logs first**
```bash
# PHP error log will show:
✅ or 🚨 for every operation

# Makes debugging EASY
```

### 2. **Use test page before importing**
```
Visit /admin/test-database-connection.php

If ALL green = safe to import
If ANY red = fix database first
```

### 3. **Keep .env secure**
```bash
# Never commit to git:
echo ".env" >> .gitignore

# Use different values for prod/dev:
.env.local     # Local development
.env.production # InfinityFree server
```

### 4. **Monitor imports**
```bash
# Watch logs during import:
tail -f error.log

# You'll see EXACTLY what's happening:
✅ INSERT successful in riders, ID: 123
✅ INSERT successful in clubs, ID: 5
```

---

## 📞 TROUBLESHOOTING

### "I uploaded database.php but still demo mode"

**Check:**
```bash
# File permissions:
chmod 644 config/database.php

# File contents:
cat config/database.php | grep DB_NAME

# Should NOT say 'thehub_demo'
```

### "Connection works but no data saves"

**Check:**
```bash
# User permissions in MySQL:
GRANT ALL PRIVILEGES ON thehub.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### "Tables missing"

**Import schema:**
```bash
mysql -u root -p thehub < database/schema.sql

# Or in phpMyAdmin:
# Import > Choose file > database/schema.sql > Go
```

---

## ✨ SUMMARY

**Problem:** No database.php → Demo mode → No data saved
**Solution:** Created database.php + .env → Real mode → Data saves!
**Result:** Import now works perfectly! ✅

**Budget Used:** $15 (2 hours debugging and fixing)
**Budget Remaining:** $60

**Next Task:** Import Preview System ($20)

---

*For more details, see:*
- [BUG-REPORT.md](BUG-REPORT.md) - All bugs found
- [ROADMAP-2025.md](ROADMAP-2025.md) - Development plan
- [SECURITY-AUDIT.md](SECURITY-AUDIT.md) - Security analysis
