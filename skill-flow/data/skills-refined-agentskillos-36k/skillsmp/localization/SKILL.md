name: localization
description: Multi-language support (English/Thai) implementation using localized base classes and resource files.
---
# Localization (Multi-Language Support)

Multi-language support patterns for MotoRent (English/Thai) using localized base classes.

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
<data name="Add"><value>Add</value></data>
<data name="Search"><value>Search</value></data>
<data name="Actions"><value>Actions</value></data>
<data name="Loading"><value>Loading...</value></data>
<data name="NoData"><value>No data available</value></data>
<data name="ConfirmDelete"><value>Are you sure you want to delete this item?</value></data>
<data name="Success"><value>Operation completed successfully</value></data>
<data name="Error"><value>An error occurred. Please try again.</value></data>

<!-- CommonResources.th.resx -->
<data name="Save"><value>บันทึก</value></data>
<data name="Cancel"><value>ยกเลิก</value></data>
<data name="Delete"><value>ลบ</value></data>
<data name="Edit"><value>แก้ไข</value></data>
<data name="Add"><value>เพิ่ม</value></data>
<data name="Search"><value>ค้นหา</value></data>
<data name="Actions"><value>การดำเนินการ</value></data>
<data name="Loading"><value>กำลังโหลด...</value></data>
<data name="NoData"><value>ไม่มีข้อมูล</value></data>
<data name="ConfirmDelete"><value>คุณแน่ใจหรือไม่ว่าต้องการลบรายการนี้?</value></data>
<data name="Success"><value>ดำเนินการสำเร็จ</value></data>
<data name="Error"><value>เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง</value></data>
```

## Thai Language Reference

| English | Thai | Notes |
|---------|------|-------|
| Rental | การเช่า | |
| Motorbike | มอเตอร์ไซค์ | or รถจักรยานยนต์ (formal) |
| Deposit | เงินมัดจำ | |
| Passport | หนังสือเดินทาง | |
| Driving License | ใบขับขี่ | |
| Check-in | เช็คอิน | transliteration common |
| Check-out | เช็คเอาท์ | transliteration common |
| Available | ว่าง | |
| Rented | ถูกเช่า | |
| Damage | ความเสียหาย | |
| Insurance | ประกันภัย | |
| Daily Rate | ราคาต่อวัน | |

## Service Registration

```csharp
// Program.cs
builder.Services.AddLocalization(options => options.ResourcesPath = "Resources");

builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    var supportedCultures = new[] { "en", "th" };
    options.SetDefaultCulture("en");
    options.AddSupportedCultures(supportedCultures);
    options.AddSupportedUICultures(supportedCultures);
});

// In app pipeline
app.UseRequestLocalization();
```



```razor
@page "/motorbikes"
@inherits LocalizedComponentBase<Motorbikes>
@using MotoRent.Domain.Entities
@inject MotorbikeService MotorbikeService

<PageTitle>@Localizer["PageTitle"]</PageTitle>

<MudStack Row="true" Justify="Justify.SpaceBetween" Class="mb-4">
    <MudText Typo="Typo.h4">@Localizer["Header"]</MudText>
    <MudButton Color="Color.Primary" OnClick="Add">
        @CommonLocalizer["Add"]
    </MudButton>
</MudStack>

<MudDataGrid T="Motorbike" Items="@m_motorbikes">
    <Columns>
        <PropertyColumn Property="x => x.LicensePlate" Title="@Localizer["LicensePlate"]" />
        <PropertyColumn Property="x => x.Brand" Title="@Localizer["Brand"]" />
        <TemplateColumn Title="@Localizer["Status"]">
            <CellTemplate>
                @* Localize enum/status values *@
                <MudChip>@Localizer[context.Item.Status ?? "Unknown"]</MudChip>
            </CellTemplate>
        </TemplateColumn>
    </Columns>
</MudDataGrid>

@code {
    private List<Motorbike> m_motorbikes = [];
}
```


```razor
@inherits LocalizedDialogBase<Motorbike, MotorbikeDialog>

<MudDialog>
    <DialogContent>
        <MudForm @ref="Form" @bind-IsValid="FormValid">
            <MudTextField @bind-Value="Entity.LicensePlate"
                          Label="@Localizer["LicensePlate"]"
                          Required="true"
                          RequiredError="@Localizer["LicensePlateRequired"]" />
        </MudForm>
    </DialogContent>
    <DialogActions>
        <MudButton OnClick="Cancel">@CommonLocalizer["Cancel"]</MudButton>
        <MudButton Color="Color.Primary" OnClick="Close">
            @(IsNew ? CommonLocalizer["Add"] : CommonLocalizer["Save"])
        </MudButton>
    </DialogActions>
</MudDialog>
```

## Formatted Strings

```csharp
// Resource file:
// RentalSummary = "Rental for {0} days at {1} per day"

// Usage:
@Localizer["RentalSummary", days, FormatCurrency(dailyRate)]
```

## What to Localize

### DO Localize
- UI labels and headers
- Button text
- Validation messages
- Success/error messages
- Tooltips and help text
- Email/SMS templates

### DO NOT Localize
- Code logic strings: `if (status == "Active")`
- Database values (status enum values in code)
- API responses (unless user-facing)
- Log messages (keep in English for debugging)
- Configuration keys

## Culture Switching

```csharp
    private string m_currentCulture = CultureInfo.CurrentCulture.TwoLetterISOLanguageName;

    private void OnCultureChanged(string culture)
    {
        var uri = new Uri(Navigation.Uri)
            .GetComponents(UriComponents.PathAndQuery, UriFormat.Unescaped);
        Navigation.NavigateTo(
            $"Culture/Set?culture={Uri.EscapeDataString(culture)}&redirectUri={Uri.EscapeDataString(uri)}",
            forceLoad: true);
    }

```

## Source
- Base classes: `src/MotoRent.Client/Controls/`
- Resources: `src/MotoRent.Client/Resources/`
- From: `..\rx-erp` localization patterns

```