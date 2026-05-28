# Framework Anti-Patterns

Patterns to avoid when working with opinionated frameworks. These add complexity without proportional benefit.

## The Complexity Trap

### Signs You're Over-Engineering

1. **More files than features** - If adding a simple feature requires touching 10+ files, something is wrong
2. **Can't explain it simply** - If you can't explain the architecture to a new developer in 5 minutes, it's too complex
3. **Framework within a framework** - Building abstractions on top of framework abstractions
4. **Solving problems you don't have** - "We might need this someday" code
5. **Copy-paste from enterprise tutorials** - Patterns designed for 1000-person teams don't fit 5-person teams

### The Service Object Trap

**When NOT to use service objects:**
- Single model operations
- Simple validations
- Basic CRUD
- Anything the model can do

**When service objects might be justified:**
- Orchestrating multiple models in a transaction
- Complex external API interactions
- Business processes that span multiple domains

```
Bad: UserRegistrationService that just creates a User
Good: Put User.create logic in the User model

Bad: EmailSendingService that wraps the mailer
Good: Use the mailer directly

Bad: OrderCalculationService for totaling an order
Good: Order#total method on the model
```

## Imported Pattern Problems

### Patterns That Don't Belong

| Pattern | Origin | Why It's Wrong Here |
|---------|--------|-------------------|
| Repository Pattern | Java/C# | ORMs already abstract database access |
| Dependency Injection Containers | Java/C# | Dynamic languages don't need them |
| Command/Query Separation | DDD | Overkill for most CRUD apps |
| Event Sourcing | Financial systems | You probably don't need an audit log of everything |
| Hexagonal Architecture | Enterprise Java | Framework IS your architecture |
| Microservices | Netflix scale | You're not Netflix |

### The "Enterprise" Smell

If your codebase has any of these, question why:
- `src/Domain/`, `src/Infrastructure/`, `src/Application/` folders
- Interface files for every class
- Abstract factories
- Builder patterns for simple objects
- Strategy patterns for one strategy
- More than 2 levels of inheritance

## Dependency Anti-Patterns

### Packages You Probably Don't Need

| Package Type | Framework Alternative |
|--------------|----------------------|
| Authentication gems/packages | Framework's built-in auth (150 lines of custom code) |
| Authorization frameworks | Simple `can_do_thing?` methods on User |
| Form builders | Framework's form helpers |
| API serializers | Framework's JSON rendering |
| State machines | Enum + transition methods |
| Soft delete gems | Simple `deleted_at` column |
| Pagination gems | Framework's built-in pagination |
| Search gems (simple cases) | SQL LIKE queries or full-text search |

### The Gem/Package Evaluation Checklist

Before adding a dependency, ask:
1. Can I write this in < 100 lines?
2. Is the framework going to add this soon?
3. Will this be maintained in 2 years?
4. What's the performance overhead?
5. Does it fight the framework or complement it?

## Testing Anti-Patterns

### Over-Mocking

```
Bad:
  # Mocking everything
  mock_user = Mock(User)
  mock_order = Mock(Order)
  mock_payment = Mock(Payment)
  # What are you even testing at this point?

Good:
  # Use real objects, mock only external services
  user = users(:john)
  order = user.orders.create!(...)
  # Mock only the payment gateway
```

### Wrong Test Types

```
Bad:
  # Unit testing controllers (integration test territory)
  # E2E testing every edge case (too slow)
  # Mocking the database in integration tests

Good:
  # Unit tests for complex model logic
  # Integration tests for request/response
  # E2E tests for critical user flows only
```

### Factory Overuse

```
Bad:
  # Factory with 50 traits
  create(:user, :admin, :verified, :with_subscription, :premium, ...)

  # Factory that creates half the database
  create(:order) # creates user, products, addresses, payments...

Good:
  # Simple fixtures with known state
  users(:admin)
  orders(:pending_shipment)
```

## Architecture Anti-Patterns

### Premature Abstraction

```
Bad:
  # Creating PaymentGateway interface before you have 2 gateways
  # Building a "plugin system" for one plugin
  # Abstracting database queries "in case we switch databases"

Good:
  # Use Stripe directly until you need another gateway
  # Build the feature, abstract later if needed
  # PostgreSQL isn't going anywhere
```

### Configuration Object Disease

```
Bad:
  class AppConfig
    attr_accessor :database_url
    attr_accessor :redis_url
    attr_accessor :api_key
    attr_accessor :timeout
    attr_accessor :feature_flags
    # 50 more settings...
  end

  CONFIG = AppConfig.new
  CONFIG.timeout = 30

Good:
  # Environment variables + framework config
  ENV['DATABASE_URL']
  Rails.application.config.timeout = 30
```

### Namespace Explosion

```
Bad:
  App::Services::Users::Registration::CreateUserService
  App::Repositories::Users::UserRepository
  App::ValueObjects::Users::UserEmail

Good:
  User  # Model with registration logic
  # That's it. You don't need the rest.
```

## Frontend Anti-Patterns

### SPA Everything

```
Bad:
  # React/Vue SPA for a blog
  # Client-side routing for content sites
  # Redux for server data
  # Building your own loading states

Good:
  # Server-rendered HTML
  # Turbo/HTMX/Livewire for interactivity
  # Let the browser handle navigation
  # Progressive enhancement
```

### Rebuilding the Browser

```
Bad:
  # Custom tooltip library
  # Custom modal system
  # Custom form validation
  # Custom routing

Good:
  # Native tooltips (title attribute)
  # Native dialogs (<dialog> element)
  # Native validation (HTML5 validation)
  # Native navigation (links)
```

## The Golden Rule

**Before adding complexity, ask:**

1. Does the framework already solve this?
2. Have I read the framework documentation?
3. Is a more experienced developer using this pattern successfully?
4. Will a new hire understand this in their first week?
5. What's the simplest thing that could possibly work?

If you can't answer "yes" to most of these, you're probably over-engineering.

## Recovery Patterns

### If You're Already Over-Engineered

1. **Stop adding more abstraction** - Don't abstract your way out of abstraction
2. **Identify the 20% causing 80% of pain** - Focus removal efforts there
3. **Inline aggressively** - Copy code from abstractions back to call sites
4. **Delete unused code** - If it's not called, it doesn't need to exist
5. **Trust the framework** - Let it do what it was designed to do

### Healthy Codebase Signs

- New developers productive in days, not weeks
- Features ship in hours, not days
- Most files under 200 lines
- Tests run in under a minute
- Deployment is boring
- Framework upgrades are straightforward
