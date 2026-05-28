---
name: avalonia-mvvm
description: Guide for using MVVM Community Toolkit with Avalonia in RemoteViewer.Client. Use when working with ViewModels, data binding, commands, or Avalonia UI patterns.
---

# Avalonia MVVM Patterns (RemoteViewer.Client)

The RemoteViewer.Client uses **CommunityToolkit.Mvvm v8.4.0** with Avalonia's compiled bindings for a modern, low-boilerplate MVVM implementation.

## Core Patterns

### ViewModels
- **Base class**: `ObservableObject` from CommunityToolkit.Mvvm
- **Location**: Co-located with views in `Views/{Feature}/` directories
- **Creation**: Use `IViewModelFactory` with dependency injection for instantiation
- **Constructor injection**: All dependencies injected via constructor (services, logger, etc.)

Main ViewModels:
- `MainViewModel`: Login/connection window (src/RemoteViewer.Client/Views/Main/)
- `ViewerViewModel`: Remote desktop viewer session (src/RemoteViewer.Client/Views/Viewer/)
- `PresenterViewModel`: Remote desktop presenter session (src/RemoteViewer.Client/Views/Presenter/)
- `ChatViewModel`, `ToastsViewModel`: Nested component ViewModels

### Observable Properties

Use `[ObservableProperty]` attribute for automatic property generation:

```csharp
[ObservableProperty]
private string? _statusText = "Connecting...";

[ObservableProperty]
private bool _isConnected;
```

**Pattern**: Private backing field with underscore prefix → Source-generated public property with `PropertyChanged` notifications

### Commands

Use `[RelayCommand]` attribute for automatic command generation:

```csharp
// Synchronous command
[RelayCommand]
private void ToggleFullscreen()
{
    this.IsFullscreen = !this.IsFullscreen;
}

// Async command
[RelayCommand]
private async Task ConnectToDeviceAsync()
{
    var error = await this._hubClient.ConnectTo(username, password);
}

// Command with CanExecute
private bool CanSendMessage() => !string.IsNullOrWhiteSpace(this.MessageInput);

[RelayCommand(CanExecute = nameof(CanSendMessage))]
private async Task SendMessageAsync()
{
    await this.Connection.SendMessageAsync(this.MessageInput);
}
```

**Generated**: `XxxCommand` property (IRelayCommand/IAsyncRelayCommand) with automatic `CanExecuteChanged` handling

### Property Dependencies

Use `[NotifyPropertyChangedFor]` for computed properties:

```csharp
[ObservableProperty]
[NotifyPropertyChangedFor(nameof(CharactersRemaining))]
[NotifyPropertyChangedFor(nameof(IsAtLimit))]
private string _messageInput = string.Empty;

public int CharactersRemaining => this.MaxLength - this.MessageInput.Length;
public bool IsAtLimit => this.MessageInput.Length >= this.MaxLength;
```

### Command State Dependencies

Use `[NotifyCanExecuteChangedFor]` to invalidate commands when properties change:

```csharp
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(ToggleInputCommand))]
[NotifyCanExecuteChangedFor(nameof(SendCtrlAltDelCommand))]
private bool _isInputBlockedByPresenter;

private bool CanToggleInput() => !this.IsInputBlockedByPresenter;

[RelayCommand(CanExecute = nameof(CanToggleInput))]
private async Task ToggleInputAsync()
{
    this.IsInputEnabled = !this.IsInputEnabled;
}
```

### Property Change Handlers

Use partial methods for custom logic on property changes:

```csharp
[ObservableProperty]
private bool _isOpen;

partial void OnIsOpenChanged(bool value)
{
    if (value)
        this.HasUnreadMessages = false;
}
```

## View-ViewModel Binding

### XAML Binding
Use `x:DataType` for compiled bindings (Avalonia 11.3 feature):

```xml
<Window x:DataType="vm:MainViewModel">
    <!-- Property binding -->
    <TextBlock Text="{Binding StatusText}"/>

    <!-- Command binding -->
    <Button Command="{Binding ConnectCommand}"/>
</Window>
```

### Code-Behind Pattern
Type-safe ViewModel access with event management:

```csharp
public partial class MainView : Window
{
    private MainViewModel? _viewModel;

    private void Window_DataContextChanged(object? sender, EventArgs e)
    {
        // Unsubscribe from old ViewModel
        if (this._viewModel is not null)
            this._viewModel.RequestShowMainView -= this.ViewModel_RequestShowMainView;

        this._viewModel = this.DataContext as MainViewModel;

        // Subscribe to new ViewModel
        if (this._viewModel is not null)
            this._viewModel.RequestShowMainView += this.ViewModel_RequestShowMainView;
    }
}
```

**Pattern**: Always unsubscribe from old ViewModel events to prevent memory leaks

## Dependency Injection

### Service Registration
Services registered in `ServiceRegistration.cs`:

```csharp
services.AddSingleton<IViewModelFactory, ViewModelFactory>();
services.AddSingleton<IClipboardService, AvaloniaClipboardService>();
services.AddSingleton<IDispatcher, AvaloniaDispatcher>();
services.AddSingleton<ConnectionHubClient>();
```

### ViewModel Factory Pattern
Use `IViewModelFactory` for creating ViewModels with DI:

```csharp
public interface IViewModelFactory
{
    MainViewModel CreateMainViewModel();
    ViewerViewModel CreateViewerViewModel(Connection connection);
}

public class ViewModelFactory(IServiceProvider serviceProvider) : IViewModelFactory
{
    public MainViewModel CreateMainViewModel() =>
        ActivatorUtilities.CreateInstance<MainViewModel>(serviceProvider);

    public ViewerViewModel CreateViewerViewModel(Connection connection) =>
        ActivatorUtilities.CreateInstance<ViewerViewModel>(serviceProvider, connection);
}
```

**Usage**: Factory methods support both DI parameters and runtime parameters (e.g., `Connection`)

## Thread Safety

Use `IDispatcher` service for thread-safe UI updates:

```csharp
private readonly IDispatcher _dispatcher;

// From background thread
this._dispatcher.Post(() =>
{
    this.StatusText = "Connected";
    this.IsConnected = true;
});
```

**Pattern**: Always use dispatcher when updating UI properties from non-UI threads

## ViewModel Communication

Use standard .NET events for ViewModel-to-View communication:

```csharp
// In ViewModel
public event EventHandler? CloseRequested;
public event EventHandler? RequestShowMainView;

private void RaiseCloseRequest()
{
    this.CloseRequested?.Invoke(this, EventArgs.Empty);
}

// In View code-behind
private void ViewModel_CloseRequested(object? sender, EventArgs e)
{
    this.Close();
}
```

## Resource Cleanup

ViewModels implement `IAsyncDisposable` for proper cleanup:

```csharp
public async ValueTask DisposeAsync()
{
    if (this._disposed)
        return;

    this._disposed = true;

    // Cleanup resources
    await this.Connection.DisconnectAsync();

    // Unsubscribe from events
    this.Connection.ParticipantsChanged -= this.Connection_ParticipantsChanged;

    GC.SuppressFinalize(this);
}
```

**Important**: Always unsubscribe from events in Dispose to prevent memory leaks

## Key Benefits

- **Minimal boilerplate**: Source generators eliminate repetitive code
- **Type-safe**: Compiled bindings catch errors at build time
- **Testable**: Full dependency injection support
- **Performant**: Avalonia compiled bindings with zero reflection
- **Maintainable**: Consistent patterns across all ViewModels
