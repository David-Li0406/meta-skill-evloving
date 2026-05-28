---
name: localization
description: Use this skill when implementing multi-language support (English/Thai) in applications using localized base classes and resource files.
---

# Skill body

## Base Class Integration

### Inherit from Localized Base Classes

```razor
@* Page with localization *@
@page "/motorbikes"
@inherits LocalizedComponentBase<Motorbikes>

@* Dialog with localization *@
@inherits LocalizedDialogBase<Motorbike, MotorbikeDialog>
```

### Available Localizers

| Localizer | Source | Usage |
|-----------|--------|-------|
| `Localizer` | `LocalizedComponentBase<T>` | Component-specific strings |
| `CommonLocalizer` | `MotoRentComponentBase` | Shared strings (Save, Cancel, etc.) |

### Usage in Components

```razor
@* Component-specific strings *@
<MudText>@Localizer["PageTitle"]</MudText>
<Component Label="@Localizer["LicensePlate"]" />

@* Shared strings (buttons, common labels) *@
<Component>@CommonLocalizer["Save"]</Component>
<Component>@CommonLocalizer["Cancel"]</Component>
<Component>@CommonLocalizer["Delete"]</Component>

@* With parameters *@
<Component>@Localizer["WelcomeMessage", userName, shopName]</Component>
```

## Naming Conventions for Keys

### Use Short, Descriptive Keys

```csharp
// BAD - Long sentences as keys
Localizer["Would you like to confirm this rental for {0}?"]

// GOOD - PascalCase variable-like names
Localizer["RentalConfirmMessage", renterName]
```

### Context Prefixes for Clarity

```csharp
// Different contexts for similar actions
Localizer["CheckInSuccessMessage"]      // "Rental checked in successfully"
Localizer["CheckOutSuccessMessage"]     // "Rental checked out successfully"
Localizer["DepositCollectedMessage"]    // "Deposit collected successfully"
```

## Resource File Structure

```
project/
├── Resources/
│   ├── CommonResources.resx           # Shared strings (English)
│   ├── CommonResources.th.resx        # Shared strings (Thai)
│   └── Pages/
│       ├── Motorbikes.resx            # English
│       ├── Motorbikes.th.resx         # Thai
│       ├── MotorbikeDialog.resx
│       ├── MotorbikeDialog.th.resx
│       └── ...
```

## CommonResources Keys

Standard keys for `CommonLocalizer`:

```xml
<!-- CommonResources.resx -->
<data name="Save"><value>Save</value></data>
<data name="Cancel"><value>Cancel</value></data>
<data name="Delete"><value>Delete</value></data>
<data name="Edit"><value>Edit</value></data>
```