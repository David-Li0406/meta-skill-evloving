---
name: blazor-development
description: Manage Blazor development, including Razor components and editing skills.
---

# Blazor Development Skills

## Blazor Conventions
- **Rendering Mode**: Server-side rendering (default)
- **Component Structure**: Follow component-based architecture
- **State Management**: Use cascading parameters and service injection
- **File Naming**:
  - Components: `ComponentName.razor`
  - Code-behind: `ComponentName.razor.cs`
  - CSS isolation: `ComponentName.razor.css`

## Blazor Component Pattern
- **Component** should inherit from `LocalizedComponentBase<ComponentName>`
- **Localization**: Use `ComponentName.resx` file in the Resources folder
- **Page Title**: Use `MotoRentPageTitle` custom component
- **Page Header**: Use `TablerHeader` with title and description in `PreTitle` property
- **Loading**: Implement a `boolean` property named `Loading` in `try-finally` when loading data
- **For Lists**: Use 2 columns, `col-3` for filters, and `col-9` for tables

## Loading Pattern (IMPORTANT)
- **Use `LoadingSkeleton`** - NOT `Dimmer` for loading states
- **Property Name**: Always use `Loading` (not `Busy`, `IsLoading`, etc.)
- **Early Return Guard**: Add `if (this.Loading) return;` at the start of the load method to avoid double loading
- **try-finally**: Always wrap loading logic in try-finally to ensure `Loading = false`

### LoadingSkeleton Modes
```razor
<LoadingSkeleton Loading="@Loading" Mode="Skeleton.PlaceholderMode.Table">
    // Table content
</LoadingSkeleton>

<LoadingSkeleton Loading="@Loading" Mode="Skeleton.PlaceholderMode.Card">
    // Card content
</LoadingSkeleton>

<LoadingSkeleton Loading="@Loading" Mode="Skeleton.PlaceholderMode.Text">
    // Text content
</LoadingSkeleton>
```

### Loading Method Pattern
```csharp
private bool Loading { get; set; }

private async Task LoadDataAsync()
{
    if (this.Loading) return; // Prevent double loading
    try
    {
        this.Loading = true;
        // Load data...
    }
    finally
    {
        this.Loading = false;
    }
}
```

### Example Component
```razor
@page "/motorbikes"
@inherits LocalizedComponentBase<MotorbikeList>
@inject MotorbikeService MotorbikeService

<MotoRentPageTitle>@Localizer["Motorbikes"]</MotoRentPageTitle>
<TablerHeader Title="@Localizer["Motorbikes"]" PreTitle="@Localizer["List of all motorbikes"]">
    <div class="d-flex justify-content-end">
        <div class="px-2">
            <a href="@("/motorbikes/create")" class="btn btn-primary">
                <i class="ti ti-plus me-2"></i>
                @Localizer["Create new motorbike"]
            </a>
        </div>
    </div>
</TablerHeader>

<LoadingSkeleton Loading="@Loading" Mode="Skeleton.PlaceholderMode.Table">
    <table class="table table-vcenter">
        <thead>
            <tr>
                <th>@CommonLocalizer["Name"]</th>
                <th>@Localizer["LicensePlate"]</th>
                <th>@Localizer["Status"]</th>
            </tr>
        </thead>
        <tbody>
            @foreach (var motorbike in this.Motorbikes)
            {
                <tr>
                    <td>@motorbike.Brand @motorbike.Model</td>
                    <td>@motorbike.LicensePlate</td>
                    <td>
                        <span class="badge @GetStatusBadgeClass(motorbike.Status)">
                            @Localizer[motorbike.Status]
                        </span>
                    </td>
                </tr>
            }
        </tbody>
    </table>
</LoadingSkeleton>

@code {
    private List<Motorbike> Motorbikes { get; } = new();
    private bool Loading { get; set; }

    protected override async Task OnParametersSetAsync()
    {
        if (this.Loading) return; // avoid double loading
        try
        {
            this.Loading = true;
            var query = this.DataContext.CreateQuery<Motorbike>()
                    .Where(x => x.MotorbikeId > 0)
                    .OrderByDescending(x => x.Brand);
            var load = await this.DataContext.LoadAsync(query, includeTotalRows: true);
            this.Motorbikes.Clear();
            this.Motorbikes.AddRange(load.ItemCollection);
        }
        finally
        {
            this.Loading = false;
        }
    }

    private static string GetStatusBadgeClass(string status) => status switch
    {
        "Available" => "bg-success-lt",
        "Rented" => "bg-primary-lt",
        "Maintenance" => "bg-warning-lt",
        _ => "bg-secondary-lt"
    };
}
```

## CSS Isolation and Theming (IMPORTANT)

### Use CSS Isolation Files
- **Always use `.razor.css` files** instead of inline `<style>` blocks for better organization
- CSS isolation files are automatically scoped to the component
- Use `::deep` combinator to style child components

### Theme-Aware Styling with Tabler CSS
This project uses the Tabler CSS framework which supports light/dark themes via the `data-bs-theme` attribute.

**DO use Tabler's built-in CSS variables:**
```css
color: var(--tblr-body-color, #1e293b);        /* Primary text */
color: var(--tblr-secondary-color, #64748b);   /* Muted/secondary text */
border-color: var(--tblr-border-color, #e2e8f0); /* Borders */
background: var(--tblr-bg-surface);             /* Surface backgrounds */
```

**DON'T use custom CSS variables with `:global()` theme selectors:**
```css
:global([data-bs-theme="light"]) .my-component {
    --my-text: #1e293b; /* AVOID */
}
```

### Theme-Safe Color Guidelines

| Element | Light Theme | Dark Theme | Recommendation |
|---------|-------------|------------|----------------|
| Primary text | Dark (`#1e293b`) | Light (`rgba(255,255,255,0.85)`) | Use `var(--tblr-body-color)` |
| Muted text | Gray (`#64748b`) | Gray (`#94a3b8`) | Use `var(--tblr-secondary-color)` or fixed `#64748b` |
| Panel/Card bg | Light gray (`#f8fafc`) | Dark surface | Use `var(--tblr-bg-surface-secondary)` |
| Table header bg | Light gray (`#f1f5f9`) | Dark surface | Use `var(--tblr-bg-surface-secondary)` |
| Table header text | Muted (`#64748b`) | Light muted | Use `var(--tblr-secondary-color)` |
| Colored headers | Semi-transparent bg + darker text | Same | `rgba(color, 0.15)` + darker shade text |
| Highlight colors | Darker shade | Brighter shade | Debit: `#b45309`, Credit: `#047857` |

### Example: Theme-Aware Table
```css
/* ComponentName.razor.css */
::deep .my-table thead {
    background: var(--tblr-bg-surface-secondary, #f1f5f9);
}

::deep .my-table thead th {
    color: var(--tblr-secondary-color, #64748b);
}

::deep .my-table thead th.col-debit {
    background: rgba(217, 119, 6, 0.15);
    color: #b45309;  /* Darker amber - readable in both themes */
}

::deep .my-table thead th.col-credit {
    background: rgba(5, 150, 105, 0.15);
    color: #047857;  /* Darker emerald - readable in both themes */
}

::deep .my-table tbody td {
    color: var(--tblr-body-color, #1e293b);
    border-color: var(--tblr-border-color, #e2e8f0);
}

::deep .amount-debit {
    color: #d97706;
    background: rgba(217, 119, 6, 0.12);
}

::deep .amount-credit {
    color: #059669;
    background: rgba(5, 150, 105, 0.12);
}
```

### Key Rules
1. **Always provide fallback values**: `var(--tblr-body-color, #1e293b)`
2. **Use Tabler surface variables for panels/headers**: `var(--tblr-bg-surface-secondary)` - NOT custom variables
3. **Semi-transparent backgrounds**: `rgba(color, 0.12-0.15)` adapts to any theme
4. **Colored headers need darker text**: Use `#b45309` (amber) and `#047857` (emerald) for readability
5. **Test both themes**: Always verify components look correct in light AND dark mode

## UI Design with Bootstrap & Tabler CSS

### Design Philosophy
Create distinctive, polished interfaces that feel intentional and professional. Avoid generic patterns.

### Color Palette (Semantic Colors)
```css
--success: #2fb344;    /* Positive, completed, profit */
--danger: #d63939;     /* Error, negative, loss */
--warning: #f76707;    /* Caution, pending */
--info: #4299e1;       /* Information, neutral */
--debit: #d97706;      /* Amber - debits, expenses */
--credit: #059669;     /* Emerald - credits, income */
--primary: #00897B;    /* Tropical Teal - primary actions */
--secondary: #6c757d;  /* Secondary actions */
--muted: #64748b;      /* Muted text, icons */
```

### Card & Panel Design
```html
<div class="card shadow-sm">
    <div class="card-header">
        <h3 class="card-title">@Localizer["Title"]</h3>
        <div class="card-actions">
            <button class="btn btn-primary btn-sm">
                <i class="ti ti-plus me-1"></i>@Localizer["Add"]
            </button>
        </div>
    </div>
    <div class="card-body">
        <!-- Content -->
    </div>
</div>

<div class="card bg-primary-lt">
    <div class="card-body">
        <div class="d-flex align-items-center">
            <div class="avatar avatar-lg bg-primary text-white me-3">
                <i class="ti ti-motorbike"></i>
            </div>
            <div>
                <div class="text-muted small">@Localizer["TotalBikes"]</div>
                <div class="h2 mb-0">@Count</div>
            </div>
        </div>
    </div>
</div>
```

### Table Design Best Practices
```html
<div class="table-responsive">
    <table class="table table-hover table-vcenter">
        <thead>
            <tr>
                <th class="w-1"><!-- Checkbox column --></th>
                <th>@CommonLocalizer["Name"]</th>
                <th class="text-end">@Localizer["DailyRate"]</th>
                <th class="w-1"><!-- Actions --></th>
            </tr>
        </thead>
        <tbody>
            @foreach (var item in Items)
            {
                <tr class="@(item.IsHighlighted ? "bg-yellow-lt" : "")">
                    <td>
                        <input type="checkbox" class="form-check-input" />
                    </td>
                    <td>
                        <div class="d-flex align-items-center">
                            <span class="avatar avatar-sm me-2 bg-primary-lt">
                                <i class="ti ti-motorbike"></i>
                            </span>
                            <div>
                                <div class="fw-medium">@item.Brand @item.Model</div>
                                <div class="text-muted small">@item.LicensePlate</div>
                            </div>
                        </div>
                    </td>
                    <td class="text-end font-monospace">@item.DailyRate.ToString("N0") THB</td>
                    <td>
                        <div class="btn-list flex-nowrap">
                            <button class="btn btn-icon btn-ghost-primary">
                                <i class="ti ti-edit"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            }
        </tbody>
    </table>
</div>
```

### Status Badges & Indicators
```html
<span class="badge bg-success">@Localizer["Available"]</span>
<span class="badge bg-primary">@Localizer["Rented"]</span>
<span class="badge bg-warning">@Localizer["Maintenance"]</span>

<span class="badge bg-success-lt text-success">@Localizer["Active"]</span>
<span class="badge bg-danger-lt text-danger">@Localizer["Overdue"]</span>

<span class="status status-green">
    <span class="status-dot status-dot-animated"></span>
    @Localizer["Online"]
</span>
```

### Icons (Tabler Icons)
Always use Tabler icons (`ti ti-*`) for consistency:
```html
<i class="ti ti-plus"></i>           <!-- Add -->
<i class="ti ti-edit"></i>           <!-- Edit -->
<i class="ti ti-trash"></i>          <!-- Delete -->
<i class="ti ti-check"></i>          <!-- Confirm/Success -->
<i class="ti ti-x"></i>              <!-- Cancel/Close -->
<i class="ti ti-alert-triangle"></i> <!-- Warning -->
<i class="ti ti-info-circle"></i>    <!-- Info -->
<i class="ti ti-download"></i>       <!-- Export/Download -->
<i class="ti ti-upload"></i>         <!-- Import/Upload -->
<i class="ti ti-search"></i>         <!-- Search -->
<i class="ti ti-filter"></i>         <!-- Filter -->
<i class="ti ti-refresh"></i>        <!-- Refresh -->
<i class="ti ti-calendar"></i>       <!-- Date -->
<i class="ti ti-motorbike"></i>      <!-- Motorbike -->
<i class="ti ti-user"></i>           <!-- User/Renter -->
<i class="ti ti-receipt"></i>        <!-- Rental/Invoice -->
<i class="ti ti-coin"></i>           <!-- Money/Deposit -->
<i class="ti ti-sun"></i>            <!-- Light theme -->
<i class="ti ti-moon"></i>           <!-- Dark theme -->
```

### Spacing & Layout
```html
<div class="mb-3"><!-- margin-bottom: 1rem --></div>
<div class="p-3"><!-- padding: 1rem --></div>
<div class="gap-2"><!-- flex gap: 0.5rem --></div>

<div class="d-flex align-items-center justify-content-between">
    <div>Left content</div>
    <div>Right content</div>
</div>

<div class="row row-cards">
    <div class="col-sm-6 col-lg-3">
        <div class="card">...</div>
    </div>
</div>
```

## Localization
- **Labels and Text** should be in `@Localizer["Name"]`
- **Variables**: String variables should not be localized
- **Enum Variables**: If a variable is a C# enum, localize it to `@Localizer[EnumValue.ToString().Humanize()]`, then create entries for each enum value in resx files
- **Name Format**: If the name is too long, CamelCase it and keep it short and meaningful
- **CommonLocalizer**: Some commonly used text is already in the CommonLocalizer class and should be used
- **Formatted and C# Interpolated Strings**: Should be localized from `$"Some text here {amount:C} and some more {count:N0} items here"` to `@Localizer["Name", $"{amount:c}", $"{count:N0}"]`
- **Razor.resx**: For every Razor file