---
name: Security Scanning
description: Security vulnerability scanning, dependency audits, and best practices
---

# Security Scanning Skill

## Dependency Auditing

### NPM Audit
```bash
# Check for vulnerabilities
npm audit

# Auto-fix what's possible
npm audit fix

# Force fix (may break things)
npm audit fix --force

# Generate report
npm audit --json > audit-report.json
```

### Snyk (if installed)
```bash
# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor
```

## Secret Detection

### git-secrets
```bash
# Scan for secrets in git history
git secrets --scan

# Install hooks
git secrets --install
```

### Manual Patterns to Check
```bash
# Search for hardcoded secrets
grep -rn "password\|secret\|api_key\|apikey\|token" --include="*.js" --include="*.ts" .

# Check for exposed .env files
find . -name ".env*" -not -path "./node_modules/*"
```

## Headers & HTTPS

### Security Headers Check
```bash
# Check security headers
curl -I https://smarter.poker | grep -iE "(strict-transport|x-frame|x-content|content-security|x-xss)"
```

### Required Headers
```javascript
// helmet.js for Express
const helmet = require('helmet');
app.use(helmet());

// Next.js headers
module.exports = {
  async headers() {
    return [{
      source: '/:path*',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' }
      ]
    }];
  }
};
```

## SQL Injection Prevention
```javascript
// NEVER do this
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ALWAYS use parameterized queries (Supabase does this automatically)
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('id', userId);
```

## XSS Prevention
```javascript
// Sanitize user input
import DOMPurify from 'dompurify';
const cleanHTML = DOMPurify.sanitize(dirtyHTML);

// React auto-escapes, but avoid dangerouslySetInnerHTML
```

## Environment Security
```bash
# Check .gitignore includes sensitive files
grep -E "\.env|\.pem|\.key" .gitignore

# Verify no secrets in git history
git log -p | grep -iE "(password|secret|api_key)" | head -20
```

## OWASP Top 10 Checklist
- [ ] Injection (SQL, NoSQL, OS, LDAP)
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XML External Entities (XXE)
- [ ] Broken Access Control
- [ ] Security Misconfiguration
- [ ] Cross-Site Scripting (XSS)
- [ ] Insecure Deserialization
- [ ] Using Components with Known Vulnerabilities
- [ ] Insufficient Logging & Monitoring
