---
name: blazor-development
description: Use this skill when managing Blazor development, including Razor components and their associated editing practices.
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
- **Component**: Should inherit from `LocalizedComponentBase<ComponentName>`
- **Localization**: Use `ComponentName.resx` file in the Resources folder
- **Page Title**: Use `MotoRentPageTitle` custom component
- **Page Header**: Use `TablerHeader` with title and description in `PreTitle` property
- **Loading**: Implement a `boolean` property named `Loading` in a try-finally block when loading data
- **For Lists**: Use 2 columns, `col-3` for filters, and `col-9` for tables

## Loading Pattern (IMPORTANT)
- **Use `LoadingSkeleton`**: NOT `Dimmer` for loading states
- **Property Name**: Always use `Loading` (not `Busy`, `IsLoading`, etc.)
- **Early Return Guard**: Add `if (this.Loading) return;` at the start of the load method to avoid double loading
- **Try-Finally**: Always wrap loading logic in try-finally to ensure `Loading = false`

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
            <a href="#">Link</a>
        </div>
    </div>
</TablerHeader>

@code {
    private List<Motorbike> Motorbikes { get; set; } = new List<Motorbike>();
    private bool Loading { get; set; }

    protected override async Task OnInitializedAsync()
    {
        await LoadDataAsync();
    }
}
```