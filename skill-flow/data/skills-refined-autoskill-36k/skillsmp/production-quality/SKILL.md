---
name: production-quality
description: Use when preparing for production deployment, conducting code reviews, setting up precommit workflows, adding type specifications, implementing testing strategies, addressing security concerns, or ensuring documentation quality and best practices
---

# Production Quality Skill

This skill provides comprehensive knowledge of production-quality standards, workflows, and best practices for Elixir development. It covers precommit workflows, testing strategies, type specifications, documentation requirements, and security considerations.

## Precommit Workflow

**Every commit must pass these four checks in order:**

### 1. Compilation with Warnings as Errors

```bash
mix compile --warnings-as-errors
```

**What it checks**:
- All code compiles successfully
- No compiler warnings
- No unused variables
- No ambiguous function calls

**Common failures**:
```elixir
# Unused variable
def process(user, _context) do  # ❌ _context unused
  user.name
end

# Fix: Remove or use
def process(user, _context) do  # ✅ _ prefix indicates intentionally unused
  user.name
end
```

### 2. Code Formatting with Styler

```bash
mix format
```

**What it does**:
- Formats code to consistent style
- Runs Styler plugin for automatic improvements
- Sorts aliases and imports
- Fixes pipe formatting

**Required configuration** (`.formatter.exs`):
```elixir
[
  plugins: [Styler],
  inputs: ["*.{ex,exs}", "{config,lib,test}/**/*.{ex,exs}"],
  line_length: 98
]
```

**Styler improvements**:
- Sorts module directives (alias, import, require)
- Simplifies pipes
- Removes unnecessary parentheses
- Consistent spacing

### 3. Static Analysis with Credo

```bash
mix credo --strict
```

**What it checks**:
- Code consistency
- Common mistakes
- Readability issues
- Best practices

**Priority categories**:
- **Consistency**: naming, module organization
- **Readability**: complexity, function length
- **Refactoring opportunities**: duplicate code
- **Warnings**: potential bugs
- **Design**: anti-patterns

**Common issues**:
```elixir
# Long function
def process_order(order) do  # ❌ 60 lines
  # ... many lines ...
end

# Fix: Extract smaller functions
def process_order(order) do  # ✅
  with {:ok, validated} <- validate_order(order),
       {:ok, processed} <- process_payment(validated),
       {:ok, order} <- create_order_record(processed) do
    {:ok, order}
  end
end
```

### 4. Test Suite

```bash
mix test
```

**What it checks**:
- All tests pass
- No flaky tests
- Test coverage adequate
- No pending tests in production code

**Test organization**:
```elixir
defmodule MyApp.AccountsTest do
  use MyApp.DataCase, async: true

  describe "create_user/1" do
    test "creates user with valid attributes" do
      attrs = %{name: "Alice", email: "alice@example.com"}
      assert {:ok, user} = Accounts.create_user(attrs)
      assert user.name == "Alice"
    end

    test "returns error with invalid email" do
      attrs = %{name: "Alice", email: "invalid"}
      assert {:error, changeset} = Accounts.create_user(attrs)
      assert "invalid format" in errors_on(changeset).email
    end

    test "returns error with missing required fields" do
      assert {:error, changeset} = Accounts.create_user(%{})
      assert changeset.errors[:name]
      assert changeset.errors[:email]
    end
  end
end
```

## Type Specifications

**All public functions must have typespecs.**

### Basic Typespecs

```elixir
@spec get_user(integer()) :: {:ok, User.t()} | {:error, :not_found}
def get_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end

@spec list_users(keyword()) :: [User.t()]
def list_users(opts \\\\ []) do
  Repo.all(User, opts)
end
```

### Custom Types

```elixir
@type user_id :: pos_integer()
@type email :: String.t()
@type create_attrs :: %{
  required(:name) => String.t(),
  required(:email) => email(),
  optional(:age) => pos_integer()
}
@type create_result :: {:ok, User.t()} | {:error, Ecto.Changeset.t()}

@spec create_user(create_attrs()) :: create_result()
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end
```

### Guidelines

**Do**:
- Use concrete types (`String.t()`, not `term()`)
- Document complex return types with `@type`
- Use `User.t()` for schema types
- Include all error cases in spec

**Don't**:
```elixir
# Too generic
@spec process(any()) :: any()

# Missing error cases
@spec get_user(integer()) :: User.t()  # What about not found?

# Inconsistent
@spec create_user(map) :: tuple()  # Be specific
```

## Testing Strategy

### Test-Driven Development (TDD)

**Process**:
1. **Red**: Write failing test
2. **Green**: Implement minimal code to pass
3. **Refactor**: Improve design while keeping tests passing

```elixir
# 1. Red - Write failing test
test "authenticates user with valid credentials" do
  user = insert(:user, email: "alice@example.com", password: "secret123")

  assert {:ok, authenticated_user} = Accounts.authenticate("alice@example.com", "secret123")
  assert authenticated_user.id == user.id
end

# 2. Green - Implement
def authenticate(email, password) do
  case Repo.get_by(User, email: email) do
    nil -> {:error, :unauthorized}
    user -> verify_password(user, password)
  end
end

# 3. Refactor - Improve while tests still pass
def authenticate(email, password) do
  email
  |> get_by_email()
  |> verify_password(password)
end
```

### Test Coverage Goals

**Unit Tests** (70% of tests):
- Test individual functions
- Pure logic, no side effects
- Fast execution (<1ms per test)
- Async when possible

```elixir
test "formats name correctly" do
  assert format_name("alice") == "Alice"
  assert format_name("ALICE") == "Alice"
  assert format_name("") == ""
end
```

**Integration Tests** (25% of tests):
- Test module interactions
- Database operations
- External service mocking with Mox
- Medium execution (<100ms per test)

```elixir
test "creates user and sends welcome email" do
  expect(EmailMock, :send, fn email ->
    assert email.to == "alice@example.com"
    assert email.subject == "Welcome"
    {:ok, %{id: "email-123"}}
  end)

  assert {:ok, user} = Accounts.register_user(%{
    name: "Alice",
    email: "alice@example.com"
  })

  assert user.name == "Alice"
end
```

**End-to-End Tests** (5% of tests):
- Test full workflows
- LiveView interactions
- API endpoints
- Slow execution (can be seconds)

```elixir
test "user can register and login", %{conn: conn} do
  # Visit registration page
  {:ok, lv, _html} = live(conn, ~p"/register")

  # Fill out form
  lv
  |> element("form")
  |> render_submit(%{user: %{email: "alice@example.com", password: "secret123"}})

  # Should redirect to dashboard
  assert_redirect(lv, ~p"/dashboard")
end
```

### Property-Based Testing

Use StreamData for exploring input space:

```elixir
use ExUnitProperties

property "name formatting is idempotent" do
  check all name <- string(:alphanumeric) do
    formatted_once = format_name(name)
    formatted_twice = format_name(formatted_once)
    assert formatted_once == formatted_twice
  end
end

property "list sorting never loses elements" do
  check all list <- list_of(integer()) do
    sorted = Enum.sort(list)
    assert Enum.count(list) == Enum.count(sorted)
    assert Enum.all?(list, &(&1 in sorted))
  end
end
```

### Testing Best Practices

```elixir
# ✅ Descriptive test names
test "returns error when email already exists"

# ❌ Vague test names
test "test email"

# ✅ Arrange-Act-Assert pattern
test "updates user successfully" do
  # Arrange
  user = insert(:user, name: "Alice")
  attrs = %{name: "Alice Updated"}

  # Act
  {:ok, updated} = Accounts.update_user(user, attrs)

  # Assert
  assert updated.name == "Alice Updated"
end

# ✅ One assertion per test (when possible)
test "validates email format" do
  assert {:error, changeset} = create_user(%{email: "invalid"})
  assert "invalid format" in errors_on(changeset).email
end

test "validates email presence" do
  assert {:error, changeset} = create_user(%{email: ""})
  assert "can't be blank" in errors_on(changeset).email
end
```

## Documentation Standards

### Module Documentation

```elixir
defmodule MyApp.Accounts do
  @moduledoc """
  The Accounts context manages user accounts and authentication.

  This context handles:
  - User registration and management
  - Authentication and session management
  - Password reset workflows
  - Email verification

  ## Examples

      iex> Accounts.register_user(%{email: "alice@example.com", password: "secret"})
      {:ok, %User{}}

      iex> Accounts.authenticate("alice@example.com", "secret")
      {:ok, %User{}}

  """
end
```

### Function Documentation

```elixir
@doc """
Authenticates a user by email and password.

Returns `{:ok, user}` if credentials are valid, or `{:error, :unauthorized}`
if the email doesn't exist or password doesn't match.

## Examples

    iex> authenticate("alice@example.com", "correct_password")
    {:ok, %User{email: "alice@example.com"}}

    iex> authenticate("alice@example.com", "wrong_password")
    {:error, :unauthorized}

    iex> authenticate("nonexistent@example.com", "password")
    {:error, :unauthorized}

"""
@spec authenticate(String.t(), String.t()) ::
  {:ok, User.t()} | {:error, :unauthorized}
def authenticate(email, password) do
  # Implementation
end
```

### Code Comments

**Do comment**:
- Why decisions were made
- Non-obvious business rules
- Performance considerations
- Security concerns

```elixir
# Use constant-time comparison to prevent timing attacks
defp verify_password(password, hashed) do
  Argon2.verify_pass(password, hashed)
end

# Preload associations to avoid N+1 queries
# Typical dashboard loads 50-200 products
def list_products_for_dashboard(user_id) do
  from(p in Product,
    where: p.user_id == ^user_id,
    preload: [:category, :vendor]  # Required for display
  )
  |> Repo.all()
end
```

**Don't comment**:
- What the code does (should be obvious)
- Redundant information

```elixir
# ❌ Obvious
# Get user by ID
def get_user(id), do: Repo.get(User, id)

# ❌ Redundant
# This function creates a user
def create_user(attrs) do
  # Create changeset
  changeset = User.changeset(%User{}, attrs)
  # Insert into database
  Repo.insert(changeset)
end
```

## Security Practices

### Input Validation

```elixir
# ✅ Validate all user input with Ecto.Changeset
def create_user(attrs) do
  %User{}
  |> cast(attrs, [:name, :email, :age])
  |> validate_required([:name, :email])
  |> validate_format(:email, ~r/@/)
  |> validate_number(:age, greater_than: 0)
  |> Repo.insert()
end

# ❌ Don't trust input
def create_user(attrs) do
  Repo.insert(%User{
    name: attrs["name"],  # Unvalidated!
    email: attrs["email"]
  })
end
```

### SQL Injection Prevention

```elixir
# ✅ Use Ecto's parameterized queries
def find_by_email(email) do
  from(u in User, where: u.email == ^email)
  |> Repo.one()
end

# ❌ Don't interpolate into queries
def find_by_email(email) do
  query = "SELECT * FROM users WHERE email = '#{email}'"  # SQL injection!
  Ecto.Adapters.SQL.query!(Repo, query)
end
```

### XSS Prevention

```elixir
# Phoenix.HTML escapes by default
<p><%= @user_input %></p>  # ✅ Escaped automatically

# Explicit escape
<p><%= Phoenix.HTML.html_escape(@user_input) %></p>

# Raw HTML (use with caution)
<p><%= raw(@trusted_html) %></p>  # ❌ Only if you trust the source
```

### Authentication & Authorization

```elixir
# Scope routes by authentication
scope "/", MyAppWeb do
  pipe_through [:browser, :require_authenticated_user]

  live "/dashboard", DashboardLive
  live "/settings", SettingsLive
end

# Check permissions in context
def delete_post(user, post) do
  if user.id == post.author_id or user.admin? do
    Repo.delete(post)
  else
    {:error, :unauthorized}
  end
end
```

### Secrets Management

```elixir
# ✅ Use runtime configuration
config :my_app, MyApp.Mailer,
  adapter: Swoosh.Adapters.Sendgrid,
  api_key: System.get_env("SENDGRID_API_KEY")

# ❌ Don't commit secrets
config :my_app, MyApp.Mailer,
  api_key: "SG.abc123..."  # Never commit!
```

## Performance Guidelines

### Database Optimization

```elixir
# ✅ Preload associations to avoid N+1
products = Repo.all(from p in Product, preload: [:category, :vendor])

# ❌ N+1 query problem
products = Repo.all(Product)  # 1 query
Enum.map(products, & &1.category)  # N more queries

# ✅ Use indexes for frequent queries
create index(:products, [:user_id])
create index(:products, [:category_id, :status])

# ✅ Select only needed fields
from(u in User, select: [:id, :name, :email])
```

### Caching Strategies

```elixir
# ETS for process-local cache
:ets.new(:cache, [:named_table, :public, read_concurrency: true])

# Cachex for more features
{:ok, _} = Cachex.start_link(:my_cache)
Cachex.get(:my_cache, key)
Cachex.put(:my_cache, key, value, ttl: :timer.hours(1))
```

## Complexity Analysis

Before implementing algorithms, analyze complexity with real-world data:

```elixir
@doc """
Matches products with similar users.

Complexity: O(n × m) where n = products, m = users
Real-world: 10,000 products × 1,000 active users = 10M operations
Estimated: ~100ms with in-memory processing

Considered O(n + m) hash-map approach but memory overhead (80MB)
not justified for current scale.
"""
def find_recommendations(user_id) do
  # Implementation
end
```

**When to benchmark**:
- O(n²) or higher complexity
- Core business logic with performance requirements
- Uncertain about approach tradeoffs

Use Benchee for microbenchmarks (see benchmark command).

## Additional References

For deeper dive into quality practices:
- `${CLAUDE_PLUGIN_ROOT}/skills/production-quality/references/typespecs.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/production-quality/references/error-handling.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/production-quality/references/testing.md`

## Success Metrics

Production-quality code achieves:
- ✅ Zero precommit failures
- ✅ 100% typespec coverage for public APIs
- ✅ Comprehensive test coverage (critical paths: 100%)
- ✅ Clear documentation with examples
- ✅ Security best practices applied
- ✅ Performance characteristics understood
