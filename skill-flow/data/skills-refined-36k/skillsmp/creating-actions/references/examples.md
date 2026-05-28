# Action Examples

Complete working examples demonstrating Action patterns.

## Contents

- [Simple Action (No Dependencies)](#simple-action-no-dependencies)
- [Action with Dependencies](#action-with-dependencies)
- [Action with Exception Handling](#action-with-exception-handling)
- [Action Composition with Transaction](#action-composition-with-transaction)

---

## Simple Action (No Dependencies)

```php
<?php

declare(strict_types=1);

namespace App\Actions\User;

use App\Models\User;

final class DeleteUserAction
{
    public function handle(User $user): bool
    {
        if ($user->avatar_path) {
            Storage::disk('public')->delete($user->avatar_path);
        }

        return (bool) $user->delete();
    }
}
```

---

## Action with Dependencies

```php
<?php

declare(strict_types=1);

namespace App\Actions\Auth;

use App\DTOs\Auth\RegisterData;
use App\Models\User;
use App\Support\Localisation\Localisation;
use Illuminate\Auth\Events\Registered;
use Illuminate\Support\Facades\Hash;

final readonly class RegisterUserAction
{
    public function __construct(
        private Localisation $localisation
    ) {}

    public function handle(RegisterData $data): User
    {
        $user = User::query()->create([
            'name' => $data->name,
            'email' => $data->email,
            'language' => $this->getLanguage($data->language),
            'password' => Hash::make($data->password),
        ]);

        event(new Registered($user));

        return $user;
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

---

## Action with Exception Handling

```php
<?php

declare(strict_types=1);

namespace App\Actions\Auth;

use App\Models\User;
use App\Support\TwoFactorAuthentication\Contracts\TwoFactorAuthentication;
use Illuminate\Support\Collection;
use Throwable;

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
            return false; // Graceful failure
        }
    }
}
```

---

## Action Composition with Transaction

```php
<?php

declare(strict_types=1);

namespace App\Actions\Order;

use App\Actions\Inventory\ReserveInventoryAction;
use App\Actions\Payment\ProcessPaymentAction;
use App\Actions\Notification\SendOrderConfirmationAction;
use App\DTOs\Order\CreateOrderData;
use App\Models\Order;
use Illuminate\Support\Facades\DB;

final readonly class CreateOrderAction
{
    public function __construct(
        private ReserveInventoryAction $reserveInventory,
        private ProcessPaymentAction $processPayment,
        private SendOrderConfirmationAction $sendConfirmation
    ) {}

    public function handle(CreateOrderData $data): Order
    {
        return DB::transaction(function () use ($data) {
            // Create order
            $order = Order::create([
                'user_id' => $data->userId,
                'total' => $data->total,
            ]);

            // Reserve inventory (must succeed)
            $this->reserveInventory->handle($order, $data->items);

            // Process payment (must succeed)
            $this->processPayment->handle($order, $data->paymentMethod);

            // Send confirmation (fire and forget, outside transaction)
            dispatch(fn () => $this->sendConfirmation->handle($order));

            return $order;
        });
    }
}
```
