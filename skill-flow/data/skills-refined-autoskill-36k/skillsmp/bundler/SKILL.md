---
name: bundler
description: This skill should be used when the user asks about "Bundler", "Gemfile", "Gemfile.lock", "bundle install", "bundle update", "bundle exec", "dependency management", "gem versions", "gem groups", "bundle add", "gem sources", or needs guidance on managing Ruby dependencies.
version: 1.0.0
---

# Bundler Dependency Management

Guide to managing Ruby gem dependencies with Bundler.

## Gemfile Basics

### Structure

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

### Version Constraints

```ruby
# Exact version
gem "rails", "7.1.0"

# Minimum version
gem "pg", ">= 1.0"

# Pessimistic constraint (recommended)
gem "rails", "~> 7.1"      # >= 7.1.0, < 8.0
gem "rails", "~> 7.1.0"    # >= 7.1.0, < 7.2.0
gem "rails", "~> 7.1.2.3"  # >= 7.1.2.3, < 7.1.3.0

# Combined constraints
gem "nokogiri", ">= 1.12", "< 2.0"

# Any version (not recommended)
gem "puma"
```

### Gem Groups

```ruby
# Default group (always installed)
gem "rails"

# Named groups
group :development do
  gem "better_errors"
  gem "binding_of_caller"
end

group :test do
  gem "rspec-rails"
  gem "capybara"
end

group :development, :test do
  gem "factory_bot_rails"
  gem "faker"
end

group :production do
  gem "redis"
end
```

### Install Without Groups

```bash
# Skip groups during install
bundle config set --local without development test
bundle install

# Or inline
bundle install --without development test
```

## Gem Sources

### Alternative Sources

```ruby
source "https://rubygems.org"

# Private gem server
source "https://gems.example.com" do
  gem "private_gem"
end
```

### Git Repositories

```ruby
# From GitHub (shorthand)
gem "rails", github: "rails/rails"
gem "rails", github: "rails/rails", branch: "main"
gem "rails", github: "rails/rails", tag: "v7.1.0"
gem "rails", github: "rails/rails", ref: "abc123"

# Full git URL
gem "my_gem", git: "https://github.com/user/my_gem.git"
gem "my_gem", git: "git@github.com:user/my_gem.git"

# Specific subdirectory
gem "my_gem", github: "user/monorepo", glob: "gems/my_gem/*.gemspec"
```

### Local Path

```ruby
# For development
gem "my_gem", path: "../my_gem"
gem "my_gem", path: "~/projects/my_gem"
```

## Platforms and Requirements

### Platform-Specific Gems

```ruby
# Only on specific platforms
gem "bcrypt", platforms: :ruby
gem "wdm", platforms: :mswin

# Exclude platforms
gem "sqlite3", platforms: [:ruby, :mswin]

# Common platforms:
# :ruby - C Ruby (MRI), Rubinius
# :mri - Only MRI
# :jruby - JRuby
# :mswin - Windows
# :mingw - MinGW
# :x64_mingw - 64-bit MinGW
```

### Ruby Version Requirements

```ruby
# In Gemfile
ruby "3.2.0"

# With engine
ruby "3.2.0", engine: "jruby", engine_version: "9.4.0"

# Version constraint
ruby "~> 3.2.0"
```

## Lock File

### Understanding Gemfile.lock

```
GEM
  remote: https://rubygems.org/
  specs:
    actionpack (7.1.0)
      actionview (= 7.1.0)
      activesupport (= 7.1.0)
      rack (~> 2.2)

PLATFORMS
  arm64-darwin-22
  x86_64-linux

DEPENDENCIES
  rails (~> 7.1)

RUBY VERSION
   ruby 3.2.0p0

BUNDLED WITH
   2.4.0
```

### Managing Platforms

```bash
# Add platform
bundle lock --add-platform x86_64-linux arm64-darwin

# Remove platform
bundle lock --remove-platform x86_64-linux

# Update lock file for all platforms
bundle lock --update
```

## Common Commands

### Install and Update

```bash
# Install gems from Gemfile.lock
bundle install

# Update all gems
bundle update

# Update specific gems
bundle update rails pg

# Conservative update (minimal changes)
bundle update --conservative rails

# Update only patch versions
bundle update --patch

# Update minor versions
bundle update --minor
```

### Dependency Information

```bash
# Show gem info
bundle info rails

# Show dependency tree
bundle show

# List all gems
bundle list

# Show outdated gems
bundle outdated

# Check for security issues
bundle audit
```

### Execution

```bash
# Run command with bundled gems
bundle exec rails server
bundle exec rspec

# Create binstubs
bundle binstubs rspec-core
bin/rspec  # Faster than bundle exec

# Open gem in editor
EDITOR=code bundle open rails
```

## Configuration

### Bundle Config

```bash
# Set configuration
bundle config set --local path vendor/bundle
bundle config set --local without development test

# View configuration
bundle config list

# Unset configuration
bundle config unset path
```

### Common Settings

```bash
# Install gems locally (not system-wide)
bundle config set --local path vendor/bundle

# Parallel installation
bundle config set --local jobs 4

# Disable shared gems
bundle config set --local disable_shared_gems true

# Use system gems
bundle config set --local system true
```

### Configuration File

```yaml
# .bundle/config
---
BUNDLE_PATH: "vendor/bundle"
BUNDLE_WITHOUT: "development:test"
BUNDLE_JOBS: "4"
```

## Troubleshooting

### Common Issues

```bash
# Clear cache and reinstall
rm -rf vendor/bundle .bundle Gemfile.lock
bundle install

# Reinstall all gems
bundle install --redownload

# Debug resolution
bundle install --verbose

# Check for conflicts
bundle check
```

### Version Conflicts

```ruby
# Error: Bundler could not find compatible versions

# Solutions:
# 1. Update the conflicting gem
bundle update conflicting_gem

# 2. Relax version constraints
# Change "~> 1.0.0" to "~> 1.0"

# 3. Check dependency tree
bundle viz  # Requires graphviz
```

### Native Extensions

```bash
# If native extension fails
bundle config build.nokogiri --use-system-libraries
bundle install

# Provide library paths
bundle config build.pg --with-pg-config=/usr/local/bin/pg_config
```

## Best Practices

### Version Constraints

```ruby
# Good: Pessimistic constraints allow updates
gem "rails", "~> 7.1"

# Avoid: Exact versions prevent updates
gem "rails", "7.1.0"

# Avoid: No constraint is risky
gem "rails"
```

### Group Organization

```ruby
# Keep groups focused
group :development do
  # Development tools only
end

group :test do
  # Testing tools only
end

group :development, :test do
  # Shared tools (factories, debugging)
end
```

### Lock File Management

- Always commit `Gemfile.lock`
- Update lock file deliberately, not accidentally
- Review changes to lock file in PRs
- Periodically run `bundle update` to get security patches

### CI/CD

```bash
# Fast CI install
bundle config set --local frozen true
bundle config set --local deployment true
bundle install --jobs 4 --retry 3
```

## Gemfile.lock vs Gemfile

| Gemfile | Gemfile.lock |
|---------|--------------|
| Dependencies you want | Exact versions resolved |
| Version constraints | Specific versions |
| Human-edited | Machine-generated |
| Flexible | Deterministic |
| What you need | What you have |

Always commit both files. The lock file ensures everyone uses identical gem versions.
