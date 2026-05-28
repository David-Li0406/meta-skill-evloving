---
title: Create Custom Error Classes
impact: HIGH
impactDescription: Enables precise error handling and better debugging
tags: errors, exceptions, classes, debugging
---

## Create Custom Error Classes

Generic Error objects lack context. Custom error classes enable precise catch handling and include relevant debugging information.

**Incorrect (generic errors):**

```javascript
function fetchUser(id) {
  if (!id) {
    throw new Error('Invalid');
  }
  // ...
}

try {
  await fetchUser(null);
} catch (error) {
  // Can't distinguish error types
  // error.message is just 'Invalid'
  console.error(error);
}
```

**Correct (custom error classes):**

```javascript
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

class NetworkError extends Error {
  constructor(url, status, message) {
    super(message);
    this.name = 'NetworkError';
    this.url = url;
    this.status = status;
  }
}

class NotFoundError extends Error {
  constructor(resource, id) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
    this.resource = resource;
    this.id = id;
  }
}

// Usage
async function fetchUser(id) {
  if (!id) {
    throw new ValidationError('id', 'User ID is required');
  }

  const response = await fetch(`/api/users/${id}`);

  if (response.status === 404) {
    throw new NotFoundError('User', id);
  }

  if (!response.ok) {
    throw new NetworkError(`/api/users/${id}`, response.status, 'Failed to fetch user');
  }

  return response.json();
}

// Precise error handling
try {
  await fetchUser(userId);
} catch (error) {
  if (error instanceof ValidationError) {
    showFieldError(error.field, error.message);
  } else if (error instanceof NotFoundError) {
    showNotFound(error.resource);
  } else if (error instanceof NetworkError) {
    showNetworkError(error.status);
  } else {
    throw error; // Re-throw unexpected errors
  }
}
```
