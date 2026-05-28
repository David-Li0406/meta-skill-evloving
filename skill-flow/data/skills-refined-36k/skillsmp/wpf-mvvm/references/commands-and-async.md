# Commands and Async

## Command usage

- Use `[RelayCommand]` for sync handlers.
- Use `[RelayCommand(IncludeCancelCommand = true)]` for cancellable async work.
- Keep command methods small; move logic to services.

## Async patterns

- Use `Task` return values for async commands.
- Avoid `async void` except for event handlers.
- Surface busy state with an `IsBusy` property.

## Error handling

- Catch expected exceptions and expose error state on the VM.
- Avoid UI message boxes inside the VM; emit notifications via services.
