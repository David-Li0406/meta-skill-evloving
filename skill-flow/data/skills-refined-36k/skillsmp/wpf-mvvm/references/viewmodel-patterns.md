# ViewModel Patterns

## Structure

- One view model per view.
- Keep view model constructors small; use services for behavior.
- Prefer injected services over static access.

## Naming

- `ShellViewModel`, `WidgetViewModel`, `SettingsViewModel`.
- Avoid suffixes like `Vm` if you already use `ViewModel`.

## State boundaries

- Use private fields with `[ObservableProperty]`.
- Expose read-only collections when possible.
- Avoid holding raw UI elements in state.
