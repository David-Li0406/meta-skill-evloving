---
name: refactor
description: Guide service layer extraction from fat controllers. Use when refactoring complex controllers, extracting business logic to services, creating action classes, or improving code organization. Auto-triggers on "refactor", "extract service", "too complex", "clean up controller", "service layer".
---

# Service Layer Refactoring Guide

You are helping refactor RentPath code from fat controllers to a clean service layer architecture.

## Arguments

This skill accepts optional arguments to specify what to refactor:

| Usage                                      | Behavior                                    |
| ------------------------------------------ | ------------------------------------------- |
| `/refactor`                                | Interactive - ask what to refactor          |
| `/refactor ApplicationController`          | Refactor that specific controller           |
| `/refactor ApplicationController::approve` | Refactor specific method                    |
| `/refactor app/Http/Controllers/`          | Analyze all controllers, suggest priorities |
| `/refactor to service`                     | Extract current context to a service class  |
| `/refactor to action`                      | Extract to a single-purpose action class    |

**Argument interpretation:**

- **Controller name** - Focus on that controller
- **Controller::method** - Focus on extracting that specific method
- **Path** - Analyze complexity across files in path
- **Target** (`to service`, `to action`) - Specify extraction pattern

## Before You Start

1. **Read the current architecture**: `docs/architecture/overview.md`
2. **Understand the target state**: Controllers handle HTTP, Services handle business logic
3. **Check existing patterns**: Look for any existing services in `app/Services/`

## Tools to Use

| Task               | Tool   | Command/Action                                  |
| ------------------ | ------ | ----------------------------------------------- |
| Analyze controller | `Read` | Read the controller file                        |
| Find usages        | `Grep` | Search for method calls                         |
| Check model        | `Read` | Read related model files                        |
| Create service     | `Bash` | `php artisan make:class Services/[Name]Service` |
| Run tests          | `Bash` | `php artisan test --filter=[Controller]`        |

## Extraction Decision Tree

```
Controller method > 50 lines?
├─ Yes -> Extract to Service
└─ No -> Is logic reused elsewhere?
    ├─ Yes -> Extract to Service
    └─ No -> Does it involve multiple models?
        ├─ Yes -> Extract to Service
        └─ No -> Are there complex business rules?
            ├─ Yes -> Extract to Service
            └─ No -> Keep in Controller (simple CRUD)
```

## Step-by-Step Process

### 1. Analyze the Controller

```bash
# Check file size and complexity
wc -l app/Http/Controllers/[Name]Controller.php

# List all public methods
grep -n "public function" app/Http/Controllers/[Name]Controller.php
```

**Key questions:**

- What are the main responsibilities?
- Which methods have business logic vs HTTP handling?
- What models are touched?

### 2. Identify Service Boundaries

Group related operations:

```
ApplicationService
├── submit()         # Business logic for submission
├── approve()        # Approval workflow
├── reject()         # Rejection workflow
├── withdraw()       # Withdrawal logic
└── scheduleVisit()  # Visit scheduling

PropertyService
├── publish()        # Publishing workflow
├── createDraft()    # Draft creation
├── updateSpecs()    # Spec updates
└── archive()        # Archival logic
```

### 3. Create the Service Class

```bash
php artisan make:class Services/ApplicationService --no-interaction
```

**Service structure:**

```php
<?php

namespace App\Services;

use App\Models\Application;
use App\Models\TenantProfile;

class ApplicationService
{
    /**
     * Submit an application for review.
     */
    public function submit(Application $application): void
    {
        // Validate business rules
        $this->validateCanSubmit($application);

        // Create profile snapshot
        $this->createSnapshot($application);

        // Update status
        $application->update([
            'status' => 'submitted',
            'submitted_at' => now(),
        ]);

        // Dispatch events (future)
        // ApplicationSubmitted::dispatch($application);
    }

    private function validateCanSubmit(Application $application): void
    {
        if ($application->status !== 'draft') {
            throw new \InvalidArgumentException('Only draft applications can be submitted');
        }
    }

    private function createSnapshot(Application $application): void
    {
        $profile = $application->tenantProfile;

        $application->update([
            'snapshot_first_name' => $profile->user->first_name,
            'snapshot_last_name' => $profile->user->last_name,
            // ... more fields
        ]);
    }
}
```

### 4. Refactor the Controller

**Before (fat controller):**

```php
public function submit(Application $application)
{
    // 50+ lines of business logic...
}
```

**After (thin controller):**

```php
public function __construct(
    private ApplicationService $applicationService
) {}

public function submit(Application $application): RedirectResponse
{
    $this->applicationService->submit($application);

    return redirect()
        ->route('applications.show', $application)
        ->with('success', __('Application submitted successfully'));
}
```

### 5. Update Tests

```php
// Test the service directly
test('application service submits draft application', function () {
    $application = Application::factory()->draft()->create();
    $service = new ApplicationService();

    $service->submit($application);

    expect($application->fresh()->status)->toBe('submitted');
});

// Test the controller integration
test('submit endpoint uses service', function () {
    $application = Application::factory()->draft()->create();

    $response = $this->actingAs($application->tenantProfile->user)
        ->post("/applications/{$application->id}/submit");

    $response->assertRedirect();
    expect($application->fresh()->status)->toBe('submitted');
});
```

## Priority Refactoring Targets

Based on codebase analysis:

| Controller                | Size  | Priority | Suggested Services                                 |
| ------------------------- | ----- | -------- | -------------------------------------------------- |
| `ApplicationController`   | 115KB | High     | `ApplicationService`, `ApplicationSnapshotService` |
| `PropertyController`      | 35KB  | Medium   | `PropertyService`, `PropertyPublishingService`     |
| `TenantProfileController` | 30KB  | Medium   | `TenantProfileService`, `VerificationService`      |

## Action Classes (Single Operations)

For complex single-purpose operations, use Action classes:

```bash
php artisan make:class Actions/ApproveApplication --no-interaction
```

```php
<?php

namespace App\Actions;

use App\Models\Application;

class ApproveApplication
{
    public function execute(Application $application, array $data): void
    {
        $application->update([
            'status' => 'approved',
            'approved_at' => now(),
            'approved_by_user_id' => auth()->id(),
            'approval_notes' => $data['notes'] ?? null,
        ]);
    }
}
```

## Documentation References

- `docs/architecture/overview.md` - Current architecture
- `docs/patterns/wizard.md` - Wizard-specific patterns
- `docs/modules/applications.md` - Application domain logic
- `docs/modules/properties.md` - Property domain logic

## Checklist

- [ ] Analyzed controller complexity
- [ ] Identified service boundaries
- [ ] Created service class(es)
- [ ] Moved business logic to service
- [ ] Controller only handles HTTP concerns
- [ ] Injected service via constructor
- [ ] Updated/created tests
- [ ] Verified existing tests pass
