---
name: dialog-pattern
description: Use this skill when implementing modal dialog patterns for simple and complex create/update operations using a localized base class and fluent API extensions.
---

# Skill body

## Dialog Pattern Skills

### Overview
- **Dialog Pattern** should be used for **SIMPLE** create and update operations.
- **Form Editor Pattern** should be used for **COMPLEX** create and update operations.
- Always **clone** the object before passing it to the dialog to ensure the original object is not modified if the user cancels the dialog.
- **Persistence** should be handled in the parent component, not within the dialog.
- The **parent component** should update the list after persistence.
- **Business logic** should **NOT** be implemented in the parent component or the dialog.
- Use the `Operation` name for committing a unit of work session.
- Utilize the base class `LocalizedDialogBase<ItemType, ResourceType>`.

### Base Class Properties and Methods
The `LocalizedDialogBase<TItem, TResource>` base class provides the following properties and methods:
- `Item`: The data object passed to the dialog.
- `DataContext`: Database context for queries.
- `RequestContext`: Request context (do NOT re-inject).
- `Localizer`: Localization for `TResource`.
- `CommonLocalizer`: Common localization strings.
- `FormId`: Unique form ID for submit binding.
- `OkClick(item)`: Call to return the result and close the dialog.
- `Cancel()`: Call to cancel and close the dialog.
- `OkDisabled`: Virtual property to control the OK button state.

### Example Implementation
```csharp
// Sample MotorbikeDialog.razor
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
        { Name: "" or null } => true,
        _ => false
    };
}
```

### Usage
- To implement a dialog for editing a `Motorbike`, create a Razor component that inherits from `LocalizedDialogBase<Motorbike, MotorbikeDialog>`.
- Ensure to handle the form submission and cancellation appropriately using the provided methods.