---
name: auth-check
description: Check authentication setup, user management, and run auth-related diagnostics
allowed-tools: [Bash, Read]
---

## Purpose
Diagnose and verify authentication setup, check user accounts, roles, and run authentication-related utilities.

## Available Commands

### 1. Check Authentication Setup
```bash
# Comprehensive auth check
npm run check:auth

# Checks:
# - Users table structure
# - Existing users and their roles
# - Password hashes validity
# - Session configuration
```

### 2. Check Database
```bash
# Verify database schema and data
npm run check:db

# Shows:
# - All tables and their structure
# - Row counts for each table
# - Sample data from key tables
```

### 3. Make User Admin
```bash
# Promote user to admin by email
npm run make:admin

# Interactive prompt for email address
# Updates user role to 'admin'
```

### 4. User Management

**Check specific user:**
```bash
# Run check:auth and look for user in output
npm run check:auth
```

**Delete user by email:**
```bash
# WARNING: Destructive operation
npm run delete:user

# Deletes:
# - User account
# - All associated data
# - Review history
# - Progress tracking
```

**Diagnose user paths:**
```bash
# Check user's learning paths and progress
tsx tools/diagnose-user-paths.ts

# Shows:
# - Assigned paths
# - Progress on each path
# - Available lessons
```

### 5. Check User Progress
```bash
# View detailed progress for a user
tsx tools/check-user-progress.ts

# Displays:
# - XP and level
# - Completed lessons
# - Current streak
# - Hearts remaining
```

### 6. XP Statistics
```bash
# Check XP stats across users
npm run check:xp-stats

# Shows:
# - Total XP per user
# - XP history
# - Lifetime XP tracking
```

### 7. Create Sample Users
```bash
# Populate with sample users and data
npm run populate:sample

# Creates:
# - Test users (user, admin, teacher)
# - Sample domains and categories
# - Flashcards and progress
```

## Migration Scripts

### Authentication Migration
```bash
# Migrate to NextAuth schema
npm run migrate:auth

# Adds:
# - Users table
# - Accounts table
# - Sessions table
# - Verification tokens
```

### Role Migration
```bash
# Add roles to users
npm run migrate:roles

# Adds role column and sets defaults
```

### Groups Migration
```bash
# Set up group functionality
npm run migrate:groups

# Creates:
# - Groups table
# - Group members table
# - Group paths table
```

## Common Tasks

### Create Admin User
```bash
# 1. Check existing users
npm run check:auth

# 2. If user exists, promote them
npm run make:admin
# Enter their email when prompted

# 3. If user doesn't exist, create via UI first
# Then run make:admin
```

### Debug Login Issues
```bash
# 1. Check auth setup
npm run check:auth

# 2. Verify environment variables
cat .env.local | grep NEXTAUTH

# Required variables:
# NEXTAUTH_SECRET=<random-string>
# NEXTAUTH_URL=http://localhost:3000
# DATABASE_URL=data/learning-cards.db

# 3. Check user exists and has password
npm run check:auth
```

### Reset User Password
```bash
# Currently requires manual database update
# or user to request password reset via UI

# Via database (advanced):
tsx -e "
import { getDb } from './src/lib/db';
import bcrypt from 'bcryptjs';

const db = getDb();
const hash = bcrypt.hashSync('newpassword', 10);
db.prepare('UPDATE users SET password_hash = ? WHERE email = ?')
  .run(hash, 'user@example.com');
console.log('Password updated');
"
```

### Check Session Status
```bash
# Sessions are stored in database
# Check active sessions:
sqlite3 data/learning-cards.db "SELECT * FROM sessions WHERE expires > datetime('now');"
```

### Verify RBAC Permissions
```bash
# Check user permissions in code:
# File: src/lib/rbac.ts

# Test permission:
tsx -e "
import { hasPermission } from './src/lib/rbac';
console.log('Teacher can create:', hasPermission('teacher', 'flashcard:create'));
console.log('User can delete:', hasPermission('user', 'flashcard:delete'));
"
```

## Environment Setup

Required .env.local variables:
```bash
# Database
DATABASE_URL=data/learning-cards.db

# NextAuth
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
NEXTAUTH_URL=http://localhost:3000

# Optional: Email (Mailgun/Resend)
MAILGUN_API_KEY=your-key
MAILGUN_DOMAIN=your-domain
# OR
RESEND_API_KEY=your-key
```

Generate NEXTAUTH_SECRET:
```bash
openssl rand -base64 32
```

## Troubleshooting

### "User not found" error
```bash
# 1. Check if user exists
npm run check:auth

# 2. Create user via signup UI

# 3. Verify email is correct (case-sensitive)
```

### "Invalid credentials" error
```bash
# 1. Verify password hash exists
npm run check:auth

# 2. Check bcrypt is working:
tsx -e "
import bcrypt from 'bcryptjs';
const hash = bcrypt.hashSync('test', 10);
console.log('Hash:', hash);
console.log('Verify:', bcrypt.compareSync('test', hash));
"
```

### "Unauthorized" in API routes
```bash
# 1. Check session is valid
# Open browser dev tools > Application > Cookies
# Look for next-auth.session-token

# 2. Verify authOptions in API route
# File: src/app/api/auth/[...nextauth]/route.ts

# 3. Check getServerSession is called correctly
```

### Role permissions not working
```bash
# 1. Check user role
npm run check:auth

# 2. Verify RBAC configuration
cat src/lib/rbac.ts

# 3. Check hasPermission calls in code
```

## Best Practices
- ✅ Always verify user exists before operations
- ✅ Check roles and permissions before access
- ✅ Use migration scripts for schema changes
- ✅ Keep NEXTAUTH_SECRET secure
- ✅ Test authentication after migrations
- ⚠️ Never commit credentials to git
- ⚠️ Backup database before user deletions
- ⚠️ Use strong passwords for admin accounts
