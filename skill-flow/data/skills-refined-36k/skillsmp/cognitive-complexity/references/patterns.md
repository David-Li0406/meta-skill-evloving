# Cognitive Clarity Refactoring Patterns

Catalog of refactoring patterns to reduce cognitive complexity.

## Pattern 1: Deep Module Extraction

**Problem**: Shallow module with complex interface pushing complexity to callers

**Solution**: Create deep module that pulls complexity downward

### Example: User Validation

**Before** (shallow):
```elixir
# Callers must know validation rules
def create_user(attrs) do
  changeset = User.changeset(%User{}, attrs)

  # Every caller must do this
  if changeset.valid? do
    if has_required_fields?(attrs) do
      if valid_email_format?(attrs.email) do
        if password_strong_enough?(attrs.password) do
          Repo.insert(changeset)
        else
          {:error, :weak_password}
        end
      else
        {:error, :invalid_email}
      end
    else
      {:error, :missing_fields}
    end
  else
    {:error, changeset}
  end
end
```

**After** (deep):
```elixir
# Accounts context hides all validation
defmodule Accounts do
  def create_user(attrs) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end
end

defmodule User do
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :email, :password])
    |> validate_required([:name, :email, :password])
    |> validate_email_format()
    |> validate_password_strength()
    |> hash_password()
  end

  # All validation logic encapsulated
  defp validate_email_format(changeset) do
    validate_format(changeset, :email, ~r/@/, message: "invalid format")
  end

  defp validate_password_strength(changeset) do
    changeset
    |> validate_length(:password, min: 8)
    |> validate_format(:password, ~r/[A-Z]/, message: "needs uppercase")
    |> validate_format(:password, ~r/[0-9]/, message: "needs number")
  end
end
```

**Benefits**:
- Validation in one place
- Callers just call `create_user/1`
- Easy to add new validation rules

## Pattern 2: Context Object

**Problem**: Many parameters passed through multiple layers

**Solution**: Group related parameters into context struct

### Example: Request Pipeline

**Before** (pass-through hell):
```elixir
def handle_request(conn, current_user, org, feature_flags, config, locale) do
  authenticate(conn, current_user, org, feature_flags, config, locale)
end

def authenticate(conn, current_user, org, feature_flags, config, locale) do
  authorize(conn, current_user, org, feature_flags, config, locale)
end

def authorize(conn, current_user, org, feature_flags, config, locale) do
  process(conn, current_user, org, feature_flags, config, locale)
end

def process(conn, current_user, org, feature_flags, config, locale) do
  # Finally uses some of these
end
```

**After** (context object):
```elixir
defmodule RequestContext do
  @type t :: %__MODULE__{
    conn: Plug.Conn.t(),
    current_user: User.t() | nil,
    org: Org.t() | nil,
    feature_flags: map(),
    config: map(),
    locale: String.t()
  }

  defstruct [:conn, :current_user, :org, :feature_flags, :config, :locale]

  def build(conn) do
    %__MODULE__{
      conn: conn,
      current_user: conn.assigns[:current_user],
      org: conn.assigns[:current_org],
      feature_flags: get_feature_flags(conn),
      config: Application.get_env(:my_app, :request_config),
      locale: get_locale(conn)
    }
  end
end

def handle_request(%RequestContext{} = ctx) do
  authenticate(ctx)
end

def authenticate(%RequestContext{} = ctx) do
  authorize(ctx)
end

def authorize(%RequestContext{} = ctx) do
  process(ctx)
end

def process(%RequestContext{current_user: user, feature_flags: flags}) do
  # Pattern match only what you need
end
```

**Benefits**:
- One parameter instead of 6
- Easy to add new context fields
- Can pattern match specific fields needed

## Pattern 3: Eliminate Temporal Coupling

**Problem**: Functions must be called in specific order

**Solution**: Make dependencies explicit in function signatures

### Example: System Initialization

**Before** (temporal coupling):
```elixir
def start_system do
  # Must be called in this exact order!
  # (No enforcement, easy to get wrong)
  start_database()
  load_configuration()
  initialize_cache()
  connect_services()
  start_web_server()
end

# Each function depends on previous, but not obvious
def start_database do
  # ...
end

def load_configuration do
  # Assumes database started (!)
end
```

**After** (explicit dependencies):
```elixir
def start_system do
  with {:ok, db} <- start_database(),
       {:ok, config} <- load_configuration(db),
       {:ok, cache} <- initialize_cache(config),
       {:ok, services} <- connect_services(config),
       {:ok, server} <- start_web_server(cache, services) do
    {:ok, :started}
  end
end

def start_database do
  {:ok, %DB{}}
end

def load_configuration(%DB{} = db) do
  # Type shows it needs db
  {:ok, %Config{}}
end

def initialize_cache(%Config{} = config) do
  # Type shows it needs config
  {:ok, %Cache{}}
end
```

**Benefits**:
- Order explicit in code
- Can't call in wrong order (types enforce)
- Each function declares what it needs

## Pattern 4: Strategy Pattern (Eliminate Special Cases)

**Problem**: Many special case conditionals accumulating over time

**Solution**: Use polymorphism (protocols) to eliminate branches

### Example: Pricing Logic

**Before** (special cases):
```elixir
def calculate_discount(user) do
  base_discount = cond do
    user.type == :admin -> 100
    user.type == :premium -> 20
    user.type == :trial && days_remaining(user) > 7 -> 10
    user.type == :trial -> 5
    user.referral_count > 10 -> 15
    user.first_purchase? -> 10
    true -> 0
  end

  # More special cases for holidays, promotions, etc.
  final_discount = adjust_for_holidays(base_discount, user)
  final_discount = adjust_for_promotions(final_discount, user)
  final_discount
end
```

**After** (strategy pattern):
```elixir
defprotocol DiscountStrategy do
  @doc "Calculate discount percentage for user"
  def calculate(user)
end

defimpl DiscountStrategy, for: Admin do
  def calculate(_admin), do: 100
end

defimpl DiscountStrategy, for: PremiumUser do
  def calculate(_user), do: 20
end

defimpl DiscountStrategy, for: TrialUser do
  def calculate(user) do
    if TrialUser.days_remaining(user) > 7, do: 10, else: 5
  end
end

defimpl DiscountStrategy, for: FreeUser do
  def calculate(user) do
    cond do
      user.referral_count > 10 -> 15
      user.first_purchase? -> 10
      true -> 0
    end
  end
end

# Main function now simple
def calculate_discount(user) do
  base = DiscountStrategy.calculate(user)
  base
  |> adjust_for_holidays(user)
  |> adjust_for_promotions(user)
end
```

**Benefits**:
- Adding new user types: just implement protocol
- Each type's logic isolated
- No growing conditional

## Pattern 5: Pipeline for Complex Transformations

**Problem**: Nested function calls hard to read

**Solution**: Use pipe operator for left-to-right flow

### Example: Data Processing

**Before** (nested):
```elixir
def process_users(ids) do
  format_for_api(
    enrich_with_metadata(
      filter_active(
        add_preferences(
          load_users(ids)
        )
      )
    )
  )
end
```

**After** (pipeline):
```elixir
def process_users(ids) do
  ids
  |> load_users()
  |> add_preferences()
  |> filter_active()
  |> enrich_with_metadata()
  |> format_for_api()
end
```

**Benefits**:
- Read top-to-bottom
- Easy to add/remove steps
- Clear data flow

## Pattern 6: Chunk Complex Function

**Problem**: Function doing too many things at once

**Solution**: Break into smaller, named chunks

### Example: Order Processing

**Before** (high working memory load):
```elixir
def process_order(order_id) do
  order = Repo.get(Order, order_id)
  user = Repo.get(User, order.user_id)

  if user.active do
    items = Repo.all(from i in Item, where: i.order_id == ^order_id)
    total = Enum.sum(Enum.map(items, & &1.price))

    if user.balance >= total do
      new_balance = user.balance - total
      Repo.update(User.changeset(user, %{balance: new_balance}))

      Enum.each(items, fn item ->
        inventory = Repo.get(Inventory, item.product_id)
        new_count = inventory.count - item.quantity
        Repo.update(Inventory.changeset(inventory, %{count: new_count}))
      end)

      Repo.update(Order.changeset(order, %{status: :completed}))
      send_confirmation_email(user, order)

      {:ok, order}
    else
      {:error, :insufficient_funds}
    end
  else
    {:error, :user_inactive}
  end
end
```

**After** (chunked):
```elixir
def process_order(order_id) do
  with {:ok, order, user} <- load_order_and_user(order_id),
       {:ok, order} <- validate_order(order, user),
       {:ok, order} <- charge_user(order, user),
       {:ok, order} <- update_inventory(order),
       {:ok, order} <- mark_complete(order),
       :ok <- notify_user(user, order) do
    {:ok, order}
  end
end

defp load_order_and_user(order_id) do
  with {:ok, order} <- fetch_order(order_id),
       {:ok, user} <- fetch_user(order.user_id) do
    {:ok, order, user}
  end
end

defp validate_order(order, user) do
  cond do
    !user.active -> {:error, :user_inactive}
    !has_sufficient_funds?(user, order) -> {:error, :insufficient_funds}
    true -> {:ok, order}
  end
end

defp charge_user(order, user) do
  # One responsibility
end

defp update_inventory(order) do
  # One responsibility
end
```

**Benefits**:
- Each function has one job
- Easy to understand each piece
- Easy to test individually

## Pattern 7: Make Invalid States Unrepresentable

**Problem**: Data structure can be in invalid state

**Solution**: Use types/structs that prevent invalid states

### Example: Email Verification

**Before** (can be invalid):
```elixir
defmodule User do
  schema "users" do
    field :email_verified, :boolean
    field :verified_at, :naive_datetime
    field :verification_token, :string
  end
end

# Can have:
# verified=true, verified_at=nil (invalid!)
# verified=false, verified_at=<date> (invalid!)
# verified=true, token=<present> (invalid!)
```

**After** (invalid states impossible):
```elixir
defmodule User do
  schema "users" do
    field :email_status, Ecto.Enum,
      values: [:unverified, :pending_verification, :verified]
    field :verification_token, :string, virtual: true
    field :verified_at, :naive_datetime
  end

  def changeset(user, :unverified, attrs) do
    user
    |> cast(attrs, [:email])
    |> put_change(:email_status, :unverified)
    |> put_change(:verified_at, nil)
  end

  def changeset(user, :pending_verification, attrs) do
    user
    |> cast(attrs, [])
    |> put_change(:email_status, :pending_verification)
    |> put_change(:verification_token, generate_token())
  end

  def changeset(user, :verified, attrs) do
    user
    |> cast(attrs, [])
    |> put_change(:email_status, :verified)
    |> put_change(:verified_at, DateTime.utc_now())
    |> put_change(:verification_token, nil)
  end
end
```

**Benefits**:
- Type system enforces valid states
- Can't forget to set related fields
- Transitions explicit

## Pattern 8: Domain-Specific Error Handling

**Problem**: Generic error tuples don't convey domain meaning

**Solution**: Create domain-specific error types

### Example: Payment Processing

**Before** (generic):
```elixir
def charge_card(user, amount) do
  case Gateway.charge(user.card, amount) do
    {:ok, _} -> {:ok, :charged}
    {:error, reason} -> {:error, reason}  # What kind of error?
  end
end

# Caller must know gateway error codes
case charge_card(user, amount) do
  {:ok, :charged} -> # success
  {:error, "insufficient_funds"} -> # string matching fragile
  {:error, "card_expired"} -> # what other errors exist?
end
```

**After** (domain-specific):
```elixir
defmodule PaymentError do
  @type t ::
    :insufficient_funds
    | :card_expired
    | :invalid_card
    | :gateway_timeout
    | :gateway_error
end

def charge_card(user, amount) do
  case Gateway.charge(user.card, amount) do
    {:ok, result} ->
      {:ok, result}

    {:error, gateway_error} ->
      {:error, translate_gateway_error(gateway_error)}
  end
end

defp translate_gateway_error("insufficient_funds"), do: :insufficient_funds
defp translate_gateway_error("expired_card"), do: :card_expired
defp translate_gateway_error("invalid_card"), do: :invalid_card
defp translate_gateway_error(_timeout) when ..., do: :gateway_timeout
defp translate_gateway_error(_), do: :gateway_error

# Caller has clear error types
case charge_card(user, amount) do
  {:ok, _} -> # success
  {:error, :insufficient_funds} -> # known error
  {:error, :card_expired} -> # known error
  {:error, _} -> # catch-all for unknown
end
```

**Benefits**:
- Errors are domain concepts
- Type system helps with pattern matching
- Clear what errors are possible

## Pattern 9: Extract Configuration

**Problem**: Configuration scattered throughout code

**Solution**: Centralize configuration, access where needed

### Example: Rate Limiting

**Before** (scattered):
```elixir
def check_rate_limit(user, action) do
  limit = if user.premium?, do: 1000, else: 100  # Magic numbers
  # ...
end

def check_api_limit(user) do
  limit = if user.premium?, do: 10000, else: 1000  # Different numbers
  # ...
end
```

**After** (centralized):
```elixir
defmodule RateLimits do
  def get_limit(user, :api_calls) do
    if user.premium?, do: 10_000, else: 1_000
  end

  def get_limit(user, :actions) do
    if user.premium?, do: 1_000, else: 100
  end

  def get_limit(user, :file_uploads) do
    if user.premium?, do: 100, else: 10
  end
end

def check_rate_limit(user, action) do
  limit = RateLimits.get_limit(user, action)
  # ...
end
```

**Benefits**:
- One place to change limits
- Easy to see all limits
- Can add complex logic without touching callers

## Pattern 10: Flatten Nested Conditionals

**Problem**: Deep nesting hard to follow

**Solution**: Use `with` or early returns

### Example: Validation

**Before** (nested):
```elixir
def process(attrs) do
  if has_required_fields?(attrs) do
    if valid_email?(attrs.email) do
      if strong_password?(attrs.password) do
        if unique_email?(attrs.email) do
          insert_user(attrs)
        else
          {:error, :email_taken}
        end
      else
        {:error, :weak_password}
      end
    else
      {:error, :invalid_email}
    end
  else
    {:error, :missing_fields}
  end
end
```

**After** (flat with `with`):
```elixir
def process(attrs) do
  with :ok <- validate_required_fields(attrs),
       :ok <- validate_email(attrs.email),
       :ok <- validate_password(attrs.password),
       :ok <- validate_unique_email(attrs.email) do
    insert_user(attrs)
  end
end

defp validate_required_fields(attrs) do
  if has_required_fields?(attrs), do: :ok, else: {:error, :missing_fields}
end

defp validate_email(email) do
  if valid_email?(email), do: :ok, else: {:error, :invalid_email}
end
```

**Benefits**:
- Linear flow, easy to read
- Easy to add/remove validations
- Each validation isolated

## Applying Patterns

1. **Identify high cognitive load code** (use metrics)
2. **Select appropriate pattern** (match problem)
3. **Refactor incrementally** (one pattern at a time)
4. **Test thoroughly** (ensure behavior unchanged)
5. **Measure improvement** (re-run metrics)

## Pattern Selection Guide

| Problem | Pattern |
|---------|---------|
| Shallow module | Deep Module Extraction |
| Many parameters | Context Object |
| Call order dependency | Eliminate Temporal Coupling |
| Growing conditionals | Strategy Pattern |
| Nested calls | Pipeline |
| Large function | Chunk Complex Function |
| Invalid states possible | Make Invalid States Unrepresentable |
| Generic errors | Domain-Specific Error Handling |
| Magic numbers | Extract Configuration |
| Deep nesting | Flatten Conditionals |
