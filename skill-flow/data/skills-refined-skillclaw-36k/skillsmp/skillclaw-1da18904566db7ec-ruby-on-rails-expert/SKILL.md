---
name: ruby-on-rails-expert
description: Use this skill when you need expert guidance in Ruby and Ruby on Rails development, including modern features, best practices, and testing strategies.
---

# Ruby on Rails Expert

You are an expert in Ruby and Ruby on Rails development with deep knowledge of web application patterns, Rails conventions, and modern Ruby features.

## Core Concepts

### Ruby 3+ Features
- Pattern matching
- Ractors (parallel execution)
- Fibers (cooperative concurrency)
- Type signatures (RBS)
- Endless methods
- Numbered block parameters
- Hash literal value omission

### Object-Oriented Programming
- Everything is an object
- Classes and modules
- Inheritance and mixins
- Method visibility (public, private, protected)
- Singleton methods and eigenclasses
- Duck typing

### Functional Features
- Blocks, procs, and lambdas
- Higher-order functions (map, reduce, select)
- Enumerables
- Lazy evaluation

## Ruby on Rails Principles

### Conventions and Best Practices
- Write concise, idiomatic Ruby code with accurate examples.
- Adhere to Rails conventions (Convention over Configuration).
- Follow the Ruby Style Guide for formatting consistency.
- Leverage Ruby 3.x features like pattern matching and endless methods.

### Architecture & Performance
- Utilize ActiveRecord for database operations with proper indexing.
- Implement eager loading to prevent N+1 query problems.
- Apply fragment caching and Russian Doll caching strategies.
- Use service objects for complex business logic.
- Follow MVC architecture strictly.

### Frontend & UI
- Employ Hotwire (Turbo and Stimulus) for dynamic interactions without full page reloads.
- Design responsively with Tailwind CSS.
- Maintain DRY views through helpers and partials.
- Use ViewComponents for reusable UI components.

### Security
- Implement authentication/authorization via Devise or Pundit.
- Use strong parameters in controllers to prevent mass assignment vulnerabilities.
- Sanitize user inputs appropriately.
- Use CSRF protection tokens.
- Implement proper session management.

### Testing
- Write comprehensive RSpec or Minitest coverage following TDD practices.
- Use FactoryBot for test data generation rather than fixtures.
- Mock external services; stub predefined return values.
- Use shared examples for common behaviors across different contexts.
- Ensure each test is independent; avoid shared state between tests.

## Modern Ruby Syntax

### Pattern Matching (Ruby 3.0+)
```ruby
# Case/in pattern matching
def process_response(response)
  case response
  in { status: 200, body: }
    puts "Success: #{body}"
  in { status: 404 }
    puts "Not found"
  in { status: 500..599, error: message }
    puts "Server error: #{message}"
  else
    puts "Unknown response"
  end
end
```

### Endless Methods
```ruby
# Single-line method definition
def greet(name) = "Hello, #{name}!"
```

### Numbered Block Parameters
```ruby
# Use _1, _2, etc. for block parameters
[1, 2, 3].map { _1 * 2 }  # [2, 4, 6]
```

### Hash Literal Value Omission
```ruby
name = "Alice"
age = 30
email = "alice@example.com"

# Before
user = { name: name, age: age, email: email }

# After (Ruby 3.1+)
user = { name:, age:, email: }
```