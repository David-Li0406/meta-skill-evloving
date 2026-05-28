---
name: dialog-pattern
description: Use this skill for implementing Tabler modal dialog patterns with localized base classes and fluent API extensions for both simple and complex create/update operations.
---

# Dialog Pattern Skills

## Dialog Pattern
- **Dialog Pattern** should be used for **SIMPLE** create and update operations.
- **Form editor Pattern** should be used for **COMPLEX** create and update operations.
- **Clone** the object before passing it to the dialog to prevent modification of the original object if the user cancels the dialog.
- **Persistence** should be handled in the parent component, not in the dialog.
- The **parent component** should update the list after persistence.
- **Business logic** should **NOT** be implemented in the parent component or in the dialog.
- Use the `Operation` name for committing a unit of work session.
- Utilize the base class `LocalizedDialogBase<ItemType, ResourceType>`.

## Base Class Properties and Methods
The `LocalizedDialogBase<TItem, TResource>` base class provides:
- `Item` - The data object passed to the dialog.
- `DataContext` - Database context for queries.
- `RequestContext` - Request context (do NOT re-inject).
- `Localizer` - Localization for TResource.
- `CommonLocalizer` - Common localization strings.
- `FormId` - Unique form ID for submit binding.
- `OkClick(item)` - Call to return result and close the dialog.
- `Cancel()` - Call to cancel and close the dialog.
- `OkDisabled` - Virtual property to control the OK button state.

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

## Beautiful Dialog UI Design

### Dialog Header with Icon
```html
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
```html
<div class="rounded-3 overflow-hidden border">
    <table class="table table-sm mb-0">
        <thead style="background: var(--tblr-bg-surface-secondary, #f1f5f9);">
            <tr>
                <th style="color: var(--tblr-secondary-color, #64748b);">@Localizer["Item"]</th>
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
<div class="d-flex align-items-center justify-content-center gap-2 p-3 rounded-3 mt-3"
     style="background: rgba(16, 185, 129, 0.15); color: #059669; border: 1px solid rgba(16, 185, 129, 0.3);">
    <i class="ti ti-circle-check"></i>
    <span class="fw-semibold">@Localizer["RentalCompleted"]</span>
</div>

<div class="d-flex align-items-center justify-content-center gap-2 p-3 rounded-3 mt-3"
     style="background: rgba(239, 68, 68, 0.15); color: #dc2626; border: 1px solid rgba(239, 68, 68, 0.3);">
    <i class="ti ti-alert-triangle"></i>
    <span class="fw-semibold">@Localizer["DamageReported"]</span>
</div>
```

### Modal Footer
```html
<div class="modal-footer">
    <a @onclick="Cancel" class="btn btn-ghost-secondary">
        @CommonLocalizer["Cancel"]
    </a>
    <button type="submit" form="@FormId" disabled="@OkDisabled" class="btn btn-primary">
        <i class="ti ti-check me-1"></i>
        @CommonLocalizer["OK"]
    </button>
</div>
```

### Design Principles for Dialogs
1. **Visual Hierarchy**: Use headers with icons to establish context.
2. **Color Coding**: Use semantic colors for debit/credit, success/error.
3. **Spacing**: Provide generous padding (`p-3`, `gap-3`) for breathing room.
4. **Typography**: Use monospace fonts for numbers, bold for totals.
5. **Rounded Corners**: Apply `rounded-3` for a modern feel.
6. **Subtle Gradients**: Use gradients only for decorative icons, not for buttons.
7. **Theme Aware**: Utilize `var(--tblr-*)` variables with fallbacks for adaptive colors.
8. **Readable Headers**: Ensure colored table headers have darker text for readability.
9. **Standard Buttons**: Always use `btn-primary`, `btn-secondary`, `btn-ghost-*` - avoid custom gradient buttons.