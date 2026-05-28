# Navigation Service (ViewModel-first)

## Goal

Provide a lightweight navigation service that swaps the current view model on the shell
without Frame navigation or heavy region managers.

## Interface sketch

```csharp
public interface INavigationService
{
    void NavigateTo<TViewModel>() where TViewModel : class;
}
```

## Shell VM pattern

- Shell VM owns `CurrentViewModel`.
- Navigation service resolves the target VM and assigns it.
- Views are mapped via DataTemplates.

```csharp
public class ShellViewModel : ObservableObject
{
    private object? _currentViewModel;
    public object? CurrentViewModel
    {
        get => _currentViewModel;
        set => SetProperty(ref _currentViewModel, value);
    }
}
```

## Notes

- Use DI to construct view models and services.
- Keep navigation synchronous unless view models require async loading.
