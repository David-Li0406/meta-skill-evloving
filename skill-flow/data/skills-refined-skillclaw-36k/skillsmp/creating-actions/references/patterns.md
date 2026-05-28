# Advanced Action Patterns

Detailed patterns for complex Action scenarios including composition, transactions, and exception handling.

## Contents

- [Private Helper Methods](#private-helper-methods)
- [Exception Handling](#exception-handling)
- [Action Composition](#action-composition)
- [Database Transactions](#database-transactions)

---

## Private Helper Methods

Extract private methods when:

- Logic is reusable within the Action
- It improves readability by naming a block of logic
- The `handle()` method becomes too long (>20 lines as guideline)

```php
final readonly class RegisterUserAction
{
    public function __construct(
        private Localisation $localisation
    ) {}

    public function handle(RegisterData $data): User
    {
        return User::create([
            'name' => $data->name,
            'email' => $data->email,
            'language' => $this->getLanguage($data->language),
            'password' => Hash::make($data->password),
        ]);
    }

    private function getLanguage(string $locale): string
    {
        $locales = [
            $this->localisation->getIso15897Locale($locale),
            $this->localisation->getLanguageFromLocale($locale),
        ];

        foreach ($locales as $locale) {
            if ($this->localisation->isSupportedLocale($locale)) {
                return $locale;
            }
        }

        return $this->localisation->getDefaultLocale();
    }
}
```

**When NOT to extract:**

- Logic is only 2-3 lines
- Extraction would make code harder to follow
- Consider extracting to a separate Action or Service instead

---

## Exception Handling

**Default approach:** Let exceptions bubble to Laravel's global exception handler

```php
public function handle(UpdateUserAvatarData $data): User
{
    // Let ImageProcessorException bubble up
    $path = ImageProcessor::process($data->image);

    $user->update(['avatar_path' => $path]);
    return $user;
}
```

**Catch only for recoverable errors** with graceful degradation:

```php
final readonly class EnableTwoFactorAction
{
    public function __construct(
        private TwoFactorAuthentication $twoFactorAuthentication
    ) {}

    public function handle(User $user): bool
    {
        try {
            return $user->update([
                'two_factor_secret' => $this->twoFactorAuthentication->generateSecretKey(),
                'two_factor_recovery_codes' => Collection::times(
                    8,
                    fn (): string => $this->twoFactorAuthentication->generateRecoveryCode()
                )->all(),
            ]);
        } catch (Throwable $throwable) {
            report($throwable);
            return false;
        }
    }
}
```

**Document uncaught exceptions** with `@throws`:

```php
/**
 * @throws ImageProcessorException
 */
public function handle(User $user, UpdateUserAvatarData $data): User
{
    $path = ImageProcessor::process($data->image);
    return $user->update(['avatar_path' => $path]);
}
```

**When to catch:**

- Error is recoverable and Action can return a fallback value
- You want to log additional context before re-throwing
- Graceful degradation is acceptable (e.g., optional features)

**When NOT to catch:**

- Validation errors (should be caught in Form Request layer)
- Database constraint violations (let global handler manage)
- Authorization failures (let middleware/policies handle)

---

## Action Composition

Actions can call other Actions for complex workflows:

```php
final readonly class RegisterUserAction
{
    public function __construct(
        private SyncUserRolesAction $syncUserRoles,
        private AssignTeamAction $assignTeam,
        private SendWelcomeEmailAction $sendWelcomeEmail
    ) {}

    public function handle(RegisterData $data): User
    {
        $user = User::create([
            'name' => $data->name,
            'email' => $data->email,
            'password' => Hash::make($data->password),
        ]);

        // Compose multiple Actions for complex workflow
        $this->syncUserRoles->handle($user, $data->roles);
        $this->assignTeam->handle($user, $data->teamId);
        $this->sendWelcomeEmail->handle($user);

        event(new Registered($user));

        return $user;
    }
}
```

**Benefits:**

- Each Action remains single-responsibility
- Easy to test individual Actions in isolation
- Reusable Actions across different workflows
- Clear separation of concerns

---

## Database Transactions

**When to use transactions:**

- Action performs multiple database writes
- Data integrity requires all-or-nothing execution
- Calling multiple Actions that modify the database

```php
final readonly class RegisterUserAction
{
    public function __construct(
        private SyncUserRolesAction $syncUserRoles,
        private AssignTeamAction $assignTeam
    ) {}

    public function handle(RegisterData $data): User
    {
        return DB::transaction(function () use ($data) {
            $user = User::create([
                'name' => $data->name,
                'email' => $data->email,
                'password' => Hash::make($data->password),
            ]);

            // Both must succeed or transaction rolls back
            $this->syncUserRoles->handle($user, $data->roles);
            $this->assignTeam->handle($user, $data->teamId);

            return $user;
        });
    }
}
```

**Note:** Database transactions are a general best practice for data consistency, not specific to the Action pattern. Use them whenever multiple database operations must succeed or fail together.
