---
name: laravel
description: Laravel/PHP coding standards. Use when working on Laravel backend to ensure proper architecture, Eloquent usage, and PHP type safety.
---

# Laravel / PHP

Critical rules for Laravel and PHP development.

---

## PHP & Types

- Follow PSR-12 or project standard
- Always use param + return types; avoid `mixed`/untyped
- Typed properties; no `stdClass` or loose arrays
- Small, single-responsibility methods; composition over inheritance

## DTOs & Enums

- Use DTOs for data crossing boundaries; typed, immutable, no logic
- Named constructors (`fromRequest`, `fromModel`) only when needed
- PHP backed enums for constrained values; no magic strings/ints

## Architecture

- Controllers thin; domain logic in models/services/actions
- DI + container; reuse events/listeners/jobs if project uses them
- Route model binding; resourceful routes when natural
- Form Requests or `$request->validate()` consistently; policies for auth

## Eloquent

- Use relationships, scopes, casts; avoid raw SQL unless necessary
- Prevent N+1 with `with()` / `loadMissing()`

## Views & API

- No DB queries in views; prepare data in controllers
- APIs: proper JSON; use API Resources if project does

## Safety

- No DB schema or env changes unless requested
- Use `config()` for tunables; no hardcoded secrets
