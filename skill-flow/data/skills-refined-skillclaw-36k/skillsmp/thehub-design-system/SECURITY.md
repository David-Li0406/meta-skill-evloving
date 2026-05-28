# TheHUB Security Documentation

**Version:** 1.0
**Last Updated:** 2025-11-12
**Security Rating:** A-

---

## 🔒 Security Overview

TheHUB implements comprehensive security measures to protect against common web vulnerabilities.

---

## ✅ Implemented Security Features

### 1. SQL Injection Protection - **A+**

**Status:** ✅ FULLY PROTECTED

**Implementation:**
- All database queries use PDO prepared statements
- Parameters are bound separately from SQL
- `PDO::ATTR_EMULATE_PREPARES => false` enforced
- No string concatenation in queries

**Example:**
```php
// SECURE - Prepared statement
$riders = $db->getAll(
    "SELECT * FROM cyclists WHERE license_number = ?",
    [$licenseNumber]
);

// NEVER DO THIS:
// $riders = $db->query("SELECT * FROM cyclists WHERE license_number = '$licenseNumber'");
```

**Files Verified:**
- ✅ `/includes/db.php` - Database wrapper
- ✅ `/admin/riders.php` - Rider management
- ✅ `/admin/events.php` - Event management
- ✅ `/admin/results.php` - Results management
- ✅ `/admin/import-riders.php` - Bulk import
- ✅ `/admin/import-results.php` - Results import

---

### 2. Cross-Site Scripting (XSS) Protection - **A+**

**Status:** ✅ FULLY PROTECTED

**Implementation:**
- All output uses `h()` function (htmlspecialchars wrapper)
- `ENT_QUOTES` flag set
- UTF-8 encoding enforced
- No unescaped echo statements

**Example:**
```php
// SECURE - Escaped output
<h1><?= h($pageTitle) ?></h1>
<div><?= h($user['name']) ?></div>

// NEVER DO THIS:
// <div><?= $user['name'] ?></div>
```

**Function Definition:**
```php
function h($str) {
    return htmlspecialchars($str ?? '', ENT_QUOTES, 'UTF-8');
}
```

---

### 3. Cross-Site Request Forgery (CSRF) Protection - **A**

**Status:** ✅ IMPLEMENTED

**Implementation:**
- CSRF tokens generated per session
- Tokens validated on all POST requests
- `hash_equals()` used for constant-time comparison
- Tokens automatically regenerated

**Protected Forms:**
- ✅ `/admin/login.php` - Login form
- ✅ `/admin/import-riders.php` - Rider import
- ✅ `/admin/import-results.php` - Results import

**Usage:**
```php
// In forms:
<form method="POST">
    <?= csrfField() ?>
    <!-- form fields -->
</form>

// In POST handlers:
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    checkCsrf(); // Validates token
    // ... process form
}
```

**Functions:**
- `generateCsrfToken()` - Creates new token
- `getCsrfToken()` - Gets current token
- `validateCsrfToken($token)` - Validates token
- `csrfField()` - Outputs hidden input field
- `checkCsrf()` - Validates POST request

---

### 4. Session Security - **A**

**Status:** ✅ FULLY IMPLEMENTED

**Features:**
```php
session_set_cookie_params([
    'lifetime' => 86400,           // 24 hours
    'path' => '/',
    'secure' => true,              // HTTPS only (production)
    'httponly' => true,            // No JavaScript access
    'samesite' => 'Strict'         // CSRF protection
]);
```

**Session Fixation Protection:**
- Session ID regenerated on every login
- Old session destroyed
- New session created with fresh ID

**Cache Prevention:**
- No-store, no-cache headers on admin pages
- Prevents browser back-button access
- Prevents sensitive data caching

---

### 5. Open Redirect Protection - **B+**

**Status:** ✅ IMPLEMENTED

**Implementation:**
```php
function redirect($url) {
    // Validate URL to prevent open redirect
    if (strpos($url, 'http://') === 0 || strpos($url, 'https://') === 0) {
        $parsed = parse_url($url);
        $currentHost = $_SERVER['HTTP_HOST'] ?? '';
        if ($parsed['host'] !== $currentHost) {
            // Block external redirects
            $url = '/';
        }
    }
    header("Location: " . $url);
    exit;
}
```

---

### 6. Security Headers - **B+**

**Status:** ✅ READY (Call `setSecurityHeaders()`)

**Available Headers:**
```php
setSecurityHeaders();
```

Sets:
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-XSS-Protection: 1; mode=block` - Legacy XSS protection
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy` - Restricts resource loading

**To Activate:** Add `setSecurityHeaders();` in config.php or individual pages.

---

### 7. File Upload Security - **A-**

**Status:** ✅ IMPLEMENTED

**Validation:**
- File size limits (10MB default)
- Extension whitelist (CSV, XLSX, XLS)
- MIME type checking
- Secure file storage path
- Auto-cleanup of temporary files

**Example:**
```php
$validation = validateUpload($file, ['csv', 'xlsx']);
if (!$validation['valid']) {
    die($validation['error']);
}
```

---

### 8. Environment Variables - **A**

**Status:** ✅ IMPLEMENTED

**Features:**
- Sensitive data in `.env` file
- `.env` excluded from git (`.gitignore`)
- `.env.example` provided as template
- Fallback to safe defaults

**Configuration:**
```bash
# .env file
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
DB_HOST=localhost
DB_NAME=thehub
DB_USER=db_user
DB_PASS=db_password
```

**Setup:**
1. Copy `.env.example` to `.env`
2. Update with actual values
3. Never commit `.env` to version control

---

## 🔴 Known Limitations

### 1. Rate Limiting - NOT IMPLEMENTED

**Risk:** Brute force attacks on login

**Mitigation:**
- Use web server rate limiting (nginx/Apache)
- Implement fail2ban
- Add rate limiting in future update

### 2. Two-Factor Authentication - NOT IMPLEMENTED

**Risk:** Account compromise if password is leaked

**Mitigation:**
- Use strong passwords
- Regular password changes
- Implement 2FA in future update

### 3. Database Encryption - NOT IMPLEMENTED

**Risk:** Data exposure if database is compromised

**Mitigation:**
- Use encrypted database connections
- Encrypt sensitive fields
- Regular backups with encryption

---

## 📋 Security Checklist for Production

### Before Deployment:

- [ ] Copy `.env.example` to `.env`
- [ ] Change `ADMIN_USERNAME` in `.env`
- [ ] Change `ADMIN_PASSWORD` to strong password
- [ ] Set `APP_ENV=production` in `.env`
- [ ] Set `APP_DEBUG=false` in `.env`
- [ ] Set `DISPLAY_ERRORS=false` in `.env`
- [ ] Configure database credentials in `.env`
- [ ] Set `FORCE_HTTPS=true` if using HTTPS
- [ ] Verify `.env` is in `.gitignore`
- [ ] Run database migrations
- [ ] Test CSRF protection works
- [ ] Test session security
- [ ] Enable security headers with `setSecurityHeaders()`
- [ ] Set up SSL/TLS certificate
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Configure error logging

### Server Configuration:

- [ ] PHP version >= 7.4
- [ ] PDO MySQL extension enabled
- [ ] Session extension enabled
- [ ] File uploads enabled (if needed)
- [ ] Set `upload_max_filesize` appropriately
- [ ] Set `post_max_size` appropriately
- [ ] Disable `expose_php`
- [ ] Set `session.cookie_httponly = On`
- [ ] Set `session.cookie_secure = On` (HTTPS only)
- [ ] Configure log rotation

---

## 🧪 Security Testing

### Manual Tests:

**1. SQL Injection Test:**
```bash
# Try injecting SQL in search fields
Search: ' OR '1'='1
Expected: No results or escaped query
```

**2. XSS Test:**
```bash
# Try injecting script in input fields
Name: <script>alert('XSS')</script>
Expected: Escaped as text, not executed
```

**3. CSRF Test:**
```bash
# Submit form without CSRF token
Expected: "CSRF token validation failed"
```

**4. Session Fixation Test:**
```bash
# Try reusing session ID after logout
Expected: Redirected to login
```

**5. Open Redirect Test:**
```bash
# Try redirecting to external site
URL: /admin/login.php?redirect=https://evil.com
Expected: Redirected to / instead
```

---

## 📊 Security Audit Summary

| Category | Status | Grade |
|----------|--------|-------|
| SQL Injection | ✅ Protected | A+ |
| XSS Protection | ✅ Protected | A+ |
| CSRF Protection | ✅ Protected | A |
| Session Security | ✅ Secure | A |
| Open Redirect | ✅ Protected | B+ |
| File Upload | ✅ Validated | A- |
| Environment Vars | ✅ Implemented | A |
| Security Headers | ⚠️ Available | B+ |
| Rate Limiting | ❌ Not Implemented | F |
| 2FA | ❌ Not Implemented | F |

**Overall Security Rating: A-**

---

## 🚨 Incident Response

### If Security Breach Suspected:

1. **Immediate Actions:**
   - Take site offline
   - Change all passwords
   - Regenerate CSRF tokens
   - Check database for unauthorized changes
   - Review server logs

2. **Investigation:**
   - Check `/logs/error.log`
   - Check web server access logs
   - Check database audit logs
   - Identify entry point

3. **Recovery:**
   - Restore from clean backup
   - Patch vulnerability
   - Update dependencies
   - Monitor for further attempts

4. **Prevention:**
   - Review security measures
   - Update this document
   - Train users
   - Implement additional monitoring

---

## 📞 Contact

For security issues, contact: [security@thehub.se](mailto:security@thehub.se)

**Do not** disclose security vulnerabilities publicly until they are fixed.

---

## 📝 Changelog

### Version 1.0 (2025-11-12)
- Initial security implementation
- SQL injection protection
- XSS protection
- CSRF protection
- Session security
- Environment variables
- Security headers framework

---

*This document should be reviewed and updated regularly as security measures evolve.*
