---
name: cognitive-complexity
description: Use when analyzing cognitive load, code complexity, onboarding difficulty, readability concerns, maintainability issues, or applying Ousterhout principles for deep modules, reducing complexity, and strategic programming approaches
---

# Cognitive Complexity Skill

This skill provides comprehensive knowledge of cognitive complexity analysis based on John Ousterhout's "A Philosophy of Software Design", focusing on deep modules, reducing complexity through better abstractions, and strategic programming approaches that minimize cognitive load.

## Core Philosophy: Ousterhout's Principles

### 1. Complexity is Incremental

**Key insight**: Complexity doesn't come from single bad decisions, but from accumulation of many small decisions. Each "just this once" special case, each quick fix, each tactical hack adds a small amount of complexity. Over time, these accumulate into systems that are hard to understand and modify.

**Implications**:
- You can't completely avoid complexity
- Focus on reducing complexity growth rate
- Strategic investments pay off over time
- Small improvements compound

**In Elixir**:
```elixir
# Each special case adds complexity
def calculate_discount(user) do
  cond do
    user.type == :admin -> 100  # Special case 1
    user.type == :premium -> 20  # Special case 2
    user.trial_expired? -> 0  # Special case 3
    user.referral_count > 10 -> 15  # Special case 4
    # More special cases accumulate over time...
    true -> 10
  end
end

# Better: Use polymorphism to eliminate special cases
defprotocol DiscountPolicy do
  def calculate_discount(user)
end

defimpl DiscountPolicy, for: Admin do
  def calculate_discount(_admin), do: 100
end

defimpl DiscountPolicy, for: PremiumUser do
  def calculate_discount(_user), do: 20
end
# Adding new types doesn't increase complexity
```

### 2. Deep Modules

**Core concept**: Best modules have **simple interfaces** but **powerful implementations**. Think of module depth as:

```
Module Depth = Implementation Power / Interface Complexity
```

**Deep modules** (Good):
- Simple to use
- Hide complex implementation
- Provide powerful functionality
- Minimal knowledge required by caller

**Shallow modules** (Bad):
- Complex to use
- Expose implementation details
- Provide minimal functionality
- Caller must understand internals

**In Elixir**:
```elixir
# Shallow module - complex interface, minimal power
defmodule ShallowCache do
  def put(cache, key, value, ttl, on_expire, compression_level, serializer) do
    # Caller must know:
    # - TTL semantics
    # - Expiration callback format
    # - Compression options
    # - Serialization format
    # Just wraps a simple map operation!
  end
end

# Deep module - simple interface, powerful implementation
defmodule DeepCache do
  @doc "Put value in cache with sensible defaults"
  def put(cache, key, value) do
    # Handles internally:
    # - Automatic TTL (configured globally)
    # - Expiration cleanup
    # - Automatic compression for large values
    # - Serialization based on value type
    # - Memory management
    # - Thread safety
    # Complex implementation, but caller just calls put/3
  end

  # Advanced options available but not required
  def put(cache, key, value, opts \\\\ []), do: # ...
end
```

**Measuring depth**:
- **Lines of code**: More implementation = more power
- **Features provided**: What can caller accomplish?
- **Required knowledge**: How much must caller know?
- **Special cases**: How many edge cases handled?

**Red flags** (shallow modules):
- Many parameters required
- Caller must read implementation
- Just delegates to other functions
- Exposes internal data structures
- Many "you must also..." requirements

### 3. Information Leakage

**Key insight**: When implementation details escape through the abstraction boundary, it creates **information leakage**. Changes to implementation now affect all callers.

**Types of leakage**:

**Temporal coupling** - Must call functions in specific order:
```elixir
# Information leakage - caller must know order
def setup_system do
  start_database()  # Must be first
  load_config()     # Must be second
  start_cache()     # Must be third
end

# No leakage - order hidden
def setup_system do
  with {:ok, db} <- start_database(),
       {:ok, config} <- load_config(db),
       {:ok, _cache} <- start_cache(config) do
    {:ok, :started}
  end
end
```

**Pass-through variables** - Same variable through many layers:
```elixir
# Leakage - config passed through 5 layers unchanged
def handle_request(conn, config) do
  process_request(conn, config)
end

def process_request(conn, config) do
  validate_request(conn, config)
end

def validate_request(conn, config) do
  check_rate_limit(conn, config)
end

def check_rate_limit(conn, config) do
  # Finally uses config.rate_limit here
end

# Better - get config where needed
def check_rate_limit(conn) do
  config = Application.get_env(:my_app, :rate_limit)
  # Use config
end
```

**Exposed data structures** - Internal representation visible:
```elixir
# Leakage - returns ETS table reference
def get_cache do
  :ets.whereis(:my_cache)  # Caller must know ETS API
end

# No leakage - hide ETS behind module API
def get(key) do
  case :ets.lookup(:my_cache, key) do
    [{^key, value}] -> {:ok, value}
    [] -> {:error, :not_found}
  end
end
```

### 4. Pull Complexity Downward

**Key insight**: It's better to add complexity to an implementation to simplify the interface than to push complexity to all callers.

**Why?** Because:
- Implementation has full context
- Complexity in one place, not duplicated
- Easier to change (one location)
- Callers stay simple

**In Elixir**:
```elixir
# Pushing complexity up (bad)
def get_user(id) do
  Repo.get(User, id)  # Returns nil or user
  # Caller must:
  # - Check for nil
  # - Verify user is active
  # - Verify user is verified
  # - Preload associations
end

# Pulling complexity down (good)
def get_active_user(id) do
  case Repo.get(User, id) do
    nil ->
      {:error, :not_found}
    user ->
      cond do
        !user.active -> {:error, :inactive}
        !user.verified_at -> {:error, :not_verified}
        true ->
          user
          |> Repo.preload([:profile, :settings])
          |> wrap_ok()
      end
  end
end
```

**When to pull down**:
- Check happens at multiple call sites
- Transformation needed by all callers
- Error handling duplicated
- Associations always needed

**Trade-off**: Sometimes creates multiple functions (`get_user/1`, `get_active_user/1`, `get_verified_user/1`), but each is simple to use correctly.

### 5. Strategic vs Tactical Programming

**Tactical** (working code, accumulates complexity):
- "Just get it working"
- Copy-paste with modifications
- Special cases as encountered
- Minimal documentation
- Quick fixes
- Short-term thinking

**Strategic** (invests in future simplicity):
- "Make it right"
- Create abstractions
- Handle cases systematically
- Comprehensive documentation
- Proper solutions
- Long-term thinking

**In Elixir**:
```elixir
# Tactical - quick fix that accumulates complexity
def notify_user(user) do
  case user.type do
    :admin -> send_admin_email(user)
    :premium -> send_premium_email(user)
    :free -> send_free_email(user)
    :trial ->
      if user.trial_days_remaining > 7 do
        send_free_email(user)
      else
        send_trial_ending_email(user)
      end
    # Each new user type = more special cases here
  end
end

# Strategic - invest in abstraction
defprotocol NotificationStrategy do
  @doc "Send notification to user based on their type"
  def notify(user)
end

defimpl NotificationStrategy, for: Admin do
  def notify(user), do: send_email(user, template: :admin_welcome)
end

defimpl NotificationStrategy, for: PremiumUser do
  def notify(user), do: send_email(user, template: :premium_welcome)
end

# Adding new types: implement protocol, no special cases
```

**When to invest strategically**:
- Feature will be extended
- Similar patterns appearing
- Code will be maintained long-term
- Team is growing

**When tactical is okay**:
- Prototyping (mark as `# SPIKE`)
- One-off scripts
- Time-critical fixes (refactor later)

### 6. Define Errors Out of Existence

**Key insight**: Best error handling is preventing errors from happening through better design.

**Techniques**:

**Use types to prevent errors**:
```elixir
# Error-prone
def divide(a, b) do
  if b == 0 do
    {:error, :division_by_zero}
  else
    {:ok, a / b}
  end
end

# Define error out with type
defmodule NonZero do
  @type t :: pos_integer() | neg_integer()

  def new(0), do: {:error, :zero_not_allowed}
  def new(n), do: {:ok, n}
end

def divide(a, %NonZero{} = b) do
  # Type system prevents zero, no runtime check needed
  a / b
end
```

**Make invalid states unrepresentable**:
```elixir
# Error-prone - can be in invalid state
defmodule User do
  schema "users" do
    field :email_verified, :boolean
    field :email_verified_at, :naive_datetime
    # Can have verified=false but verified_at set!
  end
end

# Better - states mutually exclusive
defmodule User do
  schema "users" do
    field :email_status, Ecto.Enum,
      values: [
        :unverified,
        {:verified, :naive_datetime}
      ]
    # Either unverified, or verified with timestamp
    # Invalid state impossible
  end
end
```

**Use domain semantics**:
```elixir
# Error checking
def calculate_percentage(part, whole) do
  if whole == 0 do
    {:error, :division_by_zero}
  else
    {:ok, (part / whole) * 100}
  end
end

# Error defined out - 0/0 means "not applicable" in this domain
def calculate_percentage(part, 0), do: 0  # Sensible domain interpretation
def calculate_percentage(part, whole), do: (part / whole) * 100
```

### 7. Comments Should Explain "Why"

**Key insight**: Code shows **what** it does. Comments should explain **why** it does it that way.

**Good comments**:
- Design decisions and tradeoffs
- Non-obvious optimizations
- Business rules and domain knowledge
- Historical context
- Warnings about gotchas

**Bad comments**:
- Repeating code
- Obvious information
- Outdated information
- Commented-out code

**In Elixir**:
```elixir
# Bad comment - repeats code
# Get user by ID
def get_user(id) do
  Repo.get(User, id)
end

# Good comment - explains why
# Use eager loading to prevent N+1 queries.
# Dashboard displays user profile and last 10 orders,
# so preloading is faster than lazy loading (measured: 500ms → 50ms)
def get_user_for_dashboard(id) do
  User
  |> where(id: ^id)
  |> preload([:profile, orders: from(o in Order, order_by: [desc: o.inserted_at], limit: 10)])
  |> Repo.one()
end

# Good comment - historical context
# We hash passwords in the changeset (not in database trigger) because:
# 1. Allows different hash algorithms per user (migration scenario)
# 2. Enables testing with mock passwords
# 3. Works with any database (not Postgres-specific)
# See ADR-042 for full decision context
defp hash_password(changeset) do
  # ...
end
```

**Strategic commenting**:
- Write comments while coding (fresh context)
- Update comments when changing code
- Delete comments that become outdated
- Link to ADRs, tickets, or design docs for context

## Cognitive Complexity Metrics

### Beyond Cyclomatic Complexity

Cyclomatic complexity (counting branches) is insufficient. True cognitive burden includes:

### 1. Working Memory Load

**Parameters** (Miller's Law: 7±2 items):
```elixir
# High working memory load - 8 parameters
def create_order(user_id, items, payment_method, shipping_addr,
                 billing_addr, discount_code, gift_message, gift_wrap) do
  # Developer must hold 8 concepts in mind
end

# Lower load - group related concepts
def create_order(user_id, order_details) do
  # order_details bundles related fields
  # 2 concepts instead of 8
end
```

**Variable lifespan**:
```elixir
# High cognitive load - variable used 50 lines after definition
def process_batch(items) do
  user = get_current_user()  # Line 1
  # ... 50 lines of other logic ...
  notify_user(user)  # Line 51 - must remember user from line 1
end

# Lower load - shorter lifespan
def process_batch(items) do
  results = process_items(items)
  user = get_current_user()
  notify_user(user, results)
end
```

### 2. Semantic Ambiguity

**Generic names** require reading implementation:
- `process`, `handle`, `manage`, `do_something`
- `data`, `info`, `value`, `result`
- `helper`, `util`, `misc`, `common`

**Clear names** explain purpose:
- `convert_user_to_json`, `validate_email_format`
- `calculate_discount_percentage`, `send_welcome_email`

### 3. Inconsistent Abstractions

**Same concept, different names**:
```elixir
fetch_user(id)      # HTTP fetch?
get_user(id)        # Database get?
load_user(id)       # Load from where?
retrieve_user(id)   # Same as get?
```

**Better - consistent naming**:
```elixir
# Pattern: get_<noun> for database reads
get_user(id)
get_order(id)
get_product(id)
```

### 4. Hidden Control Flow

**Macros and meta-programming** can hide complexity:
```elixir
# What does this do? Must read macro definition
use_custom_magic()

# Explicit is better
import CustomBehavior
implement_callbacks()
```

## Refactoring for Cognitive Clarity

### Pattern 1: Extract Deep Module

**Before**:
```elixir
# Callers duplicate logic
def handler1(conn) do
  user = get_user(conn.assigns.user_id)
  if user && user.active && user.verified do
    # do something
  end
end

def handler2(conn) do
  user = get_user(conn.assigns.user_id)
  if user && user.active && user.verified do
    # do something else
  end
end
```

**After**:
```elixir
# Deep module hides complexity
defmodule Auth do
  def get_active_verified_user(id) do
    case get_user(id) do
      nil -> {:error, :not_found}
      user ->
        cond do
          !user.active -> {:error, :inactive}
          !user.verified -> {:error, :not_verified}
          true -> {:ok, user}
        end
    end
  end
end

def handler1(conn) do
  with {:ok, user} <- Auth.get_active_verified_user(conn.assigns.user_id) do
    # do something
  end
end
```

### Pattern 2: Context Object

**Before**:
```elixir
# Pass-through hell
def handle_request(conn, current_user, feature_flags, config, locale) do
  process_request(conn, current_user, feature_flags, config, locale)
end

def process_request(conn, current_user, feature_flags, config, locale) do
  validate_request(conn, current_user, feature_flags, config, locale)
end
```

**After**:
```elixir
defmodule RequestContext do
  defstruct [:conn, :current_user, :feature_flags, :config, :locale]
end

def handle_request(%RequestContext{} = context) do
  process_request(context)
end

def process_request(%RequestContext{} = context) do
  validate_request(context)
end
```

### Pattern 3: Eliminate Temporal Coupling

**Before**:
```elixir
# Must call in order (hidden dependency)
setup_database()
load_config()
start_cache()
```

**After**:
```elixir
# Order explicit
def initialize do
  with {:ok, db} <- setup_database(),
       {:ok, config} <- load_config(db),
       {:ok, _cache} <- start_cache(config) do
    {:ok, :initialized}
  end
end
```

### Pattern 4: Strategy Pattern (Eliminate Special Cases)

**Before**:
```elixir
# Special cases accumulating
def calculate_price(item, user) do
  base = item.price

  discount = cond do
    user.type == :admin -> base * 1.0  # Free
    user.type == :premium -> base * 0.8
    user.type == :trial && user.trial_days > 7 -> base * 0.9
    user.type == :trial -> base * 0.95
    true -> base
  end

  # More special cases...
  discount
end
```

**After**:
```elixir
# Strategy pattern - add types without changing this code
defprotocol PricingStrategy do
  def calculate_discount(user, base_price)
end

def calculate_price(item, user) do
  PricingStrategy.calculate_discount(user, item.price)
end
```

## What to Explicitly Avoid

### Clean Code Dogma

**Arbitrary function length rules**:
- "Functions should be 5 lines"
- "Functions should fit on one screen"
- **Ousterhout**: Function length is fine if it has clear abstraction

**Excessive fragmentation**:
- Creating tiny functions for every 3-line block
- **Ousterhout**: Increases shallow modules, makes code harder to follow

**Class/module extraction for single use**:
- Creating abstraction with no reuse
- **Ousterhout**: Adds complexity without benefit

**Rules over understanding**:
- Applying rules mechanically
- **Ousterhout**: Understand principles, apply contextually

### Good Rules of Thumb (Not Dogma)

✅ **Do consider**:
- Deep modules over shallow
- Pull complexity down
- Hide implementation details
- Make common case simple
- Document design decisions

❌ **Don't blindly follow**:
- Arbitrary line count limits
- Always extract if code repeats
- Never have long functions
- Always use smallest classes

## Applying to Elixir

**Elixir strengths for cognitive clarity**:
- Pattern matching shows control flow clearly
- Pipe operator makes transformations explicit
- Tagged tuples make errors visible
- Immutability eliminates state complexity

**Elixir-specific patterns**:
- Contexts as deep modules (Phoenix pattern)
- `with` for explicit error handling
- Protocols for eliminating special cases
- Behaviours for contracts

## Additional References

For deeper exploration:
- `${CLAUDE_PLUGIN_ROOT}/skills/cognitive-complexity/references/metrics.md` - Detailed cognitive metrics
- `${CLAUDE_PLUGIN_ROOT}/skills/cognitive-complexity/references/patterns.md` - Refactoring patterns catalog
- `${CLAUDE_PLUGIN_ROOT}/skills/cognitive-complexity/references/onboarding.md` - Onboarding difficulty assessment

## Success Metrics

Code with low cognitive complexity:
- New developer productive quickly (<1 week)
- Changes isolated (touching few files)
- Bugs easy to locate
- Mental model matches code structure
- Modifications rarely break unrelated features

Code with high cognitive complexity:
- New developers struggle (>3 weeks)
- Changes ripple through many files
- Bugs hard to isolate
- Surprises when reading code
- Fear of changing anything

Focus on depth over shallowness, simplicity over cleverness, strategy over tactics.
