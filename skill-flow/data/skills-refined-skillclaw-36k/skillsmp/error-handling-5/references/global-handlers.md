# Global Handlers

## Hooks

- `AppDomain.CurrentDomain.UnhandledException`
- `Application.DispatcherUnhandledException`
- `TaskScheduler.UnobservedTaskException`

## Guidance

- Log with correlation IDs.
- Show a minimal user message and allow recovery when possible.
