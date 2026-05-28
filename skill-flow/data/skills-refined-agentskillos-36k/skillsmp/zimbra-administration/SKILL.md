---
name: Zimbra Administration
description: This skill should be used when the user asks about "zmprov commands", "zmcontrol", "Zimbra users", "domain management", "Zimbra server configuration", "create mailbox", "delete account", "Zimbra COS", "class of service", "Zimbra LDAP attributes", or mentions managing Zimbra servers. Provides comprehensive administration guidance for Zimbra 8.x, 9.x, and 10.x.
version: 1.0.0
---

# Zimbra Administration

Comprehensive guide for Zimbra server administration covering user management, domain configuration, server settings, and common administrative tasks.

## Core Concepts

### Zimbra Architecture

Zimbra Collaboration Suite consists of several components:

- **mailboxd** - Java application server handling mail storage, IMAP, POP, CalDAV
- **MTA** - Postfix mail transfer agent for SMTP
- **LDAP** - OpenLDAP directory for configuration and authentication
- **proxy** - nginx reverse proxy for HTTP/HTTPS/IMAP/POP
- **memcached** - Session caching
- **convertd** - Document conversion service

### Command-Line Tools

Primary administration tools (run as `zimbra` user):

| Tool | Purpose |
|------|---------|
| `zmprov` | Provisioning - users, domains, COS, server config |
| `zmcontrol` | Service management - start, stop, status |
| `zmmailbox` | Mailbox operations - folders, messages, search |
| `zmcertmgr` | Certificate management |
| `zmlocalconfig` | Local server configuration |
| `zmsoap` | SOAP API command-line interface |

## User Management

### Create User Account

```bash
# Basic account creation
zmprov ca user@domain.com password

# With display name
zmprov ca user@domain.com password displayName "John Doe"

# With COS assignment
zmprov ca user@domain.com password zimbraCOSid <cos-id>

# With multiple attributes
zmprov ca user@domain.com password \
  displayName "John Doe" \
  givenName "John" \
  sn "Doe" \
  zimbraMailQuota 1073741824
```

### Modify User Attributes

```bash
# Set single attribute
zmprov ma user@domain.com zimbraMailQuota 2147483648

# Set multiple attributes
zmprov ma user@domain.com \
  zimbraMailQuota 2147483648 \
  zimbraFeatureCalendarEnabled TRUE

# Add to multi-value attribute
zmprov ma user@domain.com +zimbraMailAlias alias@domain.com

# Remove from multi-value attribute
zmprov ma user@domain.com -zimbraMailAlias alias@domain.com
```

### Query User Information

```bash
# Get all attributes
zmprov ga user@domain.com

# Get specific attribute
zmprov ga user@domain.com zimbraMailQuota

# Search accounts
zmprov -l sa "(&(objectClass=zimbraAccount)(zimbraAccountStatus=active))"

# List all accounts in domain
zmprov -l gaa domain.com
```

### Account Status Management

```bash
# Lock account
zmprov ma user@domain.com zimbraAccountStatus locked

# Close account (no login, mail bounced)
zmprov ma user@domain.com zimbraAccountStatus closed

# Maintenance mode
zmprov ma user@domain.com zimbraAccountStatus maintenance

# Reactivate
zmprov ma user@domain.com zimbraAccountStatus active

# Delete account
zmprov da user@domain.com
```

## Domain Management

### Create Domain

```bash
# Basic domain
zmprov cd domain.com

# With settings
zmprov cd domain.com \
  zimbraPublicServiceHostname mail.domain.com \
  zimbraPublicServiceProtocol https \
  zimbraPublicServicePort 443
```

### Domain Settings

```bash
# Get domain info
zmprov gd domain.com

# Modify domain
zmprov md domain.com zimbraMailDomainQuota 10737418240

# Set default COS for domain
zmprov md domain.com zimbraDomainDefaultCOSId <cos-id>

# Delete domain
zmprov dd domain.com
```

## Class of Service (COS)

COS defines feature sets and quotas for groups of users.

```bash
# List all COS
zmprov gac

# Create COS
zmprov cc "Standard Users" zimbraMailQuota 1073741824

# Get COS details
zmprov gc "Standard Users"

# Modify COS
zmprov mc "Standard Users" zimbraFeatureMailEnabled TRUE

# Assign COS to user
zmprov ma user@domain.com zimbraCOSid <cos-id>

# Delete COS
zmprov dc "Standard Users"
```

## Server Management

### Service Control

```bash
# Check all services
zmcontrol status

# Start all services
zmcontrol start

# Stop all services
zmcontrol stop

# Restart specific service
zmcontrol restart mta
zmcontrol restart mailbox
zmcontrol restart ldap
zmcontrol restart proxy

# Full restart
zmcontrol restart
```

### Server Configuration

```bash
# Get server config
zmprov gs mail.domain.com

# Get specific setting
zmprov gs mail.domain.com zimbraSmtpHostname

# Modify server
zmprov ms mail.domain.com zimbraSmtpHostname localhost

# List all servers
zmprov gas

# Get global config
zmprov gacf

# Modify global config
zmprov mcf zimbraMailPurgeSleepInterval 1m
```

## Common LDAP Attributes

### Account Attributes

| Attribute | Description |
|-----------|-------------|
| `zimbraAccountStatus` | active, locked, closed, maintenance |
| `zimbraMailQuota` | Quota in bytes (0 = unlimited) |
| `zimbraMailAlias` | Email aliases (multi-value) |
| `zimbraMailForwardingAddress` | Forward destination |
| `zimbraFeatureCalendarEnabled` | Calendar access |
| `zimbraFeatureContactsEnabled` | Contacts access |
| `zimbraCOSid` | Assigned Class of Service |

### Domain Attributes

| Attribute | Description |
|-----------|-------------|
| `zimbraDomainStatus` | active, locked, closed, maintenance |
| `zimbraDomainDefaultCOSId` | Default COS for new accounts |
| `zimbraMailDomainQuota` | Domain aggregate quota |
| `zimbraPublicServiceHostname` | Public hostname |
| `zimbraVirtualHostname` | Virtual host mapping |

## Troubleshooting

### Check Service Health

```bash
# Service status
zmcontrol status

# Check mailbox
zmmailboxdctl status

# Check MTA
zmmtactl status

# View logs
tail -f /opt/zimbra/log/mailbox.log
tail -f /opt/zimbra/log/zimbra.log
```

### LDAP Issues

```bash
# Test LDAP connection
ldapsearch -x -H ldap://localhost:389 -D "uid=zimbra,cn=admins,cn=zimbra" \
  -w $(zmlocalconfig -s -m nokey zimbra_ldap_password) -b "" -s base

# Check LDAP replication (multi-server)
/opt/zimbra/libexec/zmreplchk
```

### Verify Configuration

```bash
# Describe attribute (verify it exists)
zmprov desc -a server | grep -i attributeName

# Dump all server attributes
zmprov gs $(hostname) > /tmp/server-config.txt
```

## Version Differences

### Zimbra 8.x vs 9.x/10.x

- **8.x**: Classic Web Client, traditional admin console
- **9.x**: Introduces Modern Web Client, GraphQL API
- **10.x**: Enhanced Modern Web Client, deprecated Classic for new deployments

### Command Compatibility

Most zmprov commands work across versions. Version-specific commands:

```bash
# Check Zimbra version
zmcontrol -v

# Zimbra 10.x specific
zmprov ms mail.domain.com zimbraModernWebClientEnabled TRUE
```

## Additional Resources

### Reference Files

For detailed attribute listings and advanced configurations:

- **`references/zmprov-commands.md`** - Complete zmprov command reference
- **`references/ldap-attributes.md`** - Full LDAP attribute documentation

### Example Files

Working scripts in `examples/`:

- **`examples/bulk-create-users.sh`** - Bulk user provisioning from CSV
- **`examples/export-accounts.sh`** - Export all accounts with attributes
