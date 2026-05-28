---
name: creating-support-classes
description: Create custom support classes, utilities, and domain-specific services in the Support directory. Use when creating support classes, custom utilities, domain services, or when user mentions support classes, utilities, custom services, or helper services.
---

# Create Support Classes

Create custom support classes, utilities, and domain-specific services in the `app/Support/` directory. Support classes encapsulate reusable functionality that doesn't fit standard Laravel conventions, organized by domain with contracts, facades, and service providers.

## File Structure

Support classes are organized by domain/feature:

```
app/Support/{Domain}/{Name}.php
app/Support/{Domain}/Contracts/{Name}.php
app/Support/{Domain}/Facades/{Name}.php
```

**Examples:**

- `app/Support/Localisation/Localisation.php`
- `app/Support/ImageProcessor/Contracts/ImageProcessor.php`
- `app/Support/TwoFactorAuthentication/Facades/TwoFactorAuthentication.php`

## Core Conventions

### 1. Support Class Structure

```php
<?php

declare(strict_types=1);

namespace App\Support\{Domain};

use Illuminate\Container\Attributes\Config;

final readonly class {Name}
{
    public function __construct(
        #[Config('app.key')] private string $dependency,
    ) {}

    public function methodName(string $param): ReturnType
    {
        // Business logic
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final readonly` for immutable services
- Constructor injection with `#[Config]` attribute
- Full type hints on all methods
- Framework-agnostic where possible

### 2. Contract (Interface) Structure

```php
<?php

declare(strict_types=1);

namespace App\Support\{Domain}\Contracts;

interface {Name}
{
    public function methodName(string $param): ReturnType;
}
```

### 3. Facade Structure

```php
<?php

declare(strict_types=1);

namespace App\Support\{Domain}\Facades;

use App\Support\{Domain}\Contracts\{Name} as {Name}Contract;
use Illuminate\Support\Facades\Facade;

/**
 * @method static ReturnType methodName(string $param)
 */
final class {Name} extends Facade
{
    protected static function getFacadeAccessor(): string
    {
        return {Name}Contract::class;
    }
}
```

## Examples

### Example 1: Simple Support Class

```php
<?php

declare(strict_types=1);

namespace App\Support\Localisation;

use Illuminate\Container\Attributes\Config;
use Illuminate\Http\Request;
use Illuminate\Support\Arr;
use InvalidArgumentException;

/**
 * @phpstan-type  TSupportedLocale array{name: string, nativeName: string, regional: string}
 * @phpstan-type TSupportedLocales array<string, TSupportedLocale>
 */
final readonly class Localisation
{
    /**
     * @param  TSupportedLocales  $supportedLocales
     */
    public function __construct(
        #[Config('app.locale')] private string $defaultLocale,
        #[Config('localisation.supported_locales')] private array $supportedLocales,
        private Request $request
    ) {}

    public function getIso15897Locale(string $locale): string
    {
        return str_replace('-', '_', $locale);
    }

    public function getIso639Locale(string $locale): string
    {
        return str_replace('_', '-', $locale);
    }

    public function getLanguageFromLocale(string $locale): string
    {
        $locale = $this->getIso15897Locale($locale);

        $position = strpos($locale, '_');

        if ($position === 0 || $position === false) {
            return $locale;
        }

        return substr($locale, 0, $position);
    }

    /**
     * @throws InvalidArgumentException
     */
    public function setLocale(string $locale): void
    {
        throw_unless($this->isSupportedLocale($locale), InvalidArgumentException::class, "Locale [{$locale}] is not supported.");

        app()->setLocale($locale);
    }

    /**
     * @return TSupportedLocales
     */
    public function getSupportedLocales(string $format = 'iso15897'): array
    {
        if ($format === 'iso15897') {
            return $this->supportedLocales;
        }

        return Arr::mapWithKeys($this->supportedLocales, fn (array $value, string $key): array => [
            $this->getIso639Locale($key) => [
                ...$value,
                'regional' => $this->getIso639Locale($value['regional']),
            ],
        ]);
    }

    public function getDefaultLocale(): string
    {
        return $this->defaultLocale;
    }

    public function isSupportedLocale(string $locale): bool
    {
        return isset($this->supportedLocales[$locale]);
    }
}
```

### Example 2: Contract and Implementation

```php
<?php

declare(strict_types=1);

namespace App\Support\ImageProcessor\Contracts;

use App\Support\ImageProcessor\Enums\ImageFormat;

interface ImageProcessor
{
    public function resize(string $path, int $width, int $height): string;

    public function encode(string $path, ImageFormat $format): string;

    public function optimize(string $path): string;
}
```

```php
<?php

declare(strict_types=1);

namespace App\Support\ImageProcessor\Providers\Intervention;

use App\Support\ImageProcessor\Contracts\ImageProcessor;
use App\Support\ImageProcessor\Enums\ImageFormat;
use Intervention\Image\ImageManager;

final readonly class InterventionImageProcessor implements ImageProcessor
{
    public function __construct(
        private ImageManager $imageManager
    ) {}

    public function resize(string $path, int $width, int $height): string
    {
        $image = $this->imageManager->read($path);
        $image->scale($width, $height);

        return $image->save();
    }

    public function encode(string $path, ImageFormat $format): string
    {
        $image = $this->imageManager->read($path);

        return $image->encode($format->value);
    }

    public function optimize(string $path): string
    {
        $image = $this->imageManager->read($path);

        return $image->optimize();
    }
}
```

### Example 3: Facade

```php
<?php

declare(strict_types=1);

namespace App\Support\Localisation\Facades;

use App\Support\Localisation\Localisation as LocalisationService;
use Illuminate\Support\Facades\Facade;

/**
 * @method static string getIso15897Locale(string $locale)
 * @method static string getIso639Locale(string $locale)
 * @method static string getLanguageFromLocale(string $locale)
 * @method static void setLocale(string $locale)
 * @method static array getSupportedLocales(string $format = 'iso15897')
 * @method static string getDefaultLocale()
 * @method static bool isSupportedLocale(string $locale)
 */
final class Localisation extends Facade
{
    protected static function getFacadeAccessor(): string
    {
        return LocalisationService::class;
    }
}
```

### Example 4: Custom Exception

```php
<?php

declare(strict_types=1);

namespace App\Support\ImageProcessor\Exceptions;

use Exception;

final class ImageProcessorException extends Exception
{
    public static function encodingFailed(string $reason): self
    {
        return new self("Image encoding failed: {$reason}");
    }

    public static function decodingFailed(string $reason): self
    {
        return new self("Image decoding failed: {$reason}");
    }
}
```

## Binding Support Classes

### In Service Provider

```php
use App\Support\Localisation\Localisation;

#[Override]
public function register(): void
{
    $this->app->singleton(Localisation::class);
}
```

### With Interface

```php
use App\Support\ImageProcessor\Contracts\ImageProcessor;
use App\Support\ImageProcessor\Providers\Intervention\InterventionImageProcessor;

#[Override]
public function register(): void
{
    $this->app->singleton(ImageProcessor::class, InterventionImageProcessor::class);
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't use static methods (use dependency injection)
final class Localisation
{
    public static function getLocale(): string // ❌ Use instance methods
    {
        return app()->getLocale();
    }
}

// Don't skip type hints
public function getLocale() // ❌ Type hint return
{
    return $this->locale;
}

// Don't use mutable state
final class Localisation
{
    private string $locale; // ❌ Use readonly

    public function setLocale(string $locale): void
    {
        $this->locale = $locale;
    }
}

// Don't couple to framework
public function getUser(): User
{
    return auth()->user(); // ❌ Inject dependencies
}
```

### ✅ Do This Instead

```php
// Use dependency injection
final readonly class Localisation
{
    public function __construct(
        #[Config('app.locale')] private string $defaultLocale
    ) {}

    public function getDefaultLocale(): string
    {
        return $this->defaultLocale;
    }
}

// Type hint everything
public function getLocale(): string

// Use readonly classes
final readonly class Localisation

// Inject dependencies
public function __construct(
    private Request $request
) {}

public function getUser(): ?User
{
    return $this->request->user();
}
```

## Quality Standards

- All support classes must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by unit tests
- Framework-agnostic where possible
