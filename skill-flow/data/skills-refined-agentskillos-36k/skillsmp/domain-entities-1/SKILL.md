name: domain-entities
description: Entity definitions and multi-tenant architecture schema for the MotoRent rental system.
---
# Domain Entities

Entity definitions for MotoRent rental system.

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
   - Shop data is in `[AccountNo].[Shop]` - schema provides isolation
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
| Shop | Outlet/location | Name, Location, Phone |
| Renter | Tourist/customer | FullName, Passport, Phone |
| Document | ID/license images | DocumentType, ImagePath, OcrData |
| Motorbike | Inventory | LicensePlate, Brand, Status |
| Rental | Rental transaction | Renter, Motorbike, Dates, Amount |
| Deposit | Cash/card deposits | Type, Amount, Status |
| Insurance | Insurance packages | Name, DailyRate, Coverage |
| Accessory | Helmets, etc. | Name, DailyRate, Quantity |
| RentalAccessory | Junction table | RentalId, AccessoryId |
| Payment | Payment records | Type, Method, Amount |
| DamageReport | Damage documentation | Description, Severity, Cost |
| DamagePhoto | Before/after photos | PhotoType, ImagePath |
| RentalAgreement | Digital signature | SignatureImagePath |

## Base Entity Class

```csharp
// MotoRent.Domain/Entities/Entity.cs
[JsonPolymorphic(TypeDiscriminatorPropertyName = "$type")]
// Operational entities (tenant schema)
[JsonDerivedType(typeof(Shop), nameof(Shop))]
[JsonDerivedType(typeof(Renter), nameof(Renter))]
[JsonDerivedType(typeof(Document), nameof(Document))]
[JsonDerivedType(typeof(Motorbike), nameof(Motorbike))]
[JsonDerivedType(typeof(Rental), nameof(Rental))]
[JsonDerivedType(typeof(Deposit), nameof(Deposit))]
[JsonDerivedType(typeof(Insurance), nameof(Insurance))]
[JsonDerivedType(typeof(Accessory), nameof(Accessory))]
[JsonDerivedType(typeof(RentalAccessory), nameof(RentalAccessory))]
[JsonDerivedType(typeof(Payment), nameof(Payment))]
[JsonDerivedType(typeof(DamageReport), nameof(DamageReport))]
[JsonDerivedType(typeof(DamagePhoto), nameof(DamagePhoto))]
[JsonDerivedType(typeof(RentalAgreement), nameof(RentalAgreement))]
// Core entities ([Core] schema)
[JsonDerivedType(typeof(Organization), nameof(Organization))]
[JsonDerivedType(typeof(User), nameof(User))]
[JsonDerivedType(typeof(Setting), nameof(Setting))]
[JsonDerivedType(typeof(AccessToken), nameof(AccessToken))]
[JsonDerivedType(typeof(RegistrationInvite), nameof(RegistrationInvite))]
[JsonDerivedType(typeof(LogEntry), nameof(LogEntry))]
public abstract class Entity
{
    public string? WebId { get; set; }

    [JsonIgnore] public string? CreatedBy { get; set; }
    [JsonIgnore] public DateTimeOffset CreatedTimestamp { get; set; }
    [JsonIgnore] public string? ChangedBy { get; set; }
    [JsonIgnore] public DateTimeOffset ChangedTimestamp { get; set; }

    public abstract int GetId();
    public abstract void SetId(int value);
}
```

## Shop

An outlet/location within a tenant's organization. Stored in tenant schema.

```csharp
/// <summary>
/// Represents a shop/outlet location within a tenant's organization.
/// Shop data is stored in the tenant's schema (e.g., [AccountNo].[Shop]),
/// so tenant isolation is provided by the schema itself - no AccountNo property needed.
/// </summary>
public class Shop : Entity
{
    public int ShopId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Location { get; set; } = string.Empty;  // Phuket, Krabi, Koh Samui
    public string Address { get; set; } = string.Empty;
    public string Phone { get; set; } = string.Empty;
    public string? Email { get; set; }
    public string? LogoPath { get; set; }
    public string? TermsAndConditions { get; set; }
    public bool IsActive { get; set; } = true;

    public override int GetId() => this.ShopId;
    public override void SetId(int value) => this.ShopId = value;
}
```

## Renter

```csharp
public class Renter : Entity
{
    public int RenterId { get; set; }
    public int ShopId { get; set; }
    public string FullName { get; set; } = string.Empty;
    public string? Nationality { get; set; }
    public string? PassportNo { get; set; }
    public string? NationalIdNo { get; set; }
    public string? DrivingLicenseNo { get; set; }
    public string? DrivingLicenseCountry { get; set; }
    public DateTimeOffset? DrivingLicenseExpiry { get; set; }
    public string Phone { get; set; } = string.Empty;
    public string? Email { get; set; }
    public string? HotelName { get; set; }
    public string? HotelAddress { get; set; }
    public string? EmergencyContact { get; set; }
    public string? ProfilePhotoPath { get; set; }

    public override int GetId() => this.RenterId;
    public override void SetId(int value) => this.RenterId = value;
}
```

## Document

```csharp
public class Document : Entity
{
    public int DocumentId { get; set; }
    public int RenterId { get; set; }
    public string DocumentType { get; set; } = string.Empty;  // Passport, NationalId, DrivingLicense
    public string ImagePath { get; set; } = string.Empty;
    public string? OcrRawJson { get; set; }   // Gemini response
    public string? ExtractedData { get; set; } // Parsed fields
    public DateTimeOffset UploadedOn { get; set; }
    public bool IsVerified { get; set; }

    public override int GetId() => this.DocumentId;
    public override void SetId(int value) => this.DocumentId = value;
}
```

## Motorbike

```csharp
public class Motorbike : Entity
{
    public int MotorbikeId { get; set; }
    public int ShopId { get; set; }
    public string LicensePlate { get; set; } = string.Empty;
    public string Brand { get; set; } = string.Empty;     // Honda, Yamaha
    public string Model { get; set; } = string.Empty;     // Click, PCX, Aerox
    public int EngineCC { get; set; }                     // 110, 125, 150
    public string? Color { get; set; }
    public int Year { get; set; }
    public string Status { get; set; } = "Available";     // Available, Rented, Maintenance
    public decimal DailyRate { get; set; }
    public decimal DepositAmount { get; set; }
    public string? ImagePath { get; set; }
    public string? Notes { get; set; }
    public int Mileage { get; set; }
    public DateTimeOffset? LastServiceDate { get; set; }

    public override int GetId() => this.MotorbikeId;
    public override void SetId(int value) => this.MotorbikeId = value;
}
```

## Rental

```csharp
public class Rental : Entity
{
    public int RentalId { get; set; }
    public int ShopId { get; set; }
    public int RenterId { get; set; }
    public int MotorbikeId { get; set; }
    public DateTimeOffset StartDate { get; set; }
    public DateTimeOffset ExpectedEndDate { get; set; }
    public DateTimeOffset? ActualEndDate { get; set; }
    public int MileageStart { get; set; }
    public int? MileageEnd { get; set; }
    public decimal DailyRate { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; } = "Reserved";  // Reserved, Active, Completed, Cancelled
    public string? Notes { get; set; }
    public int? InsuranceId { get; set; }
    public int? DepositId { get; set; }

    public override int GetId() => this.RentalId;
    public override void SetId(int value) => this.RentalId = value;
}
```

## Status Values

### Motorbike.Status
| Status | Description |
|--------|-------------|
| Available | Ready for rental |
| Rented | Currently out |
| Maintenance | Under repair |

### Rental.Status
| Status | Description |
|--------|-------------|
| Reserved | Booked, not started |
| Active | Currently in progress |
| Completed | Returned successfully |
| Cancelled | Cancelled before start |

### Deposit.Status
| Status | Description |
|--------|-------------|
| Held | Deposit collected |
| Refunded | Returned to customer |
| Forfeited | Kept due to damage |

### Payment.Status
| Status | Description |
|--------|-------------|
| Pending | Awaiting payment |
| Completed | Payment received |
| Refunded | Money returned |

### DamageReport.Status
| Status | Description |
|--------|-------------|
| Pending | Awaiting resolution |
| Charged | Customer paid |
| Waived | No charge |
| InsuranceClaim | Sent to insurance |

## File Location

```
MotoRent.Domain/
├── Entities/           # Operational entities (tenant schema)
│   ├── Entity.cs       # Base class with polymorphic types
│   ├── Shop.cs
│   ├── Renter.cs
│   ├── Document.cs
│   ├── Motorbike.cs
│   ├── Rental.cs
│   ├── Deposit.cs
│   ├── Insurance.cs
│   ├── Accessory.cs
│   ├── RentalAccessory.cs
│   ├── Payment.cs
│   ├── DamageReport.cs
│   ├── DamagePhoto.cs
│   └── RentalAgreement.cs
├── Core/               # Core entities ([Core] schema)
│   ├── Organization.cs
│   ├── User.cs
│   ├── UserAccount.cs
│   ├── Setting.cs
│   ├── AccessToken.cs
│   ├── RegistrationInvite.cs
│   ├── LogEntry.cs
│   ├── IRequestContext.cs
│   └── IDirectoryService.cs
└── DataContext/
    ├── RentalDataContext.cs    # Tenant operational data
    └── CoreDataContext.cs      # Core shared data
```

## Core Entity Examples

### Organization (Tenant)

```csharp
public class Organization : Entity
{
    public int OrganizationId { get; set; }
    public string AccountNo { get; set; } = "";      // Unique tenant identifier
    public string Name { get; set; } = "";
    public string Currency { get; set; } = "THB";
    public double? Timezone { get; set; } = 7;       // UTC+7 Thailand
    public string Language { get; set; } = "th-TH";
    public string[] Subscriptions { get; set; } = [];
    public bool IsActive { get; set; } = true;
    // ... address, logos, etc.
}
```

### User

```csharp
public class User : Entity
{
    public int UserId { get; set; }
    public string UserName { get; set; } = "";       // Typically email
    public string Email { get; set; } = "";
    public string FullName { get; set; } = "";
    public string CredentialProvider { get; set; }   // Google, Microsoft, Custom
    public bool IsLockedOut { get; set; }

    // Multi-tenant access
    public List<UserAccount> AccountCollection { get; } = [];
    public string? AccountNo => AccountCollection.FirstOrDefault()?.AccountNo;
}
```

### UserAccount (Links User to Organization)

```csharp
public class UserAccount
{
    public string AccountNo { get; set; } = "";      // Links to Organization
    public string? StartPage { get; set; }
    public bool IsFavourite { get; set; }
    public List<string> Roles { get; } = [];         // Role strings

    // Role constants
    public const string SUPER_ADMIN = "administrator";
    public const string ORG_ADMIN = "OrgAdmin";
    public const string SHOP_MANAGER = "ShopManager";
    public const string STAFF = "Staff";
    public const string MECHANIC = "Mechanic";
}
```
