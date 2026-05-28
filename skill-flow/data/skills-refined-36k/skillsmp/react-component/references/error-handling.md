# Error Handling & Reporting Strategy

A robust application anticipates failures and handles them gracefully. This guide provides a unified strategy for classifying, handling, and reporting errors within the React application, inspired by the principles established in the Pod Network TypeScript SDK.

## Table of Contents

1. [Guiding Principles](#guiding-principles)
2. [Error Types: User-Facing vs. Application Errors](#error-types-user-facing-vs-application-errors)
3. [Catching Application Errors with Error Boundaries](#catching-application-errors-with-error-boundaries)
4. [Structured Logging with LogTape](#structured-logging-with-logtape)
5. [Displaying User-Facing Errors](#displaying-user-facing-errors)

---

## Guiding Principles

- **Fail Fast and Clear:** Errors should be caught and handled as soon as they occur. Error messages, both for users and developers, must provide context about what failed, why, and what to do next.
- **Errors are State:** Treat errors as a predictable state of your components and application, just like `loading` or `empty` states.
- **Never Leak Internal Details:** User-facing error messages must be simple, actionable, and free of stack traces, internal codes, or sensitive information.
- **Report, Don't Just `console.log`:** All unexpected errors must be reported to a structured logging service. Never use `console.error` directly for application-level errors.

---

## Error Types: User-Facing vs. Application Errors

Properly handling errors starts with classifying them.

### 1. User-Facing Errors

These are predictable, often recoverable errors that arise from user interaction or expected system conditions. They are part of the normal application flow.

- **Examples:**
  - Invalid form input (e.g., "Invalid address format").
  - Failed API request due to network issues (`NetworkError` with `retryable: true`).
  - Blockchain transaction rejected by the user.
  - Business logic failure (e.g., "Insufficient funds").
- **How to Handle:**
  - Handle them locally within the component or hook where they occur.
  - Update the component's state to display a user-friendly message.
  - Use inline validation, toasts, or specific error states.

### 2. Application Errors

These are unexpected bugs or system failures. They represent a deviation from the expected application flow and are generally not recoverable by the user.

- **Examples:**
  - A React component fails to render due to a JavaScript error (`TypeError: Cannot read properties of undefined`).
  - An API response is malformed in a way that bypasses Zod validation.
  - State management logic enters an impossible state.
- **How to Handle:**
  - Catch them globally using an **Error Boundary**.
  - Display a generic fallback UI to the user (e.g., "Something went wrong").
  - Report the full error with stack trace and context to a logging service.

---

## Catching Application Errors with Error Boundaries

An Error Boundary is a React component that catches JavaScript errors anywhere in its child component tree, logs those errors, and displays a fallback UI. This prevents a single component crash from taking down the entire application.

### Example Reusable Error Boundary

```tsx
// src/components/common/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react'
import { getLogger } from '@logtape/logtape'

const logger = getLogger(['app', 'error-boundary'])

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logger.error('uncaught_render_error', {
      error: error.message,
      componentStack: errorInfo.componentStack,
    })
  }

  public render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Something went wrong.</h1>
    }

    return this.props.children
  }
}
```

### Usage

Wrap your main application layout or specific high-risk features with the `ErrorBoundary`.

```tsx
// src/app/layout.tsx
import { ErrorBoundary } from '@/components/common/ErrorBoundary'
import { GlobalErrorFallback } from '@/components/common/GlobalErrorFallback'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary fallback={<GlobalErrorFallback />}>{children}</ErrorBoundary>
      </body>
    </html>
  )
}
```

---

## Structured Logging with LogTape

As established in the [Security Guide](security.md), **never use `console.*` directly.** All logging must be done via LogTape to ensure logs are structured, namespaced, and stripped of sensitive data in production.

### Creating a Logger

Create namespaced loggers for different features or components.

```ts
import { getLogger } from '@logtape/logtape'

// In a feature hook
const logger = getLogger(['app', 'hooks', 'useRevenue'])

// In a component
const logger = getLogger(['app', 'components', 'RevenueCard'])
```

### Logging Errors

When you `catch` an error, log it with structured context.

```ts
// In a TanStack Query queryFn
async function fetchRevenue() {
  const logger = getLogger(['app', 'api', 'revenue'])
  try {
    const response = await api.get('/revenue')
    return revenueSchema.parse(response.data)
  } catch (error) {
    logger.error('fetch_revenue_failed', {
      // Provide context, but NEVER sensitive data
      error: error instanceof Error ? error.message : String(error),
      // Add any relevant non-sensitive context, like request IDs
    })
    // Re-throw the error so TanStack Query can handle it
    throw new Error('Failed to fetch revenue data.')
  }
}
```

---

## Displaying User-Facing Errors

Choose the right UI pattern for the error.

| Pattern                   | When to Use                                                                                                              | Example                                                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Inline Message**        | Form validation, contextual errors tied to a specific element.                                                           | Displaying "Invalid address" below a text input. Use `aria-describedby` to link the error message to the input for screen readers. |
| **Component Error State** | When a component's data fetching fails. This is the `state="error"` from the [Container/Presenter Pattern](patterns.md). | A chart component shows a message like "Could not load chart data. Please try again."                                              |
| **Toast / Alert**         | Non-blocking feedback for asynchronous actions (e.g., a background save fails).                                          | A toast appears saying "Failed to update settings."                                                                                |
| **Dialog / Modal**        | Critical errors that halt the user's workflow and require a specific action or acknowledgement.                          | "Your session has expired. Please log in again to continue."                                                                       |
