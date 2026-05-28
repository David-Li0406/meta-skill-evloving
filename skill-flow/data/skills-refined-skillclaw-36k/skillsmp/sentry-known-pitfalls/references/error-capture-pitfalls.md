# Error Capture Pitfalls

## Error Capture Pitfalls

### Pitfall 4: Swallowing Errors
```typescript
// ❌ BAD: Error captured but swallowed
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  // Error swallowed - app continues incorrectly
}

// ✅ GOOD: Capture and handle appropriately
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  throw error; // Or handle properly
}
```

### Pitfall 5: Capturing Non-Errors
```typescript
// ❌ BAD: Capturing strings instead of errors
Sentry.captureException('Something went wrong'); // No stack trace!

// ✅ GOOD: Capture actual Error objects
Sentry.captureException(new Error('Something went wrong'));

// Or use captureMessage for non-errors
Sentry.captureMessage('Something happened', 'info');
```

### Pitfall 6: Double Capture
```typescript
// ❌ BAD: Capturing same error multiple times
app.use((err, req, res, next) => {
  Sentry.captureException(err);
  next(err);
});
app.use(Sentry.Handlers.errorHandler()); // Captures again!

// ✅ GOOD: Single capture point
app.use(Sentry.Handlers.errorHandler()); // Only this
```