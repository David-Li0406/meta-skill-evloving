# Error Handling & Reporting Strategy

A robust application anticipates failures and handles them gracefully. This guide provides a unified strategy for classifying, handling, and reporting errors in our TypeScript projects.

## Table of Contents

- [Guiding Principles](#guiding-principles)
- [Error Types: User-Facing vs. Internal Errors](#error-types-user-facing-vs-internal-errors)
- [Using Result or Effect for Errors](#using-result-or-effect-for-errors)
- [Transforming and Propagating Errors](#transforming-and-propagating-errors)
- [Global Error Handling](#global-error-handling)
- [Logging and Reporting Errors](#logging-and-reporting-errors)

## Guiding Principles

- **Never Fail Silently**: Every error should either be handled or explicitly propagated. There should be no swallowed exceptions or ignored promise rejections.
- **Predictability**: Use structured error handling (like `Result` types or Effect error channels) instead of throwing exceptions in most of our code. This makes the flow predictable (no surprise `catch` needed mid-stack).
- **User-Facing vs. Internal**: Distinguish errors that can be shown to users from internal errors meant for logs. Users should get friendly messages, internal logs get technical details.
- **Single Source of Truth**: Define error classes or error codes in a central place (or at least per feature module) so they can be consistently caught and handled.
- **Fail Fast, Fail Loud in Dev**: In development, it’s better to throw or log loudly when unexpected errors happen (to catch issues early). In production, handle errors gracefully and provide fallbacks where possible.

## Error Types: User-Facing vs. Internal Errors

### User-Facing Errors

These are errors arising from user input or expected error cases (e.g., invalid form data, unable to find entity by ID). They should:

- Be captured in a `Result` with a specific error variant, or as a custom error class.
- Include a user-friendly message (e.g., "The username is already taken. Please choose another.").
- Not include internal stack traces or sensitive info.
- Often these are validation errors or business rule violations.

**Example**: A function returns `Result.Err(new UsernameTakenError())`. The presentation layer catches this and displays the friendly message from the error.

### Internal/Application Errors

These are unexpected or system errors (exceptions, failed network calls, etc.). They should:

- Be converted to a controlled error type if possible at a boundary (e.g., wrap a low-level error in an `InternalError` with context).
- Include technical context for logs (stack trace, error code, raw error message).
- Usually not surface directly to the user. The user might just see "Something went wrong, please try again later." while logs contain the detailed error for developers.

We often introduce an `InternalError` or use an error wrapper (like `Data.TaggedError` in Effect[5]) to represent these, ensuring they carry a `cause`.

## Using Result or Effect for Errors

Rather than throwing exceptions through our codebase:

- **Use `Result`**: Functions that can fail return `Result<SuccessType, FailureType>` (e.g., using True Myth’s `Result` or similar). The failure carries an error object or error code.
- **Use `Effect`**: When using the Effect library, represent errors in the effect’s type (Effect’s `Cause` or typed error). For example, `Effect.tryPromise({ ..., catch: () => new GetUserError() })` wraps a failure in a typed error[6].
- This approach forces callers to handle the error case (since the type is `Result` or an `Effect` that could fail). It’s explicit and checked by the compiler, unlike exceptions.

**`neverthrow` vs. `True Myth` vs. `Effect`**: All provide a way to avoid throwing:

- True Myth’s `Result` and `Maybe` give methods like `.unwrapOr`, `.mapErr` etc., to handle gracefully.
- `neverthrow`’s `Result` is similar; since we are using True Myth (and Effect’s `Either`), we don’t need `neverthrow`.
- Effect’s built-in error channel is preferred in asynchronous or complex flows, because it also handles fiber interruptions, etc.

## Transforming and Propagating Errors

When an error occurs at a low level (e.g., database query failed):

- **Catch at Low Level**: Catch the raw error (if using `try/await` or promise) and wrap it in a domain-specific error. For example, catch a MongoDB exception and throw/return a `DatabaseError` with the original error as `cause`.
- **Propagate Up**: The calling function now receives a `Result.Err(DatabaseError)` or an `Effect` that fails with `DatabaseError`. It can add context and propagate further up.
- **Avoid Losing Information**: Always preserve the original error message or stack in some form (as a `cause` property). This is crucial for debugging. If using Effect, use `Cause.annotate` or similar to add context rather than replacing the error entirely.

**Example transformation (without Effect)**:

```ts
function getUserById(id: string): Result<User, AppError> {
  try {
    const record = db.findById(id);
    if (!record) {
      return Err(new NotFoundError('User', id));
    }
    return Ok(toUser(record));
  } catch (e) {
    return Err(new DatabaseError('Failed to fetch user', e));
  }
}
```

Here `NotFoundError` is a user-facing error (maybe status 404), whereas `DatabaseError` is internal (500).

In an Effect context, the same logic would use `Effect.tryPromise` with a structured error as shown in Effect docs[2].

## Global Error Handling

At the top level of an application (for instance, an Express error middleware, or the outermost React error boundary, or the `catch` method in Oclif):

- Catch any unhandled exceptions or rejections. These represent cases we didn’t anticipate with `Result` or `Effect`.
- Log the detailed error (with stack) for developers (using our structured logging with redaction as needed).
- Convert to a generic user message:
  - **API**: respond with a 500 and generic JSON error.
  - **CLI**: print a user-friendly message (and maybe an option to run with `--verbose` to see more).
  - **UI**: show an error toast/modal saying “Unexpected error, please try again.”

Centralizing this logic prevents leaking stack traces or raw errors to end-users. It also ensures we don’t forget to log something critical.

For Effect, typically you would catch errors at the end of the fiber. For example, if using `Effect.runPromise(program)`, wrap it in a `try/catch` or use `.catchAll` on the Effect to handle any failure in one spot[7].

## Logging and Reporting Errors

Leverage our logging system (LogTape) to record errors:

- Use `logger.error()` with structured data. E.g., `logger.error({ err }, "Failed to process payment")` where `err` is the error object. This way we capture message, stack, plus context[8][9].
- Use `@logtape/sentry` integration to send exceptions to Sentry in production. For critical parts, `logger.fatal(error)` might trigger a Sentry report automatically if configured.
- Ensure sensitive fields in errors are redacted (configure `@logtape/redaction` patterns for things like credit card numbers, emails, etc. in error messages[10][11]).

**Examples**:

- In Express, in the error middleware:
  `logger.error({ err: error, reqId: req.id }, "Unhandled error in request");`
  The `reqId` helps tie the error to a specific request, and `err` includes stack trace.
- In a CLI `catch`, you might do:

  ```ts
  if (error instanceof UserFacingError) {
    this.log(error.message);
  } else {
    logger.error({ err: error }, "CLI command failed");
    this.error("Unexpected error occurred. Run with --verbose for details.");
  }
  ```

  This prints minimal info to user but logs the full error internally.

**Categorize logging by severity**:

- Expected but handled errors (like validation failures) might only be `logger.info` or `warn` (since they are not system issues).
- Unexpected errors are `logger.error` or `fatal` if it will crash/stop the service.

By following this strategy, our error handling will be consistent, our users will receive clear feedback, and we as developers will have the information needed to debug issues in logs and monitoring systems.
