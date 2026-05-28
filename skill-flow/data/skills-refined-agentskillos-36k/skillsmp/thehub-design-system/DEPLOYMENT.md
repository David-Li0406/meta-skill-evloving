# Deployment Guide - TheHUB

Complete deployment instructions for TheHUB v2.0.0.

## Pre-Deployment Checklist

### Requirements
- [ ] PHP 8.0 or higher
- [ ] MySQL 5.7 or higher / MariaDB 10.3 or higher
- [ ] Apache/Nginx web server
- [ ] mod_rewrite enabled (Apache) or equivalent (Nginx)
- [ ] PHP extensions: mysqli, mbstring, json, fileinfo
- [ ] Minimum 50MB disk space
- [ ] Minimum 128MB PHP memory_limit

### Pre-Deployment Tasks
- [ ] Backup existing database
- [ ] Backup existing files
- [ ] Review `CHANGELOG.md` for breaking changes
- [ ] Test in staging environment first
- [ ] Verify PHP version compatibility
- [ ] Check database user permissions

---

## Deployment Steps

### 1. Prepare Database

#### 1.1 Run Database Migrations

Execute the following SQL migrations in order:

```bash
# If using MySQL command line:
mysql -u username -p database_name < database/migrations/003_import_history.sql
```

Or manually execute the SQL:

```sql
-- Create import history tables
SOURCE /path/to/TheHUB/database/migrations/003_import_history.sql;
```

#### 1.2 Verify Tables Created

```sql
-- Verify import_history table
DESCRIBE import_history;

-- Verify import_records table
DESCRIBE import_records;

-- Check all tables exist
SHOW TABLES;
```

Expected tables:
- admin_users
- categories
- clubs
- events
- import_history ✨ NEW
- import_records ✨ NEW
- riders (formerly cyclists)
- results
- series

#### 1.3 Table Name Migration (If Needed)

If your database still has `cyclists` table instead of `riders`:

```sql
-- Rename table
RENAME TABLE cyclists TO riders;

-- Update any foreign keys if needed
-- (Check your specific schema)
```

---

### 2. Deploy Files

#### 2.1 Upload Files

Upload all files to your web server, preserving directory structure:

```bash
# Using rsync (recommended):
rsync -avz --exclude='.git' /local/TheHUB/ user@server:/var/www/html/TheHUB/

# Using FTP:
# Upload entire TheHUB directory to your web root
```

#### 2.2 Set File Permissions

```bash
# Set directory permissions
find /var/www/html/TheHUB -type d -exec chmod 755 {} \;

# Set file permissions
find /var/www/html/TheHUB -type f -exec chmod 644 {} \;

# Make uploads directory writable
chmod 775 /var/www/html/TheHUB/uploads
chown www-data:www-data /var/www/html/TheHUB/uploads

# Protect sensitive files
chmod 600 /var/www/html/TheHUB/config.php
```

#### 2.3 Configure Environment

Edit `config.php` with your production settings:

```php
<?php
// Database Configuration
define('DB_HOST', 'your_db_host');
define('DB_NAME', 'your_db_name');
define('DB_USER', 'your_db_user');
define('DB_PASS', 'your_db_password');

// Security
define('SESSION_LIFETIME', 86400); // 24 hours
ini_set('session.cookie_secure', '1'); // HTTPS only
ini_set('session.cookie_httponly', '1');
ini_set('session.cookie_samesite', 'Strict');

// Uploads
define('UPLOADS_PATH', __DIR__ . '/uploads');
define('MAX_UPLOAD_SIZE', 10485760); // 10MB

// Admin Credentials (change these!)
define('DEFAULT_ADMIN_USERNAME', 'admin');
define('DEFAULT_ADMIN_PASSWORD', password_hash('your_strong_password', PASSWORD_DEFAULT));
```

**IMPORTANT**: Change default admin credentials!

---

### 3. Web Server Configuration

#### 3.1 Apache Configuration

Create/update `.htaccess` in TheHUB root:

```apache
# Enable rewrite engine
RewriteEngine On

# Force HTTPS (recommended for production)
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Protect sensitive files
<FilesMatch "^(config\.php|\.git|composer\.(json|lock)|package(-lock)?\.json)">
    Require all denied
</FilesMatch>

# Protect database directory
<IfModule mod_authz_core.c>
    <Directory "database">
        Require all denied
    </Directory>
</IfModule>

# Set default charset
AddDefaultCharset UTF-8

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Browser caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

#### 3.2 Nginx Configuration

Add to your Nginx server block:

```nginx
server {
    listen 80;
    server_name thehub.example.com;
    root /var/www/html/TheHUB;
    index index.php;

    # Force HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name thehub.example.com;
    root /var/www/html/TheHUB;
    index index.php;

    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # PHP Processing
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # Protect sensitive files
    location ~ /(config\.php|database/|\.git) {
        deny all;
        return 404;
    }

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

---

### 4. Post-Deployment Verification

#### 4.1 Access Website

1. Navigate to `https://your-domain.com`
2. Verify landing page loads correctly
3. Check that all links work

#### 4.2 Test Admin Login

1. Go to `https://your-domain.com/admin/login.php`
2. Login with admin credentials
3. Verify dashboard loads

#### 4.3 Test CRUD Operations

For each entity (Events, Series, Riders, Clubs, Venues, Results):
- [ ] Create a test record
- [ ] Edit the test record
- [ ] Verify list view shows the record
- [ ] Delete the test record
- [ ] Verify deletion worked

#### 4.4 Test Import System

1. Go to `https://your-domain.com/admin/import-uci.php`
2. Upload a small test CSV file
3. Verify import completes successfully
4. Check `https://your-domain.com/admin/import-history.php`
5. Test rollback on the import
6. Verify rollback worked

#### 4.5 Security Checks

- [ ] HTTPS is enforced
- [ ] config.php is not accessible via browser
- [ ] database/ directory is not accessible
- [ ] CSRF protection working (try submitting form without token)
- [ ] Session timeout working
- [ ] Admin pages require authentication

---

### 5. Performance Optimization

#### 5.1 Enable OpCache (PHP)

Edit `php.ini`:

```ini
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=4000
opcache.revalidate_freq=60
```

#### 5.2 Database Optimization

```sql
-- Analyze tables
ANALYZE TABLE events, riders, results, clubs, series, import_history, import_records;

-- Optimize tables
OPTIMIZE TABLE events, riders, results, clubs, series;
```

#### 5.3 Enable Compression

Ensure gzip/deflate compression is enabled in your web server (see configuration above).

---

### 6. Monitoring & Maintenance

#### 6.1 Set Up Monitoring

Monitor these metrics:
- Disk space usage (uploads directory)
- Database size
- PHP error logs
- Web server error logs
- Import history growth

#### 6.2 Backup Strategy

**Daily Backups**:
```bash
#!/bin/bash
# Daily backup script

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/thehub"

# Database backup
mysqldump -u username -p'password' database_name > $BACKUP_DIR/db_$DATE.sql

# Files backup
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /var/www/html/TheHUB/uploads

# Keep only last 30 days
find $BACKUP_DIR -type f -mtime +30 -delete
```

**Add to crontab**:
```bash
0 2 * * * /path/to/backup-script.sh
```

#### 6.3 Import History Cleanup

Optionally clean old import history (keep last 90 days):

```sql
-- Delete import records older than 90 days
DELETE ir FROM import_records ir
JOIN import_history ih ON ir.import_id = ih.id
WHERE ih.imported_at < DATE_SUB(NOW(), INTERVAL 90 DAY);

-- Delete import history older than 90 days
DELETE FROM import_history
WHERE imported_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

Add to monthly cron job:
```bash
0 3 1 * * mysql -u username -p'password' database_name < /path/to/cleanup.sql
```

---

### 7. Troubleshooting

#### 7.1 Common Issues

**Issue**: Blank white page
- **Solution**: Check PHP error logs, enable display_errors temporarily
- **Location**: `/var/log/php/error.log` or `/var/log/apache2/error.log`

**Issue**: Database connection failed
- **Solution**: Verify credentials in `config.php`, check database server is running
- **Test**: `mysql -u username -p -h hostname database_name`

**Issue**: Permissions errors on file upload
- **Solution**: `chmod 775 uploads/ && chown www-data:www-data uploads/`

**Issue**: CSRF token errors
- **Solution**: Check session is working, verify session cookie settings

**Issue**: Import history not working
- **Solution**: Verify `003_import_history.sql` migration ran successfully

#### 7.2 Enable Debug Mode

Temporarily enable debug mode in `config.php`:

```php
// FOR DEBUGGING ONLY - DISABLE IN PRODUCTION
define('DEBUG', true);
ini_set('display_errors', '1');
error_reporting(E_ALL);
```

**IMPORTANT**: Disable debug mode after troubleshooting!

---

### 8. Rollback Procedure

If deployment fails, follow these steps:

#### 8.1 Rollback Files

```bash
# Restore from backup
rsync -avz /backups/thehub/files_backup/ /var/www/html/TheHUB/
```

#### 8.2 Rollback Database

```bash
# Restore database
mysql -u username -p database_name < /backups/thehub/db_backup.sql
```

#### 8.3 Verify Rollback

- [ ] Website loads correctly
- [ ] Admin login works
- [ ] No errors in logs

---

### 9. Security Hardening

#### 9.1 SSL/TLS Configuration

Use Let's Encrypt for free SSL:

```bash
# Install certbot
apt-get install certbot python3-certbot-apache

# Get certificate
certbot --apache -d thehub.example.com

# Auto-renewal
certbot renew --dry-run
```

#### 9.2 Additional Security Measures

- [ ] Change default admin password
- [ ] Disable directory listing
- [ ] Enable fail2ban for failed login attempts
- [ ] Set up firewall rules (only allow 80, 443, SSH)
- [ ] Regular security updates (`apt-get update && apt-get upgrade`)
- [ ] Monitor access logs for suspicious activity

#### 9.3 Content Security Policy

Add to your web server configuration:

```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://unpkg.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;
```

---

### 10. Post-Deployment Tasks

#### 10.1 User Communication

- [ ] Notify users of new features
- [ ] Provide training on new CRUD operations
- [ ] Share import history documentation
- [ ] Update internal documentation

#### 10.2 Monitoring Setup

- [ ] Set up uptime monitoring (e.g., UptimeRobot)
- [ ] Configure error alerting
- [ ] Set up performance monitoring
- [ ] Create dashboard for system health

#### 10.3 First Week Checks

- Day 1: Check error logs, verify all features working
- Day 3: Monitor database growth, check import history
- Day 7: Review user feedback, address any issues

---

## Deployment Checklist

Use this checklist during deployment:

### Pre-Deployment
- [ ] Backup database
- [ ] Backup files
- [ ] Test in staging
- [ ] Review CHANGELOG.md
- [ ] Verify requirements

### Deployment
- [ ] Run database migrations
- [ ] Upload files
- [ ] Set permissions
- [ ] Configure config.php
- [ ] Configure web server
- [ ] Test HTTPS

### Verification
- [ ] Website loads
- [ ] Admin login works
- [ ] All CRUD operations tested
- [ ] Import system tested
- [ ] Import history tested
- [ ] Security checks passed

### Post-Deployment
- [ ] Enable monitoring
- [ ] Set up backups
- [ ] Document any custom configurations
- [ ] Notify users
- [ ] Monitor first 24 hours

---

## Support

For issues during deployment:

1. Check `TEST-RESULTS.md` for known issues
2. Review error logs
3. Verify all migration scripts ran successfully
4. Check file permissions
5. Verify database connections

---

## Success Criteria

Deployment is successful when:
- ✅ All pages load without errors
- ✅ Admin authentication works
- ✅ All CRUD operations functional
- ✅ Import system working with history tracking
- ✅ No errors in logs
- ✅ Security measures in place
- ✅ Backups configured

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Version**: 2.0.0
**Status**: _______________

---

*For change history, see `CHANGELOG.md`*
*For test results, see `TEST-RESULTS.md`*
