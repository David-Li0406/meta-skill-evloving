# ExDoc (Elixir)

Documentation convention for Elixir codebases.

## Overview

Elixir has first-class documentation support via `@moduledoc` and `@doc` attributes. ExDoc generates HTML documentation, and IEx (the shell) displays docs inline. Documentation supports Markdown and can include executable examples (doctests).

## Basic Syntax

```elixir
defmodule Shipping do
  @moduledoc """
  Calculate shipping costs for orders.

  Supports domestic and international shipping with
  tiered pricing based on weight and destination.
  """

  @doc """
  Calculate shipping cost for an order.

  Uses tiered pricing:
  - Domestic under 5kg: standard rates
  - Larger packages: dimensional weight pricing
  - International: carrier-specific rate tables

  ## Parameters

    - `order` - The order struct containing items
    - `destination` - Address struct with country and postal code

  ## Returns

  `{:ok, cost_in_cents}` or `{:error, reason}`

  ## Examples

      iex> order = %Order{items: [%Item{weight: 2}]}
      iex> dest = %Address{country: "US", postal: "90210"}
      iex> Shipping.calculate(order, dest)
      {:ok, 599}

  """
  @spec calculate(Order.t(), Address.t()) :: {:ok, integer()} | {:error, atom()}
  def calculate(order, destination) do
    # ...
  end
end
```

## Common Sections

| Section | Purpose |
|---------|---------|
| `## Parameters` | Document function arguments |
| `## Returns` | Document return values |
| `## Options` | Document keyword list options |
| `## Examples` | Show usage (can be doctests) |
| `## Raises` | Document exceptions |

## Applying Core Principles

### Use Different Vocabulary

```elixir
# Bad: Restates the function name
@doc """
Gets a user by ID.
"""
def get_user(id)

# Good: Explains the abstraction
@doc """
Retrieve a user's complete profile from the database.

Returns the user with preloaded associations (orders, preferences).
Returns `nil` if no user exists with the given ID.

Deactivated accounts are excluded; use `get_user_admin/1` for those.

## Examples

    iex> MyApp.Users.get_user(123)
    %User{id: 123, name: "Alice", status: :active}

    iex> MyApp.Users.get_user(999)
    nil

"""
def get_user(id)
```

### Document Options

```elixir
@doc """
Fetch paginated results from the API.

## Options

  - `:page` - Page number, starting from 1 (default: 1)
  - `:per_page` - Results per page, max 100 (default: 20)
  - `:sort` - Sort field, one of `:created_at`, `:updated_at`, `:name`
  - `:order` - Sort direction, `:asc` or `:desc` (default: `:desc`)

## Examples

    iex> Api.fetch(resource, page: 2, per_page: 50)
    {:ok, %{data: [...], meta: %{total: 150, page: 2}}}

"""
def fetch(resource, opts \\ [])
```

### Document Pattern Matching

```elixir
@doc """
Process different message types from the queue.

Handles three message formats:
- `{:user_created, user_id}` - Trigger welcome email
- `{:order_placed, order_id}` - Start fulfillment workflow
- `{:payment_failed, payment_id}` - Notify customer service

Unknown messages are logged and acknowledged to prevent redelivery.

## Examples

    iex> Worker.process({:user_created, 123})
    :ok

    iex> Worker.process({:unknown, "data"})
    :ok  # logged as unhandled

"""
def process({:user_created, user_id}), do: # ...
def process({:order_placed, order_id}), do: # ...
def process({:payment_failed, payment_id}), do: # ...
def process(unknown), do: # ...
```

## Module Documentation

```elixir
defmodule MyApp.Auth do
  @moduledoc """
  User authentication and session management.

  Supports multiple authentication methods:
  - OAuth 2.0 (Google, GitHub)
  - Username/password with Argon2 hashing
  - API tokens for programmatic access

  Sessions are stored in ETS with configurable TTL.

  ## Quick Start

      {:ok, session} = Auth.authenticate(credentials)
      true = Auth.valid?(session.token)
      :ok = Auth.logout(session.token)

  ## Configuration

      config :my_app, MyApp.Auth,
        session_ttl: :timer.hours(24),
        token_length: 32

  ## See Also

  - `MyApp.Auth.Session` - Session struct and lifecycle
  - `MyApp.Auth.Token` - API token management
  """
end
```

## Documenting Behaviours

```elixir
defmodule MyApp.Store do
  @moduledoc """
  Behaviour for session storage backends.

  Implement this behaviour to create custom storage backends.
  The default implementation uses ETS; see `MyApp.Store.ETS`.

  ## Example Implementation

      defmodule MyApp.Store.Redis do
        @behaviour MyApp.Store

        @impl true
        def get(token) do
          case Redix.command(:redix, ["GET", token]) do
            {:ok, nil} -> {:ok, nil}
            {:ok, data} -> {:ok, :erlang.binary_to_term(data)}
            {:error, _} = err -> err
          end
        end

        # ... other callbacks
      end
  """

  @doc """
  Retrieve a session by its token.

  Returns `{:ok, session}` if found, `{:ok, nil}` if not found,
  or `{:error, reason}` if the storage backend fails.
  """
  @callback get(token :: String.t()) :: {:ok, Session.t() | nil} | {:error, term()}

  @doc """
  Store a session with the given TTL in milliseconds.

  If a session with this token exists, it is overwritten.
  """
  @callback put(session :: Session.t(), ttl :: pos_integer()) :: :ok | {:error, term()}
end
```

## Documenting Structs

```elixir
defmodule MyApp.User do
  @moduledoc """
  Represents an authenticated user account.

  ## Fields

    - `:id` - Unique identifier (UUID)
    - `:email` - Primary contact email (unique, verified)
    - `:name` - Display name shown in UI
    - `:status` - Account status: `:active`, `:pending`, or `:suspended`
    - `:inserted_at` - Account creation timestamp
    - `:updated_at` - Last modification timestamp

  ## Examples

      %User{
        id: "550e8400-e29b-41d4-a716-446655440000",
        email: "alice@example.com",
        name: "Alice",
        status: :active
      }

  """

  @type t :: %__MODULE__{
    id: String.t(),
    email: String.t(),
    name: String.t(),
    status: :active | :pending | :suspended,
    inserted_at: DateTime.t(),
    updated_at: DateTime.t()
  }

  defstruct [:id, :email, :name, :status, :inserted_at, :updated_at]
end
```

## Doctests

Examples in documentation can be run as tests:

```elixir
@doc """
Add two numbers.

## Examples

    iex> Math.add(1, 2)
    3

    iex> Math.add(-1, 1)
    0

"""
def add(a, b), do: a + b
```

Run with `mix test`. Doctests ensure examples stay accurate.

### Multi-line Doctests

```elixir
@doc """
## Examples

    iex> list = [1, 2, 3]
    iex> Enum.map(list, fn x -> x * 2 end)
    [2, 4, 6]

    iex> result =
    ...>   "hello"
    ...>   |> String.upcase()
    ...>   |> String.reverse()
    iex> result
    "OLLEH"

"""
```

## Hiding Documentation

```elixir
# Hide from documentation but keep the function public
@doc false
def internal_helper(x), do: x

# Document as deprecated
@doc deprecated: "Use `new_function/1` instead"
def old_function(x), do: new_function(x)
```

## Tools

- **mix docs**: Generate HTML documentation (requires ex_doc dependency)
- **IEx**: `h Module.function` shows docs in shell
- **mix test**: Runs doctests automatically
- **HexDocs**: Automatic documentation hosting for Hex packages
