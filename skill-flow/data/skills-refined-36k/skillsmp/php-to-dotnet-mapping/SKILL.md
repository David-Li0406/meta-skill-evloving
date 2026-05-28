---
name: php-to-dotnet-mapping
description: PHP to .NET 10 code mapping reference. Use when converting PHP code patterns to .NET equivalents including framework mapping, authentication, templates (Blade to Razor), packages (Composer to NuGet), and validation rules.
---

# PHP to .NET 10 Mapping Reference

Use this skill when migrating PHP code to .NET 10. It provides direct mappings for common patterns.

## Framework Mapping

| PHP Framework | .NET 10 Equivalent |
|---------------|-------------------|
| Laravel | ASP.NET Core MVC |
| Symfony | ASP.NET Core MVC |
| CodeIgniter | ASP.NET Core Minimal APIs |
| Slim | ASP.NET Core Minimal APIs |
| Lumen | ASP.NET Core Minimal APIs |

## Architecture Pattern Mapping

| PHP Pattern | .NET 10 Equivalent |
|-------------|-------------------|
| MVC (Laravel/Symfony) | ASP.NET Core MVC |
| API-only | ASP.NET Core Web API / Minimal APIs |
| Blade/Twig templates | Razor Views |
| LiveWire | Blazor Server |

## Data Access Mapping

| PHP | .NET 10 |
|-----|---------|
| Eloquent ORM | Entity Framework Core |
| Doctrine ORM | Entity Framework Core |
| PDO | ADO.NET / Dapper |
| Query Builder | LINQ |
| Migrations | EF Core Migrations |

## Authentication Mapping

| PHP | .NET 10 |
|-----|---------|
| Laravel Auth | ASP.NET Core Identity |
| Laravel Sanctum | JWT Bearer Authentication |
| Laravel Passport | IdentityServer / Duende |
| PHP Sessions | ASP.NET Core Session |
| tymon/jwt-auth | Microsoft.AspNetCore.Authentication.JwtBearer |
| Socialite | OAuth2 / Microsoft.Identity.Web |

## Dependency Injection

| PHP | .NET 10 |
|-----|---------|
| Laravel Container | Built-in DI Container |
| Symfony DI | Built-in DI Container |
| Service Providers | IServiceCollection extensions |
| Facades | Injected services |

## Template Syntax Mapping (Blade → Razor)

| Blade (PHP) | Razor (.NET) |
|-------------|--------------|
| `{{ $var }}` | `@Model.Var` or `@var` |
| `{!! $html !!}` | `@Html.Raw(html)` |
| `@if($cond)` | `@if (cond)` |
| `@foreach($items as $item)` | `@foreach (var item in items)` |
| `@extends('layout')` | `@{ Layout = "_Layout"; }` |
| `@section('content')` | `@section Content { }` |
| `@yield('content')` | `@RenderSection("Content")` |
| `@include('partial')` | `<partial name="_Partial" />` |
| `@csrf` | `@Html.AntiForgeryToken()` |
| `@auth` | `@if (User.Identity?.IsAuthenticated == true)` |
| `{{ route('name') }}` | `@Url.Action("Action", "Controller")` |
| `@component` | View Component |

## Package Mapping (Composer → NuGet)

| Composer Package | NuGet Package |
|-----------------|---------------|
| guzzlehttp/guzzle | HttpClient (built-in) |
| stripe/stripe-php | Stripe.net |
| intervention/image | ImageSharp |
| tymon/jwt-auth | Microsoft.AspNetCore.Authentication.JwtBearer |
| predis/predis | StackExchange.Redis |
| aws/aws-sdk-php | AWSSDK.* |
| league/flysystem | Azure.Storage.Blobs |
| phpmailer/phpmailer | Azure.Communication.Email / SendGrid |
| monolog/monolog | Serilog / ILogger |

## Configuration Mapping

| PHP | .NET 10 |
|-----|---------|
| `.env` files | `appsettings.json` + Environment Variables |
| `config/*.php` | `IOptions<T>` pattern |
| `env('KEY')` | `IConfiguration["Key"]` |

## Background Jobs Mapping

| PHP | .NET 10 |
|-----|---------|
| Laravel Queues | Azure Service Bus + BackgroundService |
| Symfony Messenger | Azure Service Bus + BackgroundService |
| Laravel Scheduler | Hosted Services + Cron expressions |
| Artisan commands | .NET CLI tools |

## Validation Mapping

| Laravel Validation | .NET 10 |
|-------------------|---------|
| `required` | `[Required]` |
| `email` | `[EmailAddress]` |
| `max:100` | `[MaxLength(100)]` |
| `min:1` | `[MinLength(1)]` or `[Range(1, ...)]` |
| `unique:table` | Custom validator / EF unique index |
| `confirmed` | `[Compare("PropertyName")]` |
| Form Requests | FluentValidation |

## Code Examples

See the [examples](./examples/) directory for sample conversions:
- [Controller example](./examples/controller-example.cs) - PHP controller to .NET controller
- [Service example](./examples/service-example.cs) - PHP service to .NET service
- [Model example](./examples/model-example.cs) - Eloquent model to EF Core entity
