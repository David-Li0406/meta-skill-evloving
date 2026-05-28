# Context Design Patterns

## Overview

Contexts are Elixir's approach to Domain-Driven Design (DDD), organizing code by business domain rather than technical layers.

## Basic Context Structure

```
lib/my_app/
  accounts/           # Private implementation
    user.ex          # Schema
    user_token.ex    # Schema
    queries.ex       # Query helpers (private)
  accounts.ex        # Public API

  products/
    product.ex
    category.ex
    queries.ex
  products.ex        # Public API
```

## Public API Module

```elixir
defmodule MyApp.Accounts do
  @moduledoc """
  The Accounts context handles user management and authentication.
  """

  import Ecto.Query
  alias MyApp.Repo
  alias MyApp.Accounts.{User, UserToken}

  ## User functions

  @doc """
  Returns the list of users.

  ## Examples

      iex> list_users()
      [%User{}, ...]

  """
  def list_users do
    Repo.all(User)
  end

  @doc """
  Gets a single user.

  Raises `Ecto.NoResultsError` if the User does not exist.
  """
  def get_user!(id), do: Repo.get!(User, id)

  @doc """
  Creates a user.
  """
  def create_user(attrs \\\\ %{}) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  ## Authentication functions

  @doc """
  Authenticates a user by email and password.

  Returns {:ok, user} if valid, {:error, :unauthorized} otherwise.
  """
  def authenticate_user(email, password) do
    user = Repo.get_by(User, email: email)

    cond do
      user && verify_password(password, user.hashed_password) ->
        {:ok, user}

      user ->
        # Prevent timing attacks
        Argon2.no_user_verify()
        {:error, :unauthorized}

      true ->
        Argon2.no_user_verify()
        {:error, :unauthorized}
    end
  end

  ## Private functions

  defp verify_password(password, hashed_password) do
    Argon2.verify_pass(password, hashed_password)
  end
end
```

## Context Boundaries

**Rule**: Never cross context boundaries at the database level.

```elixir
# ❌ BAD - Direct cross-context query
def list_user_orders(user_id) do
  from(o in Order,
    join: u in User, on: o.user_id == u.id,
    where: u.id == ^user_id,
    select: o
  )
  |> Repo.all()
end

# ✅ GOOD - Use context public APIs
def list_user_orders(user_id) do
  user = Accounts.get_user!(user_id)
  Orders.list_orders_for_user(user)
end
```

## Context Dependencies

When one context needs another:

```elixir
defmodule MyApp.Orders do
  alias MyApp.Accounts
  alias MyApp.Products

  def create_order(user_id, product_id, attrs) do
    with {:ok, user} <- Accounts.fetch_user(user_id),
         {:ok, product} <- Products.fetch_product(product_id),
         {:ok, order} <- do_create_order(user, product, attrs) do
      {:ok, order}
    end
  end

  defp do_create_order(user, product, attrs) do
    # Order creation logic
  end
end
```

## Shared Schemas

Sometimes data is used across contexts:

```elixir
# Option 1: Keep in one context, expose via API
defmodule MyApp.Accounts do
  def get_user_name(user_id) do
    case get_user(user_id) do
      {:ok, user} -> user.name
      error -> error
    end
  end
end

# Option 2: Create a separate shared context for truly shared data
defmodule MyApp.Common do
  # Shared schemas, types, utilities
end
```

## Context Anti-Patterns

### 1. God Context

```elixir
# ❌ Everything in one giant context
defmodule MyApp.Core do
  # Users, products, orders, reviews, payments, shipping...
  # 5000+ lines
end
```

**Fix**: Split into focused contexts.

### 2. Technical Layering

```elixir
# ❌ Organized by technical concern
lib/my_app/
  models/       # All schemas
  queries/      # All queries
  services/     # All business logic
```

**Fix**: Organize by business domain.

### 3. Anemic Contexts

```elixir
# ❌ Just CRUD, no business logic
defmodule MyApp.Users do
  def create(attrs), do: %User{} |> User.changeset(attrs) |> Repo.insert()
  def update(user, attrs), do: user |> User.changeset(attrs) |> Repo.update()
  def delete(user), do: Repo.delete(user)
end
```

**Fix**: Add business operations.

```elixir
# ✅ Business operations
defmodule MyApp.Accounts do
  def register_user(attrs)
  def verify_email(token)
  def reset_password(user, new_password)
  def authenticate(email, password)
end
```

## Testing Contexts

```elixir
defmodule MyApp.AccountsTest do
  use MyApp.DataCase, async: true

  alias MyApp.Accounts

  describe "list_users/0" do
    test "returns all users" do
      user1 = insert(:user)
      user2 = insert(:user)

      assert Accounts.list_users() == [user1, user2]
    end
  end

  describe "create_user/1" do
    test "with valid data creates a user" do
      attrs = %{name: "Alice", email: "alice@example.com"}

      assert {:ok, user} = Accounts.create_user(attrs)
      assert user.name == "Alice"
    end

    test "with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Accounts.create_user(%{})
    end
  end
end
```

## When to Create New Context

Create a new context when:
- Clear business domain boundary
- Set of related operations
- Different stakeholders/teams
- Independent lifecycle

Keep in same context when:
- Tightly coupled data
- Share many operations
- Same business rules
- Always used together
