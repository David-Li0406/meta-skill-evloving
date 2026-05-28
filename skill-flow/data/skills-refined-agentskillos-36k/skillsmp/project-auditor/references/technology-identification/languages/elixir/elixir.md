# Elixir

**Category**: languages
**Description**: Elixir programming language - dynamic, functional language for building scalable applications on the Erlang VM
**Homepage**: https://elixir-lang.org

## Package Detection

### HEX
- `phoenix`
- `ecto`
- `plug`
- `jason`
- `absinthe`

## Configuration Files

- `mix.exs`
- `mix.lock`
- `.formatter.exs`
- `.credo.exs`
- `.dialyzer_ignore.exs`
- `config/config.exs`
- `config/dev.exs`
- `config/prod.exs`
- `config/runtime.exs`
- `.tool-versions`

## File Extensions

- `.ex`
- `.exs` (Elixir script)
- `.eex` (EEx templates)
- `.heex` (Phoenix HEEx templates)
- `.leex` (LiveView templates)

## Import Detection

### Elixir
**Pattern**: `^defmodule\s+\w+`
- Module declaration
- Example: `defmodule MyApp.User do`

**Pattern**: `^import\s+\w+`
- Import statement
- Example: `import Ecto.Query`

**Pattern**: `^use\s+\w+`
- Use macro
- Example: `use GenServer`

**Pattern**: `^alias\s+\w+`
- Alias
- Example: `alias MyApp.Accounts.User`

**Pattern**: `^def\s+\w+`
- Public function
- Example: `def create_user(attrs) do`

**Pattern**: `^defp\s+\w+`
- Private function
- Example: `defp validate(changeset) do`

## Environment Variables

- `MIX_ENV`
- `SECRET_KEY_BASE`
- `DATABASE_URL`
- `PHX_HOST`
- `PHX_SERVER`

## Version Indicators

- Elixir 1.15+ (current)
- Elixir 1.14 (stable)
- OTP 26 (Erlang/OTP)

## Detection Notes

- Look for `.ex` files in repository
- mix.exs is the primary indicator
- Phoenix projects have specific directory structure
- Check for config/ directory
- LiveView uses .heex templates

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **mix.exs Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
