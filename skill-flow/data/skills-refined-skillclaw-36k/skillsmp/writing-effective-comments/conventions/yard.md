# YARD (Ruby)

Documentation convention for Ruby codebases.

## Overview

YARD (Yet Another Ruby Documenter) is the standard documentation tool for Ruby. It uses a tag-based syntax similar to Javadoc, with Ruby-specific features for documenting dynamic behavior.

## Basic Syntax

```ruby
# Brief description of what this method does.
#
# Longer description if needed, explaining behavior,
# constraints, or usage patterns. YARD supports
# {markdown formatting}.
#
# @param name [String] the user's display name
# @param options [Hash] configuration options
# @option options [Boolean] :notify whether to send notification
# @return [User] the created user object
# @raise [ValidationError] if name is empty or invalid
#
# @example Create a user with notification
#   user = create_user('Alice', notify: true)
#
def create_user(name, options = {})
  # ...
end
```

## Common Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `@param` | Document a parameter | `@param id [String] user identifier` |
| `@option` | Document hash option | `@option opts [Boolean] :force` |
| `@return` | Document return value | `@return [Boolean] true if valid` |
| `@raise` | Document exceptions | `@raise [IOError] if file not found` |
| `@yield` | Document block parameter | `@yield [item] each element` |
| `@yieldparam` | Document yielded params | `@yieldparam item [String]` |
| `@yieldreturn` | Document block return | `@yieldreturn [Boolean]` |
| `@example` | Show usage example | `@example\n  result = method()` |
| `@deprecated` | Mark as deprecated | `@deprecated Use {#new_method}` |
| `@see` | Reference related code | `@see OtherClass#method` |
| `@note` | Important information | `@note Thread-safe` |
| `@todo` | Planned changes | `@todo Add caching` |
| `@api` | API visibility | `@api private` |

## Applying Core Principles

### Don't Just Repeat the Method Name

```ruby
# Bad: Restates the method name
# Gets the user by ID.
# @param id [Integer] the ID
# @return [User] the user
def get_user(id)

# Good: Explains the abstraction
# Retrieve a user's complete profile from the database.
#
# Includes associated records (orders, preferences) via eager loading.
# Results are cached for 5 minutes; use +reload: true+ to bypass.
#
# @param id [Integer] unique identifier from users table
# @return [User, nil] user with associations loaded, or nil if not found
def get_user(id, reload: false)
```

### Document Block Behavior

```ruby
# Process items in batches to manage memory usage.
#
# Items are loaded lazily and processed in groups of +batch_size+.
# Processing continues until all items are handled or the block
# returns +false+.
#
# @param batch_size [Integer] items per batch (default: 100)
# @yield [Array<Item>] batch of items to process
# @yieldreturn [Boolean] false to stop processing early
# @return [Integer] total number of items processed
#
# @example Process all pending orders
#   count = process_in_batches(50) do |orders|
#     orders.each(&:fulfill)
#     true  # continue processing
#   end
#
def process_in_batches(batch_size = 100)
  # ...
end
```

### Document Dynamic Behavior

```ruby
# Dynamically defines accessor methods for configuration options.
#
# For each key in +options+, creates:
# - A getter method returning the current value
# - A setter method that validates and stores new values
#
# @param options [Hash{Symbol => Object}] option names to default values
# @return [void]
#
# @example
#   config_option timeout: 30, retries: 3
#   # Creates: timeout, timeout=, retries, retries=
#
def self.config_option(options)
  # ...
end
```

## Class Documentation

```ruby
# Manages connection pooling for database access.
#
# Maintains a fixed pool of connections that are checked out
# for use and returned when done. Connections are validated
# before checkout and recycled if stale.
#
# Thread-safe: multiple threads can safely use the pool
# without external synchronization.
#
# @example Basic usage
#   pool = ConnectionPool.new(size: 5, timeout: 10)
#   pool.with_connection do |conn|
#     conn.execute('SELECT * FROM users')
#   end
#
# @see Connection Individual connection behavior
# @see ConnectionConfig Configuration options
#
class ConnectionPool
  # Create a new connection pool.
  #
  # @param size [Integer] maximum connections to maintain
  # @param timeout [Integer] seconds to wait for available connection
  # @param config [ConnectionConfig] database connection settings
  # @raise [ArgumentError] if size < 1 or timeout < 0
  #
  def initialize(size:, timeout: 30, config:)
    # ...
  end
end
```

## Module Documentation

```ruby
# Authentication and authorization helpers.
#
# Provides mixins for controllers and models to handle
# user authentication, session management, and permission
# checking.
#
# @example Include in ApplicationController
#   class ApplicationController < ActionController::Base
#     include Auth::ControllerHelpers
#   end
#
module Auth
  # Helpers for controller authentication.
  #
  # Adds +current_user+, +authenticate!+, and +authorized?+
  # methods to controllers.
  #
  module ControllerHelpers
    # ...
  end
end
```

## Documenting DSLs

```ruby
# Define a state machine for the model.
#
# States are defined as symbols. Transitions specify
# valid source and target states. Invalid transitions
# raise {InvalidTransitionError}.
#
# @example Order fulfillment workflow
#   state_machine :status do
#     state :pending, initial: true
#     state :processing
#     state :shipped
#     state :delivered
#
#     transition from: :pending, to: :processing
#     transition from: :processing, to: :shipped
#     transition from: :shipped, to: :delivered
#   end
#
# @param attribute [Symbol] model attribute to track state
# @yield Configuration block for states and transitions
# @return [void]
#
def self.state_machine(attribute, &block)
  # ...
end
```

## Documenting Metaprogramming

```ruby
# @!method find_by_email(email)
#   Find a user by their email address.
#   @param email [String] email to search for
#   @return [User, nil] matching user or nil

# @!method find_by_username(username)
#   Find a user by their username.
#   @param username [String] username to search for
#   @return [User, nil] matching user or nil

# Dynamically creates find_by_* methods for searchable attributes.
SEARCHABLE_ATTRIBUTES.each do |attr|
  define_method("find_by_#{attr}") do |value|
    where(attr => value).first
  end
end
```

## Tools and Integration

- **Generate docs**: `yard doc` or `yard server` for live preview
- **Check coverage**: `yard stats --list-undoc`
- **RubyMine/VS Code**: Built-in YARD support
- **SDoc**: Alternative generator with Rails-style output
- **Inch**: Documentation quality checker
