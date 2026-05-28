# Universal Framework Patterns

These patterns apply across all opinionated frameworks. The syntax differs, but the concepts are universal.

## REST Resource Mapping

### The Problem with Custom Actions

Custom actions like `POST /cards/123/close` or `POST /orders/456/ship` seem convenient but create problems:
- Non-standard HTTP semantics
- Harder to cache
- Inconsistent API design
- More routes to maintain

### The Solution: Resources for Everything

Map actions to resources:

| Custom Action | RESTful Alternative | HTTP Verb |
|--------------|---------------------|-----------|
| Close a card | Create a closure | POST /cards/:id/closure |
| Reopen a card | Delete the closure | DELETE /cards/:id/closure |
| Ship an order | Create a shipment | POST /orders/:id/shipment |
| Archive a post | Create an archival | POST /posts/:id/archival |
| Ban a user | Create a ban | POST /users/:id/ban |
| Unban a user | Delete the ban | DELETE /users/:id/ban |

### Controller Structure

Each resource gets its own controller with standard CRUD actions:

```
ClosuresController
  create  - Close the card
  destroy - Reopen the card

ShipmentsController
  create - Ship the order
  show   - View shipment details

BansController
  create  - Ban the user
  destroy - Unban the user
```

## State as Data

### The Problem with Boolean Flags

Boolean columns seem simple but cause issues:
- No history of when state changed
- No record of who changed it
- Hard to query complex state combinations
- State explosion with multiple booleans

### The Solution: State Records

Instead of `card.closed: boolean`, create a `closures` table:

```
closures
  id
  card_id
  closed_by_id
  closed_at
  reason
```

Benefits:
- Full audit trail
- Query with joins: "cards with closures" = closed cards
- Additional metadata (who, when, why)
- Easy to add more states without schema changes

### Querying State

```
# Closed cards (have a closure record)
cards.joins(:closure)
Card.objects.filter(closure__isnull=False)

# Open cards (no closure record)
cards.where.missing(:closure)
Card.objects.filter(closure__isnull=True)
```

## Naming Conventions

### Domain Verbs

Use verbs that describe what happens in the domain:

```
Good:
  card.close()
  order.ship()
  user.activate()
  post.publish()
  comment.flag()

Bad:
  card.setStatus('closed')
  order.updateShippingStatus(true)
  user.setActive(true)
  post.setPublished(true)
```

### Predicates

Boolean methods should read naturally:

```
Good:
  card.closed?    # Ruby
  card.is_closed  # Python (property)
  card.isClosed() # Java/TypeScript
  order.shipped?
  user.active?

Bad:
  card.getIsClosed()
  card.checkIfClosed()
  order.isShippedStatus()
```

### Scopes and Queries

Name scopes/querysets by what they return:

```
Good:
  .chronologically      # Ordered by date
  .alphabetically       # Ordered by name
  .recent              # Last N items
  .active              # Currently active
  .pending             # Awaiting action
  .by_author(user)     # Filtered by author

Bad:
  .sortByCreatedAt()
  .filterByActive()
  .getRecentItems()
  .whereStatusActive()
```

## Frontend Patterns

### Server-First

Modern frameworks embrace server-rendered HTML with progressive enhancement:

| Framework | Server-First Solution |
|-----------|----------------------|
| Rails | Hotwire (Turbo + Stimulus) |
| Laravel | Livewire |
| Phoenix | LiveView |
| Django | HTMX or Turbo |
| Next.js | Server Components |
| Remix | Loaders + Actions |

### When to Use Client-Side JS

Only reach for heavy client-side JavaScript when you need:
- Real-time collaboration (multiple cursors, live editing)
- Complex drag-and-drop interfaces
- Offline-first functionality
- Heavy data visualization

For everything else, server-rendered HTML with progressive enhancement is simpler and more maintainable.

### Component Patterns

```
Good:
  - Small, focused components
  - Props/attributes for configuration
  - Server-rendered by default
  - JS enhancement for interactivity

Bad:
  - Giant components doing everything
  - Client-side state management for server data
  - SPAs for content sites
  - Rebuilding browser features in JS
```

## Testing Patterns

### Use Framework Tools

Every framework has built-in testing support. Use it.

| Framework | Test Framework | Fixtures/Factories |
|-----------|---------------|-------------------|
| Rails | Minitest | Fixtures |
| Django | unittest/pytest | Fixtures |
| Laravel | PHPUnit | Factories |
| Phoenix | ExUnit | Fixtures |
| Next.js | Jest/Vitest | - |
| Spring | JUnit | @DataJpaTest |

### Test Types

```
Unit Tests
  - Test models/domain logic in isolation
  - Fast, no database/network
  - Mock external dependencies

Integration Tests
  - Test controllers/views with database
  - Verify request/response cycle
  - Use real (test) database

System/E2E Tests
  - Test full user flows in browser
  - Slow, use sparingly
  - Cover critical paths only
```

### Fixture vs Factory Philosophy

**Fixtures** (static test data):
- Defined once, reused everywhere
- Fast to load
- Relationships explicit
- Great for stable domain models

**Factories** (generated test data):
- Dynamic, create what you need
- More flexible
- Can be slower
- Great for complex scenarios

Most framework creators prefer fixtures for simplicity. Factories add complexity that's often unnecessary.

## Configuration Patterns

### Environment-Based Config

```
Good:
  - Config from environment variables
  - Sensible defaults
  - Framework config files
  - 12-factor app principles

Bad:
  - Config objects with dependency injection
  - XML configuration
  - Config spread across many files
  - Runtime configuration changes
```

### Simple Accessors

```
Good:
  MyLib.api_key = ENV['API_KEY']
  MyLib.timeout = 30

Bad:
  MyLib.configure do |config|
    config.api_key = ENV['API_KEY']
    config.timeout = 30
  end
```

The simpler pattern (direct assignment) is often sufficient. Only use configuration blocks when you have many related settings.

## Authorization Patterns

### Keep It Simple

```
Good:
  # On the User model
  def can_edit?(post)
    post.author == self || admin?
  end

  # In controller
  authorize! if current_user.can_edit?(@post)

Bad:
  # Separate policy classes
  class PostPolicy
    def edit?
      user.admin? || record.author == user
    end
  end

  # Complex authorization framework
  authorize @post, :edit?
```

For most applications, simple methods on User are enough. Only introduce policy objects when authorization becomes genuinely complex.

## Job/Background Task Patterns

### Shallow Wrappers

Jobs should be thin wrappers that call model methods:

```
Good:
  class ShipOrderJob
    def perform(order_id)
      Order.find(order_id).ship!
    end
  end

Bad:
  class ShipOrderJob
    def perform(order_id)
      order = Order.find(order_id)
      order.update!(status: 'shipping')
      ShippingService.new(order).create_label
      NotificationService.new(order.user).send_shipped_email
      AnalyticsService.track('order_shipped', order_id: order.id)
    end
  end
```

The logic belongs in the model. The job just triggers it.
