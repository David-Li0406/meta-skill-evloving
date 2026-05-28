# Validation

## Toolkit approach

- Derive from `ObservableValidator`.
- Use `ValidateAllProperties()` before save operations.
- Expose validation results for the view to display.

## Attribute examples

```csharp
public partial class SettingsViewModel : ObservableValidator
{
    [ObservableProperty]
    [Required]
    [MinLength(3)]
    private string _userName = string.Empty;
}
```

## Notes

- Keep validation rules in the VM, not in XAML.
- Prefer data annotations for simple rules; use custom validation for complex rules.
