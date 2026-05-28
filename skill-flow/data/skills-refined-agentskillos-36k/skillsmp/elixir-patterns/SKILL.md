---
name: elixir-patterns
description: Use when implementing or refactoring Elixir code, designing system architecture, working with functional programming patterns, OTP design patterns (GenServer, supervision trees), or needing idiomatic Elixir code structures and best practices
---

# Elixir Patterns Skill

This skill provides comprehensive knowledge of production-ready Elixir patterns including functional programming principles, OTP design patterns, and idiomatic Elixir code structures.

## Core Patterns

### 1. Pattern Matching

Pattern matching is Elixir's fundamental control flow mechanism.

#### Function Head Pattern Matching

```elixir
# Match on data structure shape
def process_result({:ok, value}), do: {:success, value}
def process_result({:error, reason}), do: {:failure, reason}

# Match and destructure
def greet(%User{name: name, admin: true}), do: "Hello Admin #{name}"
def greet(%User{name: name}), do: "Hello #{name}"

# Match with guards
def calculate(x) when x > 0, do: x * 2
def calculate(x) when x <= 0, do: 0
```

**When to use**:
- Multiple code paths based on input shape
- Extracting values from complex structures
- Validating input at function boundary

**Avoid**:
```elixir
# Don't extract then check
def process_result(result) do
  case result do
    {:ok, value} -> {:success, value}
    {:error, reason} -> {:failure, reason}
  end
end
```

### 2. Railway-Oriented Programming

Chain operations that can fail using `with` for explicit error handling.

```elixir
def create_user(params) do
  with {:ok, validated} <- validate_params(params),
       {:ok, user} <- insert_user(validated),
       {:ok, _token} <- generate_token(user),
       {:ok, _email} <- send_welcome_email(user) do
    {:ok, user}
  else
    {:error, changeset = %Ecto.Changeset{}} ->
      {:error, {:validation, changeset}}

    {:error, :email_failed} = error ->
      # User created but email failed - different handling
      error

    error ->
      error
  end
end
```

**Key benefits**:
- **Explicit error handling**: Each step can fail independently
- **Early returns**: First error short-circuits the chain
- **Composable**: Easy to add/remove steps
- **Readable**: Vertical flow matches execution order

**When to use**:
- Sequential operations where each depends on previous success
- Multiple potential failure points
- Need different handling for different error types

**Avoid for**:
- Simple branching logic (use `case`)
- When you need side effects regardless of success/failure
- Single operation (just use `case` or pattern matching)

### 3. Tagged Tuples

Explicit return values for success and failure cases.

```elixir
# Standard return types
@type result :: {:ok, value} | {:error, reason}

# Success with value
{:ok, user} = Accounts.get_user(id)

# Failure with reason
{:error, :not_found} = Accounts.get_user(999)

# Multiple error types
@spec create_user(map()) ::
  {:ok, User.t()}
  | {:error, :validation_failed, Ecto.Changeset.t()}
  | {:error, :email_exists}
  | {:error, :service_unavailable}

def create_user(params) do
  with {:ok, changeset} <- validate(params),
       false <- email_exists?(changeset.changes.email),
       {:ok, user} <- insert(changeset) do
    {:ok, user}
  else
    true -> {:error, :email_exists}
    {:error, changeset} -> {:error, :validation_failed, changeset}
    {:error, :db_error} -> {:error, :service_unavailable}
  end
end
```

**Guidelines**:
- First element is `:ok` or `:error` (tagged)
- Second element is the value or reason
- Use atoms for error types (`:not_found`, `:unauthorized`)
- Complex errors can include additional context

**Never**:
```elixir
# Don't return bare values or raise for control flow
def get_user(id) do
  user  # What if nil?
end

# Don't use exceptions for expected failures
def get_user(id) do
  user = Repo.get!(User, id)  # Raises if not found
  user
end
```

### 4. Immutable Data Transformations

Data is immutable. Create new versions instead of modifying.

```elixir
# Transforming data with pipe operator
user
|> Map.put(:name, "New Name")
|> Map.put(:updated_at, DateTime.utc_now())
|> Map.update!(:login_count, &(&1 + 1))

# Updating nested structures
user = %User{
  name: "Alice",
  profile: %Profile{bio: "Hello"}
}

# Update nested immutably
updated_user = put_in(user.profile.bio, "Updated bio")

# Or with update_in
updated_user = update_in(user.profile.bio, &String.upcase/1)

# Lists - transformation not mutation
list = [1, 2, 3]
new_list = [0 | list]  # Prepend (O(1))
mapped = Enum.map(list, &(&1 * 2))
```

**Key patterns**:
- **Pipe operator** (`|>`): Chain transformations
- **Enum module**: map, filter, reduce for lists
- **Map module**: put, update, delete for maps
- **Access behavior**: get_in, put_in, update_in for nested

**Performance**:
- List prepend is O(1), append is O(n)
- Map operations are O(log n)
- Avoid modifying large lists repeatedly (use Enum.reduce)

### 5. Ecto.Changeset for Validation

Changesets validate and transform data at boundaries.

```elixir
defmodule MyApp.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :name, :string
    field :email, :string
    field :age, :integer
    timestamps()
  end

  @required_fields [:name, :email]
  @optional_fields [:age]

  def changeset(user, attrs) do
    user
    |> cast(attrs, @required_fields ++ @optional_fields)
    |> validate_required(@required_fields)
    |> validate_format(:email, ~r/@/)
    |> validate_number(:age, greater_than: 0, less_than: 150)
    |> unique_constraint(:email)
  end
end

# Usage
def create_user(attrs) do
  %User{}
  |> User.changeset(attrs)
  |> Repo.insert()
end
```

**Key patterns**:
- **cast/3**: Filter and cast input data
- **validate_***: Built-in validations
- **custom validation**: Add with `validate_change/3`
- **constraints**: Database-level validation with *_constraint

**Use changesets for**:
- Form input validation
- API parameter validation
- Business rule validation
- Transforming external data

### 6. OTP: GenServer Pattern

GenServers provide stateful processes.

```elixir
defmodule MyApp.Cache do
  use GenServer

  # Client API
  def start_link(opts) do
    GenServer.start_link(__MODULE__, opts, name: __MODULE__)
  end

  def get(key) do
    GenServer.call(__MODULE__, {:get, key})
  end

  def put(key, value) do
    GenServer.cast(__MODULE__, {:put, key, value})
  end

  # Server Callbacks
  @impl true
  def init(_opts) do
    {:ok, %{}}  # Initial state
  end

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end
end
```

**Key concepts**:
- **Synchronous** (`call`): Wait for response, blocks caller
- **Asynchronous** (`cast`): Fire and forget, doesn't block
- **State**: Maintained between calls
- **Process mailbox**: Messages queued and processed sequentially

**When to use GenServer**:
- Need to maintain state
- Coordinating access to shared resource
- Background processing with state
- Rate limiting or throttling

**Avoid for**:
- Stateless operations (use plain modules)
- Simple caching (use ETS)
- Pure computation (use functions)

### 7. Supervision Trees

Supervisors monitor and restart child processes.

```elixir
defmodule MyApp.Application do
  use Application

  def start(_type, _args) do
    children = [
      # Database connection pool
      MyApp.Repo,

      # PubSub for real-time features
      {Phoenix.PubSub, name: MyApp.PubSub},

      # GenServer with specific restart
      {MyApp.Cache, []},

      # Supervisor for dynamic workers
      {DynamicSupervisor, name: MyApp.WorkerSupervisor, strategy: :one_for_one},

      # Web endpoint
      MyAppWeb.Endpoint
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

**Supervision strategies**:
- `:one_for_one`: Restart only failed child
- `:one_for_all`: Restart all children if one fails
- `:rest_for_one`: Restart failed child and those started after it

**"Let it crash" philosophy**:
- Don't defensively handle every error
- Let process crash for unexpected errors
- Supervisor restarts with clean state
- Focus on expected error cases only

### 8. Registry for Process Discovery

Registry provides process name registration.

```elixir
# Start registry
Registry.start_link(keys: :unique, name: MyApp.Registry)

# Register process
{:ok, pid} = MyWorker.start_link(user_id: 123)
Registry.register(MyApp.Registry, "user:123", pid)

# Find process
case Registry.lookup(MyApp.Registry, "user:123") do
  [{pid, _}] -> send(pid, :hello)
  [] -> {:error, :not_found}
end

# Use with via tuple in GenServer
defmodule MyWorker do
  use GenServer

  def start_link(user_id: user_id) do
    GenServer.start_link(__MODULE__, user_id, name: via_tuple(user_id))
  end

  defp via_tuple(user_id) do
    {:via, Registry, {MyApp.Registry, "user:#{user_id}"}}
  end
end
```

**Use Registry for**:
- Dynamic process pools
- User-specific processes (websocket connections)
- Pub/Sub within application
- Process discovery by key

### 9. Protocols for Polymorphism

Protocols enable polymorphic behavior.

```elixir
defprotocol Serializable do
  @doc "Serialize data to JSON-compatible format"
  def serialize(data)
end

defimpl Serializable, for: User do
  def serialize(%User{name: name, email: email}) do
    %{name: name, email: email}
  end
end

defimpl Serializable, for: Product do
  def serialize(%Product{id: id, name: name, price: price}) do
    %{id: id, name: name, price: Decimal.to_float(price)}
  end
end

# Usage - works for any type implementing Serializable
Serializable.serialize(%User{name: "Alice", email: "alice@example.com"})
Serializable.serialize(%Product{id: 1, name: "Widget", price: Decimal.new("19.99")})
```

### 10. Task for Concurrent Operations

Tasks provide simple concurrency.

```elixir
# Async/await for concurrent operations
tasks = [
  Task.async(fn -> fetch_user(user_id) end),
  Task.async(fn -> fetch_orders(user_id) end),
  Task.async(fn -> fetch_reviews(user_id) end)
]

results = Task.await_many(tasks, 5000)

# Task.Supervisor for fault tolerance
{:ok, result} = Task.Supervisor.start_child(MyApp.TaskSupervisor, fn ->
  expensive_operation()
end)
```

## Domain-Driven Design Patterns

### Contexts

Organize code by business domain, not technical layers.

```
lib/
  my_app/
    accounts/        # Accounts context
      user.ex
      user_token.ex
      user_notifier.ex
    accounts.ex      # Public API

    products/        # Products context
      product.ex
      category.ex
    products.ex      # Public API
```

**Context public API**:
```elixir
defmodule MyApp.Accounts do
  # Public API - business operations
  def register_user(attrs)
  def authenticate_user(email, password)
  def get_user!(id)
  def update_user(user, attrs)

  # Internal - don't expose
  defp hash_password(password)
  defp send_confirmation_email(user)
end
```

**Context boundaries**:
- Never cross-context database queries
- Use public APIs for cross-context calls
- Each context owns its data

## Additional References

For deeper dive into specific patterns, see:
- `${CLAUDE_PLUGIN_ROOT}/skills/elixir-patterns/references/contexts.md` - Context design patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/elixir-patterns/references/processes.md` - OTP and process patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/elixir-patterns/references/changesets.md` - Advanced changeset patterns

## When to Apply These Patterns

**Small projects (<10k LOC)**:
- Focus on tagged tuples and pattern matching
- Simple supervision trees
- Basic contexts

**Medium projects (10-50k LOC)**:
- Add GenServers for state management
- Use Registry for dynamic processes
- Implement protocols for polymorphism
- Well-defined context boundaries

**Large projects (>50k LOC)**:
- Comprehensive supervision strategies
- Complex OTP patterns (GenStateMachine, :gen_statem)
- Umbrella applications for separation
- Consider distributed systems patterns (see distributed-systems skill)

## Success Metrics

Code using these patterns should have:
- Clear error handling (no silent failures)
- Predictable behavior (no hidden state)
- Easy to test (pure functions, injectable dependencies)
- Self-documenting (pattern matching shows intent)
- Fault-tolerant (supervision trees handle failures)
