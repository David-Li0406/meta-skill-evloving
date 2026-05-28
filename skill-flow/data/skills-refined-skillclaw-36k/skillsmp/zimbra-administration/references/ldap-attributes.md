# Zimbra LDAP Attributes Reference

Complete reference for Zimbra LDAP attributes used in account, domain, COS, and server configuration.

## Account Attributes

### Status and Authentication

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraAccountStatus` | enum | Account status: active, locked, closed, maintenance, pending |
| `zimbraAuthTokenValidityValue` | integer | Auth token validity in seconds |
| `zimbraPasswordMustChange` | boolean | Force password change on next login |
| `zimbraPasswordLockoutEnabled` | boolean | Enable account lockout after failed attempts |
| `zimbraPasswordLockoutMaxFailures` | integer | Max failed attempts before lockout |

### Mail Settings

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraMailQuota` | long | Mailbox quota in bytes (0 = unlimited) |
| `zimbraMailAlias` | string[] | Email aliases |
| `zimbraMailForwardingAddress` | string[] | Forwarding addresses |
| `zimbraMailDeliveryAddress` | string | Primary delivery address |
| `zimbraPrefMailForwardingAddress` | string | User-set forwarding address |
| `zimbraMailSieveScript` | string | Sieve filter script |

### Features

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraFeatureMailEnabled` | boolean | Email feature |
| `zimbraFeatureCalendarEnabled` | boolean | Calendar feature |
| `zimbraFeatureContactsEnabled` | boolean | Contacts feature |
| `zimbraFeatureTasksEnabled` | boolean | Tasks feature |
| `zimbraFeatureBriefcasesEnabled` | boolean | Briefcase feature |
| `zimbraFeatureIMEnabled` | boolean | Instant messaging |
| `zimbraFeatureSharingEnabled` | boolean | Sharing feature |

### Identity

| Attribute | Type | Description |
|-----------|------|-------------|
| `displayName` | string | Full display name |
| `givenName` | string | First name |
| `sn` | string | Surname (last name) |
| `initials` | string | Middle initials |
| `company` | string | Company name |
| `title` | string | Job title |
| `telephoneNumber` | string | Phone number |

## Domain Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraDomainStatus` | enum | Domain status |
| `zimbraDomainDefaultCOSId` | string | Default COS for new accounts |
| `zimbraMailDomainQuota` | long | Aggregate quota for domain |
| `zimbraPublicServiceHostname` | string | Public-facing hostname |
| `zimbraPublicServiceProtocol` | string | http or https |
| `zimbraPublicServicePort` | integer | Public port |
| `zimbraVirtualHostname` | string[] | Virtual host mappings |
| `zimbraAuthMech` | string | Authentication mechanism |

## COS Attributes

COS attributes are inherited by accounts. Most account attributes can be set at COS level.

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraCOSId` | string | COS unique identifier |
| `cn` | string | COS name |
| `description` | string | COS description |
| `zimbraMailQuota` | long | Default quota for COS members |

## Server Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `zimbraServiceEnabled` | string[] | Enabled services |
| `zimbraServiceInstalled` | string[] | Installed services |
| `zimbraSmtpHostname` | string | SMTP relay hostname |
| `zimbraMtaRelayHost` | string | MTA relay host |
| `zimbraMtaMyNetworks` | string[] | Trusted networks |

## Lookup Commands

```bash
# Describe all account attributes
zmprov desc -a account

# Describe all domain attributes
zmprov desc -a domain

# Describe all COS attributes
zmprov desc -a cos

# Describe all server attributes
zmprov desc -a server

# Search for specific attribute
zmprov desc -a account | grep -i quota
```
