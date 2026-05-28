---
name: domain-entities
description: Use this skill when defining entity structures and multi-tenant architecture for a rental system like MotoRent.
---

# Domain Entities

Entity definitions for the MotoRent rental system.

## Multi-Tenant Architecture

MotoRent uses a **schema-per-tenant** isolation strategy:

```
[Core] schema (shared)              [AccountNo] schema (per tenant)
+------------------------+          +------------------------+
| Organization (tenant)  |          | Shop (outlet)          |
| User                   |          | Motorbike              |
| UserAccount (embedded) |          | Renter                 |
| Setting                |          | Rental                 |
| AccessToken            |          | Payment                |
| RegistrationInvite     |          | ... other operational  |
| LogEntry               |          +------------------------+
+------------------------+
```

### Key Concepts

1. **Organization** = Tenant (in [Core] schema)
   - Identified by `AccountNo` (unique string)
   - Contains tenant settings, subscriptions, timezone, currency

2. **Shop** = Outlet/Location (in tenant's schema)
   - One Organization can have multiple Shops
   - Shop data is stored in `[AccountNo].[Shop]` - schema provides isolation
   - **NO AccountNo property needed** on Shop entity

3. **User** = System user (in [Core] schema)
   - Can belong to multiple Organizations via `AccountCollection`
   - Each `UserAccount` entry links to an Organization with roles

### Why Shop doesn't have AccountNo

```csharp
// WRONG - Redundant! Schema already provides tenant isolation
public class Shop : Entity
{
    public string AccountNo { get; set; }  // DON'T DO THIS
}

// CORRECT - Schema isolation handles multi-tenancy
public class Shop : Entity
{
    // Data stored in [AccountNo].[Shop] table
    // No AccountNo property needed
}
```

## Entity Overview

### Core Entities (Shared [Core] Schema)

| Entity | Description | Key Fields |
|--------|-------------|------------|
| Organization | Tenant/company | AccountNo, Name, Currency, Timezone |
| User | System user | UserName, Email, AccountCollection |
| UserAccount | User-org link | AccountNo, Roles[] |
| Setting | Config values | AccountNo, Key, Value, UserName |
| AccessToken | API tokens | Token, Salt, AccountNo, Expires |
| RegistrationInvite | Invite codes | Code, ValidFrom, ValidTo, MaxAccount |
| LogEntry | Audit logs | AccountNo, UserName, Message, Severity |

### Operational Entities (Tenant Schema)

| Entity | Description | Key Fields |
|--------|-------------|------------|
| Shop | Outlet location | Name, Address, ContactInfo |
| Motorbike | Rental vehicle | Model, Year, Status |
| Renter | Customer renting | Name, ContactInfo, RentalHistory |
| Rental | Transaction details | StartDate, EndDate, TotalCost |
| Payment | Payment details | Amount, PaymentMethod, Status |
```