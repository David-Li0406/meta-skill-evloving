# API Controllers

Patterns for building REST API controllers that return JSON responses.

## Contents

- [Directory Structure](#directory-structure)
- [Key Differences from Web Controllers](#key-differences-from-web-controllers)
- [Response Types](#response-types)
- [Status Codes](#status-codes)
- [Exception Handling](#exception-handling)

---

## Directory Structure

```
app/Http/Controllers/Api/
├── V1/
│   ├── UserController.php
│   └── Auth/
│       └── AuthController.php
└── V2/
    └── UserController.php
```

**Routes:**

```php
// routes/api.php
Route::prefix('v1')->group(function (): void {
    Route::apiResource('users', App\Http\Controllers\Api\V1\UserController::class);
});
```

**Note:** This codebase is primarily Inertia.js. Only create API controllers when building a REST API.

---

## Key Differences from Web Controllers

| Aspect         | Web (Inertia)                          | API                        |
| -------------- | -------------------------------------- | -------------------------- |
| Returns        | `Inertia\Response`, `RedirectResponse` | `JsonResponse`, `Resource` |
| Authentication | Session (`auth:web`)                   | Token (`auth:sanctum`)     |
| Errors         | Redirects with flash messages          | JSON with status codes     |
| CSRF           | Required                               | Not required (stateless)   |

---

## Response Types

### Success with resource (200 OK)

```php
return UserResource::make($user);
```

### Created (201)

```php
return UserResource::make($user)
    ->response()
    ->setStatusCode(Response::HTTP_CREATED);
```

### No content (204) - for deletes

```php
return response()->noContent();
```

### Collection

```php
return UserResource::collection($users)->response();
```

### Custom JSON

```php
return response()->json([
    'success' => true,
    'data' => $data,
], Response::HTTP_OK);
```

### Validation error (422)

```php
return response()->json([
    'message' => 'Validation failed',
    'errors' => $errors,
], Response::HTTP_UNPROCESSABLE_ENTITY);
```

---

## Status Codes

| Code | Constant                               | Usage                               |
| ---- | -------------------------------------- | ----------------------------------- |
| 200  | `Response::HTTP_OK`                    | Successful GET, PUT, PATCH          |
| 201  | `Response::HTTP_CREATED`               | Successful POST creating a resource |
| 204  | `Response::HTTP_NO_CONTENT`            | Successful DELETE                   |
| 401  | `Response::HTTP_UNAUTHORIZED`          | Not authenticated                   |
| 403  | `Response::HTTP_FORBIDDEN`             | Authenticated but not authorized    |
| 404  | `Response::HTTP_NOT_FOUND`             | Resource not found                  |
| 422  | `Response::HTTP_UNPROCESSABLE_ENTITY`  | Validation failed                   |
| 500  | `Response::HTTP_INTERNAL_SERVER_ERROR` | Server error                        |

---

## Exception Handling

```php
use Illuminate\Validation\ValidationException;

public function store(
    StoreRequest $request,
    CreateAction $action
): RedirectResponse {
    try {
        $result = $action->handle($request->toDTO());
    } catch (SpecificException $e) {
        report($e);  // Log for debugging

        throw ValidationException::withMessages([
            'field' => __('validation.custom_message'),
        ]);
    }

    return redirect()->route('resource.show', $result);
}
```

**Best Practices:**

- Catch specific exceptions, not generic `Exception`
- Always `report()` exceptions for debugging
- Transform technical exceptions to user-friendly messages
- Re-throw as `ValidationException` for form errors
