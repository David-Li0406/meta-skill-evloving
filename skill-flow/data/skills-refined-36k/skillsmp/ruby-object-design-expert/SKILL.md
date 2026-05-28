---
name: Ruby Object Design Expert
description: Automatically invoked when making decisions about Ruby code structure and organization. Triggers on mentions of "class or module", "should this be a class", "struct vs class", "PORO", "data object", "design pattern", "class vs module", "when to use class", "module vs class", "stateless class", "value object", "data container", "object factory", "extend self", "singleton class". Provides guidance on choosing the right Ruby construct (class, module, Struct, Data, Hash) based on the principle that Ruby is object-oriented, not class-oriented.
allowed-tools: Read, Grep, Glob
---

# Ruby Object Design Expert

Guidance for choosing the right Ruby construct based on the principle that **Ruby is object-oriented, not class-oriented**. Break the reflex of using the `class` keyword as your default starting point.

## Core Philosophy

Ruby developers should think in terms of **objects and messages**, not classes and inheritance. The `class` keyword should be reserved for specific use cases, not used as a default container for code.

## When to Use This Skill

- Deciding between class, module, Struct, or Data
- Reviewing code that may be over-engineered with unnecessary classes
- Identifying "class smell" - classes that should be modules or simpler constructs
- Designing new features with appropriate Ruby constructs
- Refactoring pattern-heavy code to idiomatic Ruby

## Quick Decision Tree

```
Do you need multiple instances with encapsulated state?
├── YES: Does the object have both state AND behavior?
│   ├── YES → Use a Class
│   └── NO (just data) → Use Struct or Data
└── NO: Is this a collection of related functions?
    ├── YES → Use a Module with `extend self`
    └── NO: Is this a one-off transformation?
        └── YES → Use a standalone method or lambda
```

## The Object Factory Rule

**Only use `class` if you are creating an object factory** - a template specifically designed to generate multiple objects that encapsulate internal state with behaviors that operate on that state.

### Valid Use of Class

```ruby
# Good: Object factory with state and behavior
class Policy
  def initialize(holder:, coverage:, premium:)
    @holder = holder
    @coverage = coverage
    @premium = premium
  end

  def active?
    @coverage.end_date > Date.today
  end

  def renew(new_end_date)
    @coverage = @coverage.extend_to(new_end_date)
  end
end
```

### Invalid Uses of Class

See [class-vs-module.md](class-vs-module.md) for detailed scenarios.

## Decision Matrix

| Scenario | Use | Why |
|----------|-----|-----|
| Multiple instances with state + behavior | Class | True object factory |
| Stateless utility methods | Module with `extend self` | No state to encapsulate |
| Simple data container | Struct or Data | Avoids boilerplate |
| Immutable value object | Data (Ruby 3.2+) or frozen Struct | Built-in immutability |
| Ad-hoc/temporary data grouping | Hash | Simplest solution |
| Named after design pattern | Rethink design | Patterns often unnecessary in Ruby |
| Invalid after `.new` without setup | Not a class | Objects should be valid at birth |

## Red Flags: When NOT to Use a Class

### 1. Stateless Utility Buckets

If your class has no instance variables, no meaningful instance methods, and no constructor logic, it is a module pretending to be a class.

```ruby
# Bad: Class with no state
class StringUtils
  def self.titleize(string)
    string.split.map(&:capitalize).join(' ')
  end

  def self.truncate(string, length)
    string[0...length]
  end
end

# Good: Module with extend self
module StringUtils
  extend self

  def titleize(string)
    string.split.map(&:capitalize).join(' ')
  end

  def truncate(string, length)
    string[0...length]
  end
end
```

### 2. Single-Method "Service" Classes

Classes with only a `call` or `perform` method are often just functions in disguise.

```ruby
# Questionable: Is this really an object factory?
class CalculateDiscount
  def initialize(order)
    @order = order
  end

  def call
    @order.subtotal * discount_rate
  end

  private

  def discount_rate
    @order.customer.premium? ? 0.1 : 0.05
  end
end

# Alternative: Module function
module Discounts
  extend self

  def calculate(order)
    order.subtotal * discount_rate(order.customer)
  end

  private

  def discount_rate(customer)
    customer.premium? ? 0.1 : 0.05
  end
end
```

### 3. Classes Named After Design Patterns

If your class is named `Factory`, `Builder`, `Decorator`, `Adapter`, or `AbstractBase`, reconsider. Most GoF patterns were workarounds for C++ limitations and are often unnecessary or built into Ruby.

```ruby
# Bad: Pattern for pattern's sake
class UserFactory
  def self.create(type)
    case type
    when :admin then AdminUser.new
    when :guest then GuestUser.new
    end
  end
end

# Good: Ruby already handles this
User.new(role: :admin)
# or
AdminUser.new
```

### 4. Objects Invalid After Initialization

If an object requires calling setter methods before it can function, it should not exist as a class.

```ruby
# Bad: Invalid state after .new
class Report
  def initialize
    @data = nil
  end

  def set_data(data)  # Must call this before generate!
    @data = data
  end

  def generate
    raise "No data!" unless @data
    # ...
  end
end

# Good: Valid at birth
class Report
  def initialize(data)
    @data = data
  end

  def generate
    # @data is guaranteed to exist
  end
end
```

### 5. Simple Data Containers

For "Plain Old Ruby Objects" (POROs) that just hold data, avoid class boilerplate.

See [data-structures.md](data-structures.md) for Struct, Data, and Hash patterns.

## Alternative Strategies

### Namespace with Modules

Use modules to group related methods and provide namespace organization.

```ruby
module Insurance
  module PremiumCalculations
    extend self

    def calculate_base(policy)
      policy.coverage_amount * rate_for(policy.type)
    end

    def apply_discounts(base_premium, discounts)
      discounts.reduce(base_premium) { |premium, discount| premium * (1 - discount) }
    end

    private

    def rate_for(type)
      RATES.fetch(type, DEFAULT_RATE)
    end
  end
end

# Usage
Insurance::PremiumCalculations.calculate_base(policy)
```

### Prioritize Standalone Functions

Moving functionality out of classes enables **method-level polymorphism**, making code more general-purpose.

```ruby
# Instead of class-based polymorphism
def process(item)
  case item
  when Policy then PolicyProcessor.new(item).process
  when Claim then ClaimProcessor.new(item).process
  end
end

# Consider function-based approach
module Processors
  extend self

  def process_policy(policy)
    # ...
  end

  def process_claim(claim)
    # ...
  end
end
```

### Start Simple

Begin by writing code in a single file without classes or methods. Only refactor into methods or modules once the complexity becomes uncomfortable.

```ruby
# Start here
data = fetch_data
processed = data.map { |d| transform(d) }
result = aggregate(processed)

# Only extract when needed
module DataPipeline
  extend self

  def run(source)
    data = fetch_data(source)
    processed = transform_all(data)
    aggregate(processed)
  end

  # ... extracted methods
end
```

## Context Awareness

Before applying these principles, check the existing codebase:

1. **Grep for existing patterns**: `grep -r "class.*Service" app/`
2. **Check Ruby version**: Data class requires Ruby 3.2+
3. **Review team conventions**: Some teams prefer consistent service objects

| Pattern | Detection | Conflicts | Applicability |
|---------|-----------|-----------|---------------|
| Module over Class | Check for stateless classes | None - always applicable | Use Now |
| Struct/Data | Check `.ruby-version` for 3.2+ | Older Ruby versions | Use Now / Future |
| Avoid pattern-named classes | Grep for `Factory`, `Decorator` | Established conventions | Future Direction |
| Objects valid at birth | Check for required setters | Legacy code | Use Now |

## Output Format

When providing object design recommendations:

### 1. Current State Analysis
Identify what construct is being used and why it may be suboptimal

### 2. Recommended Construct
Suggest the appropriate Ruby construct with rationale

### 3. Code Example
Provide before/after code showing the improvement

### 4. Migration Path
How to safely transition from current to recommended state

### 5. Caveats
Note any team conventions or Ruby version requirements

## Related Documentation

- [class-vs-module.md](class-vs-module.md) - Detailed class vs module decision guide
- [data-structures.md](data-structures.md) - Struct, Data, and Hash patterns

## Quick Reference

| Question | Answer |
|----------|--------|
| Does it have instance state? | No state = Module |
| Does it have behavior on that state? | No behavior = Struct/Data |
| Is it named after a pattern? | Reconsider the design |
| Is it valid immediately after `.new`? | No = Not a class |
| Is it just a `call` method? | Consider a module function |

Remember: **Ruby is object-oriented, not class-oriented.** Think objects and messages, not classes and inheritance.
