# zmprov Command Reference

Complete reference for Zimbra provisioning commands.

## Command Syntax

```bash
zmprov [options] <command> [arguments]
```

### Common Options

| Option | Description |
|--------|-------------|
| `-l` | LDAP mode (bypasses memcached, required for large searches) |
| `-v` | Verbose output |
| `-d` | Debug output |
| `-s` | Server to connect to |
| `-a` | Account to auth as (admin) |
| `-p` | Password |

## Account Commands

### Create Account (ca)

```bash
zmprov ca <email> <password> [attribute value ...]
```

Common attributes for creation:
- `displayName` - Full name
- `givenName` - First name
- `sn` - Surname
- `zimbraCOSid` - Class of Service ID
- `zimbraMailQuota` - Quota in bytes
- `zimbraAccountStatus` - Initial status (active/locked)

### Delete Account (da)

```bash
zmprov da <email>
```

### Get Account (ga)

```bash
# All attributes
zmprov ga <email>

# Specific attribute
zmprov ga <email> <attribute>
```

### Modify Account (ma)

```bash
# Set attribute
zmprov ma <email> <attribute> <value>

# Add to multi-value
zmprov ma <email> +<attribute> <value>

# Remove from multi-value
zmprov ma <email> -<attribute> <value>

# Clear attribute
zmprov ma <email> <attribute> ""
```

### Get All Accounts (gaa)

```bash
# All accounts
zmprov -l gaa

# In domain
zmprov -l gaa <domain>
```

### Search Accounts (sa)

```bash
# LDAP filter
zmprov -l sa "<ldap-filter>"

# Examples
zmprov -l sa "(&(objectClass=zimbraAccount)(zimbraAccountStatus=active))"
zmprov -l sa "(mail=*@domain.com)"
zmprov -l sa "(&(sn=Smith)(zimbraAccountStatus=active))"
```

### Rename Account (ra)

```bash
zmprov ra <old-email> <new-email>
```

### Add Account Alias (aaa)

```bash
zmprov aaa <email> <alias>
```

### Remove Account Alias (raa)

```bash
zmprov raa <email> <alias>
```

### Get Account Membership (gam)

```bash
# Lists distribution lists account belongs to
zmprov gam <email>
```

## Domain Commands

### Create Domain (cd)

```bash
zmprov cd <domain> [attribute value ...]
```

### Delete Domain (dd)

```bash
zmprov dd <domain>
```

### Get Domain (gd)

```bash
zmprov gd <domain> [attribute]
```

### Modify Domain (md)

```bash
zmprov md <domain> <attribute> <value>
```

### Get All Domains (gad)

```bash
zmprov gad
```

### Count Account (cta)

```bash
# Count accounts in domain
zmprov cta <domain>
```

## COS Commands

### Create COS (cc)

```bash
zmprov cc <name> [attribute value ...]
```

### Delete COS (dc)

```bash
zmprov dc <name-or-id>
```

### Get COS (gc)

```bash
zmprov gc <name-or-id> [attribute]
```

### Modify COS (mc)

```bash
zmprov mc <name-or-id> <attribute> <value>
```

### Get All COS (gac)

```bash
zmprov gac
```

### Copy COS (cpc)

```bash
zmprov cpc <src-cos> <dest-cos>
```

## Server Commands

### Get Server (gs)

```bash
zmprov gs <server> [attribute]
```

### Modify Server (ms)

```bash
zmprov ms <server> <attribute> <value>
```

### Get All Servers (gas)

```bash
zmprov gas
```

## Distribution List Commands

### Create Distribution List (cdl)

```bash
zmprov cdl <email> [attribute value ...]
```

### Delete Distribution List (ddl)

```bash
zmprov ddl <email>
```

### Get Distribution List (gdl)

```bash
zmprov gdl <email>
```

### Add Distribution List Member (adlm)

```bash
zmprov adlm <dl-email> <member-email>
```

### Remove Distribution List Member (rdlm)

```bash
zmprov rdlm <dl-email> <member-email>
```

### Get Distribution List Membership (gdlm)

```bash
# Lists members of DL
zmprov gdlm <dl-email>
```

## Global Config Commands

### Get All Config (gacf)

```bash
zmprov gacf [attribute]
```

### Modify Config (mcf)

```bash
zmprov mcf <attribute> <value>
```

## Describe Commands

### Describe Attributes (desc)

```bash
# Describe account attributes
zmprov desc -a account

# Describe domain attributes
zmprov desc -a domain

# Describe server attributes
zmprov desc -a server

# Describe COS attributes
zmprov desc -a cos

# Search for specific attribute
zmprov desc -a account | grep -i quota
```

## Mailbox Commands

### Get Mailbox (gm)

```bash
zmprov gm <email>
```

### Get Mailbox Size (gms)

```bash
zmprov gms <email>
```

## Auth Commands

### Create Auth Token (gat)

```bash
# Generate auth token for account
zmprov gat <email>
```

### Check Password Strength (cps)

```bash
zmprov cps <email> <password>
```

## Flush Commands

### Flush Cache (fc)

```bash
# Flush all caches
zmprov fc all

# Flush specific cache
zmprov fc account
zmprov fc domain
zmprov fc server
zmprov fc cos
zmprov fc config
```

## Rights Commands

### Get Effective Rights (ger)

```bash
zmprov ger <target-type> <target> <grantee-type> <grantee>
```

### Grant Right (grr)

```bash
zmprov grr <target-type> <target> <grantee-type> <grantee> <right>
```

### Revoke Right (rvr)

```bash
zmprov rvr <target-type> <target> <grantee-type> <grantee> <right>
```

## Useful Combinations

### Bulk Operations

```bash
# Set attribute for all users in domain
for user in $(zmprov -l gaa domain.com); do
  zmprov ma $user zimbraMailQuota 2147483648
done

# Export all accounts with attributes
zmprov -l gaa | while read account; do
  echo "=== $account ===" >> accounts.txt
  zmprov ga $account >> accounts.txt
done
```

### Query Examples

```bash
# Find locked accounts
zmprov -l sa "(zimbraAccountStatus=locked)"

# Find accounts over quota
zmprov -l gaa | while read account; do
  used=$(zmprov gm $account | grep zimbraMailUsed | awk '{print $2}')
  quota=$(zmprov ga $account zimbraMailQuota | grep zimbraMailQuota | awk '{print $2}')
  if [ "$used" -gt "$quota" ] && [ "$quota" -gt 0 ]; then
    echo "$account: $used / $quota"
  fi
done

# Find accounts without COS
zmprov -l sa "(&(objectClass=zimbraAccount)(!(zimbraCOSid=*)))"
```
