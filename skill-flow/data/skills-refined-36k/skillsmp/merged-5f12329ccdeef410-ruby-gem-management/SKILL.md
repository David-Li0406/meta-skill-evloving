---
name: ruby-gem-management
description: Use this skill when you need guidance on managing Ruby gem dependencies, creating, testing, and publishing Ruby gems.
---

# Ruby Gem Management

Guide to managing Ruby gem dependencies with Bundler and developing Ruby gems.

## Bundler Dependency Management

### Gemfile Basics

#### Structure

```ruby
# Gemfile
source "https://rubygems.org"

# Ruby version (optional but recommended)
ruby "3.2.0"

# Direct dependencies
gem "rails", "~> 7.1"
gem "pg", ">= 1.0"
gem "puma"
```

#### Version Constraints

```ruby
# Exact version
gem "rails", "7.1.0"

# Minimum version
gem "pg", ">= 1.0"

# Pessimistic constraint (recommended)
gem "rails", "~> 7.1"      # >= 7.1.0, < 8.0
```

#### Gem Groups

```ruby
# Default group (always installed)
gem "rails"

# Named groups
group :development do
  gem "better_errors"
end
```

### Common Commands

```bash
# Install gems from Gemfile.lock
bundle install

# Update all gems
bundle update
```

## Ruby Gem Development

### Creating a New Gem

#### Using Bundler

```bash
# Create gem scaffold
bundle gem my_gem
```

Generated structure:

```
my_gem/
├── lib/
│   ├── my_gem/
│   │   └── version.rb
│   └── my_gem.rb
├── test/ or spec/
├── Gemfile
├── Rakefile
├── my_gem.gemspec
├── README.md
├── LICENSE.txt
└── CHANGELOG.md
```

### The Gemspec

```ruby
# my_gem.gemspec
Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = "0.1.0"
  spec.authors       = ["Your Name"]
  spec.email         = ["you@example.com"]
  spec.summary       = "Short summary of your gem"
  spec.description   = "Longer description explaining what your gem does"
  spec.license       = "MIT"
  spec.required_ruby_version = ">= 3.0.0"
end
```

### Testing Your Gem

#### Test Helper

```ruby
# test/test_helper.rb
$LOAD_PATH.unshift File.expand_path("../lib", __dir__)
require "my_gem"
require "minitest/autorun"
```

### Versioning

#### Semantic Versioning

```
MAJOR.MINOR.PATCH
```

### Publishing

#### Release Process

```bash
# 1. Update version in lib/my_gem/version.rb
# 2. Commit changes
git add -A
git commit -m "Release v1.0.0"

# 3. Build and push
bundle exec rake release
```

## Best Practices

- Always commit `Gemfile.lock` to ensure everyone uses identical gem versions.
- Use semantic versioning for your gems to communicate changes effectively.

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
      - name: Run tests
        run: bundle exec rake test
```