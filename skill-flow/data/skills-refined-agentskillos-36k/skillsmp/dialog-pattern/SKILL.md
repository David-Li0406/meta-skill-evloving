---
name: dialog-pattern
description: Tabler modal dialog patterns using localized base classes and fluent API extensions.
---
# Dialog Pattern Skills

## Dialog Pattern
- **Dialog Pattern** should be used for **SIMPLE** create, update
- **Form editor Pattern** should be used for **COMPLEX** create, update
- **Clone** the object before passing it to the dialog, so that the original object is not modified if user cancels the dialog
- **Persistence** should be done in the parent component, not in the dialog
- **Parent component** Update the list after persistence
- **Business logic** should **NOT** be done in the parent component, nor in the dialog
- **Use Operation** `Operation` name should be used for committing unit of work session
- **Base class** Use `LocalizedDialogBase<ItemType, ResourceType>`

## Base Class Properties and Methods
The `LocalizedDialogBase<TItem, TResource>` base class provides:
- `Item` - The data object passed to the dialog
- `DataContext` - Database context for queries
- `RequestContext` - Request context (do NOT re-inject)
- `Localizer` - Localization for TResource
- `CommonLocalizer` - Common localization strings
- `FormId` - Unique form ID for submit binding
- `OkClick(item)` - Call to return result and close dialog
- `Cancel()` - Call to cancel and close dialog
- `OkDisabled` - Virtual property to control OK button state

```csharp
// sample MotorbikeDialog.razor
@inherits LocalizedDialogBase<Motorbike, MotorbikeDialog>

@if (this.Item is not null)
{
    <CascadingValue Name="LabelCols" Value="3">
        <EditForm Model="@Item" id="@FormId" OnValidSubmit="() => OkClick(Item)">

            <div class="mb-3">
                <label class="form-label required">@CommonLocalizer["Name"]</label>
                <input type="text" class="form-control" @bind="Item.Name" autofocus required />
            </div>

        </EditForm>
    </CascadingValue>
}
<div class="modal-footer">
    <button type="submit" form="@FormId" disabled="@OkDisabled" class="btn btn-primary ms-auto" data-bs-dismiss="modal">
        @CommonLocalizer["OK"]
    </button>
    <a @onclick="Cancel" class="btn btn-link link-secondary" data-bs-dismiss="modal">
        @CommonLocalizer["Cancel"]
    </a>
</div>

@code {

    protected override bool OkDisabled => this.Item switch
    {
        null => true,
        {Name: "" or null} => true,
        _ => false
    };
}
```

```csharp
// "MotorbikeDialog" is your Razor component
private async Task EditMotorbike(Motorbike? motorbike = null)
{
    motorbike ??= new Motorbike(); // for new Motorbike, we create it
    var result = await this.DialogService.Create<MotorbikeDialog>(Localizer["Add new motorbike"])
        .WithParameter(x => x.Item, motorbike.Clone())
        .ShowDialogAsync();

    if (result is {Cancelled:false, Data: Motorbike item})
    {
        // Save the item to persistent
        using(var session = this.DataContext.OpenSession())
        {
            session.Attach(item);
            await session.SubmitChanges("Edit");

            // since the edit is called from a table or list, we just update or add new one
            this.Motorbikes.AddOrReplace(item, x => x.MotorbikeId == item.MotorbikeId);
        }
    }
}
```

## UI Helpers
### Text Prompt
```csharp
string? reason = await this.DialogService.PromptAsync(
    Localizer["Cancel Rental"],
    Localizer["Please provide a reason for cancelling this rental:"]
);
```
### Confirmation Dialog
```csharp
if (!await this.DialogService.ConfirmYesNoAsync(Localizer["Are you sure you want to delete this?"]))
{
    return;
}
```
### Message Box
```csharp
await this.DialogService.ShowMessageAsync(
    Localizer["Rental {0} has been saved", Rental.No],
    CommonLocalizer["Rental"],
    icon: MessageIcon.Info
);
```

## Selection Dialog Pattern
For dialogs that select items from a list (multi-select, search, pagination):

```csharp
// SelectionDialog.razor
@inherits LocalizedDialogBase<SelectionResult, SelectionDialog>

<div class="modal-body">
    <div class="row mb-3">
        <div class="col-8">
            <span class="badge bg-primary-lt">@SelectedCount @Localizer["selected"]</span>
        </div>
        <div class="col-4">
            <div class="input-icon">
                <input type="search" placeholder="@CommonLocalizer["Search..."]"
                       class="form-control form-control-sm" @oninput="OnSearchChanged" />
                <span class="input-icon-addon"><i class="ti ti-search"></i></span>
            </div>
        </div>
    </div>

    <LoadingSkeleton Loading="@Loading" Mode="Skeleton.PlaceholderMode.Table">
        <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
            <table class="table table-sm table-hover">
                <thead class="sticky-top bg-white">
                    <tr>
                        <th class="w-1">
                            <input class="form-check-input" type="checkbox"
                                   checked="@AllSelected" @onchange="ToggleSelectAll" />
                        </th>
                        <th>@CommonLocalizer["Name"]</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var item in Items)
                    {
                        var isSelected = SelectedIds.Contains(item.Id);
                        <tr class="@(isSelected ? "table-primary" : "")" @onclick="() => ToggleItem(item)">
                            <td>
                                <input class="form-check-input" type="checkbox" checked="@isSelected"
                                       @onclick:stopPropagation="true" @onchange="() => ToggleItem(item)" />
                            </td>
                            <td>@item.Name</td>
                        </tr>
                    }
                </tbody>
            </table>
        </div>
        <Pager TotalRows="@TotalRows" Size="@PageSize" OnPageChanged="PageChanged"></Pager>
    </LoadingSkeleton>
</div>
<div class="modal-footer">
    <button type="button" class="btn btn-primary" @onclick="ConfirmSelection">
        <i class="ti ti-check me-1"></i>@CommonLocalizer["OK"]
    </button>
    <a @onclick="Cancel" class="btn btn-link link-secondary" data-bs-dismiss="modal">
        @CommonLocalizer["Cancel"]
    </a>
</div>
```

```csharp
// SelectionDialog.razor.cs
public partial class SelectionDialog
{
    private int TotalRows { get; set; }
    private bool Loading { get; set; }
    private int PageSize { get; } = 20;
    private List<Item> Items { get; } = [];
    private HashSet<int> SelectedIds { get; } = [];
    private string? SearchTerm { get; set; }

    [Parameter] public List<int> InitialSelectedIds { get; set; } = [];

    private int SelectedCount => this.SelectedIds.Count;
    private bool AllSelected => this.Items.Count > 0 && this.Items.All(e => this.SelectedIds.Contains(e.Id));

    protected override async Task OnInitializedAsync()
    {
        this.Item ??= new SelectionResult();
        foreach (var id in this.InitialSelectedIds) this.SelectedIds.Add(id);
        await this.LoadItemsAsync(1);
    }

    private async Task LoadItemsAsync(int page)
    {
        if (this.Loading) return;
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

    private void ConfirmSelection()
    {
        var result = new SelectionResult { SelectedIds = this.SelectedIds.ToList() };
        this.OkClick(result);
    }
}
```

## Beautiful Dialog UI Design

### Dialog Header with Icon
```html
<!-- Use Tabler's bg-surface-secondary for theme-aware panel backgrounds -->
<div class="p-3 mb-3 rounded-3" style="background: var(--tblr-bg-surface-secondary, #f8fafc); border: 1px solid var(--tblr-border-color);">
    <div class="d-flex align-items-center gap-3">
        <div class="avatar avatar-lg" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);">
            <i class="ti ti-motorbike text-white" style="font-size: 1.5rem;"></i>
        </div>
        <div>
            <div class="text-muted small text-uppercase fw-bold" style="letter-spacing: 0.05em;">
                @Localizer["HeaderLabel"]
            </div>
            <div class="h4 mb-0 fw-bold">@Item.Title</div>
        </div>
    </div>
</div>
```

### Styled Data Table in Dialog
**IMPORTANT**: For table headers, use Tabler's surface variables with darker text colors for readability. Avoid bright text on colored backgrounds.
```html
<div class="rounded-3 overflow-hidden border">
    <table class="table table-sm mb-0">
        <!-- Use Tabler surface variable for theme-aware header -->
        <thead style="background: var(--tblr-bg-surface-secondary, #f1f5f9);">
            <tr>
                <th style="color: var(--tblr-secondary-color, #64748b);">@Localizer["Item"]</th>
                <!-- Colored headers: semi-transparent bg + DARKER text for readability -->
                <th class="text-end" style="background: rgba(217, 119, 6, 0.15); color: #b45309;">
                    @Localizer["Debit"]
                </th>
                <th class="text-end" style="background: rgba(5, 150, 105, 0.15); color: #047857;">
                    @Localizer["Credit"]
                </th>
            </tr>
        </thead>
        <tbody>
            @foreach (var line in Lines)
            {
                <tr>
                    <td>
                        <span class="d-flex align-items-center gap-2">
                            <i class="ti @line.Icon text-muted"></i>
                            @Localizer[line.Description]
                        </span>
                    </td>
                    <td class="text-end font-monospace fw-semibold" style="color: #d97706;">
                        @(line.Debit > 0 ? line.Debit.ToString("N2") : "")
                    </td>
                    <td class="text-end font-monospace fw-semibold" style="color: #059669;">
                        @(line.Credit > 0 ? line.Credit.ToString("N2") : "")
                    </td>
                </tr>
            }
        </tbody>
        <!-- Footer can use dark bg since it's a fixed element -->
        <tfoot style="background: #1e293b;">
            <tr>
                <td class="text-light fw-bold">@CommonLocalizer["Total"]</td>
                <td class="text-end font-monospace fw-bold" style="color: #fbbf24;">
                    @TotalDebit.ToString("N2")
                </td>
                <td class="text-end font-monospace fw-bold" style="color: #6ee7b7;">
                    @TotalCredit.ToString("N2")
                </td>
            </tr>
        </tfoot>
    </table>
</div>
```

### Status Indicator Cards
```html
<!-- Success indicator -->
<div class="d-flex align-items-center justify-content-center gap-2 p-3 rounded-3 mt-3"
     style="background: rgba(16, 185, 129, 0.15); color: #059669; border: 1px solid rgba(16, 185, 129, 0.3);">
    <i class="ti ti-circle-check"></i>
    <span class="fw-semibold">@Localizer["RentalCompleted"]</span>
</div>

<!-- Warning indicator -->
<div class="d-flex align-items-center justify-content-center gap-2 p-3 rounded-3 mt-3"
     style="background: rgba(239, 68, 68, 0.15); color: #dc2626; border: 1px solid rgba(239, 68, 68, 0.3);">
    <i class="ti ti-alert-triangle"></i>
    <span class="fw-semibold">@Localizer["DamageReported"]</span>
</div>
```

### Modal Footer (IMPORTANT)
**Always use standard Tabler classes for modal footers** - custom button styling causes theme issues (invisible in light/dark mode).

```html
<!-- CORRECT: Use standard Tabler modal-footer and btn-primary -->
<div class="modal-footer">
    <a @onclick="Cancel" class="btn btn-ghost-secondary">
        @CommonLocalizer["Cancel"]
    </a>
    <button type="submit" form="@FormId" disabled="@OkDisabled" class="btn btn-primary">
        <i class="ti ti-check me-1"></i>
        @CommonLocalizer["OK"]
    </button>
</div>

<!-- WRONG: Custom gradient buttons break in light/dark themes -->
<!-- <button class="btn text-white" style="background: linear-gradient(...)"> -->
```

**Why standard classes?**
- `modal-footer` - Tabler handles padding, border, and background for both themes
- `btn-primary` - Automatically visible and styled correctly in light AND dark mode
- `btn-ghost-secondary` - Theme-aware ghost button for cancel actions
- Custom gradients with `text-white` become invisible on light backgrounds

### Design Principles for Dialogs
1. **Visual Hierarchy**: Use headers with icons to establish context
2. **Color Coding**: Semantic colors for debit/credit, success/error
3. **Spacing**: Generous padding (`p-3`, `gap-3`) for breathing room
4. **Typography**: Monospace fonts for numbers, bold for totals
5. **Rounded Corners**: Use `rounded-3` for modern feel
6. **Subtle Gradients**: Only for decorative icons (avatars), NOT for buttons
7. **Theme Aware**: Use `var(--tblr-*)` variables with fallbacks for adaptive colors
8. **Readable Headers**: For colored table headers, use darker text (`#b45309`, `#047857`) not bright colors
9. **Standard Buttons**: Always use `btn-primary`, `btn-secondary`, `btn-ghost-*` - NEVER custom gradient buttons
