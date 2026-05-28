# Phoenix

**Category**: web-frameworks/backend
**Description**: Productive, reliable, fast web framework built with Elixir for real-time applications

## Package Detection

### HEX
- `phoenix`
- `phoenix_html`
- `phoenix_live_view`

### Related Packages
- `phoenix_ecto`
- `phoenix_live_view`
- `phoenix_live_dashboard`
- `plug`
- `ecto`
- `postgrex`

## Import Detection

### Elixir
File extensions: .ex, .exs

**Pattern**: `use Phoenix\.`
- Phoenix module usage
- Example: `use Phoenix.Controller`

**Pattern**: `defmodule.*Web\.`
- Phoenix web module
- Example: `defmodule MyAppWeb.UserController do`

**Pattern**: `use Phoenix\.LiveView`
- Phoenix LiveView
- Example: `use Phoenix.LiveView`

**Pattern**: `plug :|pipeline :`
- Plug pipeline definitions
- Example: `pipeline :browser do`

### Common Imports
- `Phoenix.Controller`
- `Phoenix.LiveView`
- `Phoenix.HTML`
- `Plug.Conn`

## Environment Variables

*Phoenix environment variables*

- `PHX_SERVER`
- `PHX_HOST`
- `PORT`
- `SECRET_KEY_BASE`
- `DATABASE_URL`

## Configuration Files

- `mix.exs`
- `config/config.exs`
- `config/dev.exs`
- `config/prod.exs`
- `lib/*_web/router.ex`
- `lib/*_web/endpoint.ex`

## Detection Notes

- Phoenix is Elixir-based
- Built on Plug and Cowboy
- Excellent for real-time features with LiveView

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
- **API Endpoint Detection**: 75% (MEDIUM)
