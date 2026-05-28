# Google Workspace Security Best Practices

## Admin Account Security

### Super Admin Requirements
- **2-5 super admins only** (1 = single point of failure, >5 = unnecessary risk)
- Dedicated admin accounts separate from daily-use accounts
- Physical security keys required (not SMS/voice)
- No email forwarding on admin accounts
- Regular review of admin roles

### Break Glass Account
- Emergency super admin with strong passphrase
- Stored securely (password manager, safe)
- Only used when all other admin access fails
- Audit usage immediately after any use

### Least Privilege
- Use delegated admin roles instead of super admin where possible
- Available roles: Groups Admin, User Management Admin, Help Desk Admin, Services Admin, etc.
- Custom roles for specific needs

```bash
# Audit admin roles
gam print admins todrive
gam print adminroles todrive
```

## Authentication & Access

### 2-Step Verification (2SV/MFA)
```bash
# Check 2SV enrollment
gam print users fields primaryEmail,isEnrolledIn2Sv,isEnforcedIn2Sv todrive

# Find non-enrolled users
gam print users query "isEnrolledIn2Sv=false" todrive
```

**Enforcement path**: Admin Console > Security > 2-Step Verification > Enforcement

**Recommended settings**:
- Enforce for all users
- Allow only security keys + authenticator apps (disable SMS/voice)
- Grace period: 1 week max for new users

### Password Policy
- Minimum 12 characters
- Enforce strong passwords
- Prevent password reuse
- Force reset for compromised passwords

```bash
# Check password strength
gam print users fields primaryEmail,agreedToTerms,lastLoginTime todrive
```

### Session Management
- Configure session length based on sensitivity
- Force re-authentication for sensitive actions
- Monitor suspicious login activity

```bash
# Login audit
gam report login start -7d todrive
gam report login event account_disabled_password_leak todrive
```

## Data Protection

### External Sharing
```bash
# Find externally shared files
gam all users print filelist query "visibility='anyoneWithLink' or visibility='anyoneCanFind'" fields id,name,owners,permissions todrive

# Find files shared with specific external domain
gam all users print filelist query "sharedwith:external.com" todrive
```

**Recommended settings** (Admin Console > Apps > Google Workspace > Drive):
- Restrict sharing outside organization OR
- Warn when sharing externally
- Block sharing with non-Google accounts
- Disable link sharing by default

### DLP (Data Loss Prevention)
- Enable DLP scanning for Drive and Gmail
- Create rules for sensitive data patterns (SSN, credit cards, PHI)
- Use labels for classification-based rules

### Client-Side Encryption (CSE)
For highest sensitivity data, enable CSE which encrypts data before it leaves the client.

## Application Security

### OAuth App Whitelisting
```bash
# Audit OAuth tokens
gam all users print tokens todrive

# Find specific app
gam all users print tokens filter "displayText=<app_name>" todrive
```

**Settings**: Admin Console > Security > API controls > App access control

- Block all third-party apps by default
- Whitelist approved apps explicitly
- Regular review of connected apps

### Less Secure Apps
- Disable access to less secure apps (apps not using OAuth)
- Admin Console > Security > Less secure apps

### Google Marketplace Apps
- Restrict installation to approved apps only
- Review permissions before approving

## Device Security

### Mobile Device Management
```bash
# Audit mobile devices
gam print mobile todrive

# Find unmanaged devices
gam print mobile query "status=APPROVED" todrive
```

**Recommended settings**:
- Require device approval
- Enforce screen lock
- Enable remote wipe capability
- Block jailbroken/rooted devices

### Chrome Device Management
```bash
# Audit Chrome devices
gam print cros allfields todrive

# Find devices with old OS
gam print cros query "osVersion lt 100" todrive
```

### Endpoint Verification
Enable endpoint verification for context-aware access decisions.

## Monitoring & Alerts

### Alert Center
Enable alerts for:
- User-granted admin privileges
- Suspicious login attempts
- Government-backed attacks
- Malware detected
- Data exfiltration attempts
- Account suspension

### Regular Audits
```bash
# Admin activity
gam report admin start -30d todrive

# Drive activity
gam report drive start -7d todrive

# Login activity
gam report login start -7d todrive

# User accounts audit
gam print users fields primaryEmail,suspended,lastLoginTime,creationTime,isEnrolledIn2Sv todrive
```

### Security Investigation Tool
Available in Enterprise editions for advanced threat investigation.

## Network & Access

### Context-Aware Access
- Restrict access based on device, location, network
- Require managed devices for sensitive apps
- Block access from high-risk countries

### SAML/SSO
- Use SAML for third-party app integration
- Enforce SSO for all apps where possible
- Regular review of SSO configurations

## Compliance

### Data Regions
- Configure data regions for compliance requirements
- Available in some Workspace editions

### Vault
- Enable Vault for eDiscovery and retention
- Set retention rules before needed
- Regular exports for compliance

### Audit Logs
- Retain logs beyond default 6 months if required
- Export to SIEM for long-term storage

## Security Checklist

### Weekly
- [ ] Review Alert Center
- [ ] Check for new admin grants
- [ ] Review suspended users
- [ ] Check 2SV enrollment

### Monthly
- [ ] Audit OAuth apps
- [ ] Review external sharing
- [ ] Check admin roles
- [ ] Review group memberships

### Quarterly
- [ ] Full security posture review
- [ ] Update password policies if needed
- [ ] Review and update DLP rules
- [ ] Test incident response procedures

## GAM Security Audit Commands

```bash
# Full security audit script
gam print users fields primaryEmail,suspended,isAdmin,lastLoginTime,isEnrolledIn2Sv,isEnforcedIn2Sv todrive
gam print admins todrive
gam print groups allfields members todrive
gam all users print tokens todrive
gam print mobile todrive
gam print cros allfields todrive
gam report admin start -90d todrive
gam report login start -30d todrive
gam report drive start -30d todrive
```
