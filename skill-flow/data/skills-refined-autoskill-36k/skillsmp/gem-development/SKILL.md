---
name: gem-development
description: This skill should be used when the user asks about "gem development", "create a gem", "gemspec", "publish gem", "RubyGems", "bundler", "gem structure", "gem versioning", "semantic versioning", "gem testing", "gem documentation", or needs guidance on creating and publishing Ruby gems.
version: 1.0.0
---

# Ruby Gem Development

Guide to creating, testing, and publishing Ruby gems.

## Creating a New Gem

### Using Bundler

```bash
# Create gem scaffold
bundle gem my_gem

# With options
bundle gem my_gem --test=minitest --ci=github --linter=rubocop
```

Generated structure:

```
my_gem/
├── lib/
│   ├── my_gem/
│   │   └── version.rb
│   └── my_gem.rb
├── test/ or spec/
├── bin/
│   ├── console
│   └── setup
├── Gemfile
├── Rakefile
├── my_gem.gemspec
├── README.md
├── LICENSE.txt
└── CHANGELOG.md
```

### Manual Structure

```
my_gem/
├── lib/
│   ├── my_gem/
│   │   ├── version.rb
│   │   ├── configuration.rb
│   │   └── core_class.rb
│   └── my_gem.rb          # Main entry point
├── test/
│   ├── test_helper.rb
│   └── my_gem_test.rb
├── Gemfile
├── Rakefile
├── my_gem.gemspec
├── README.md
├── LICENSE.txt
└── CHANGELOG.md
```

## The Gemspec

### Complete Example

```ruby
# my_gem.gemspec
require_relative "lib/my_gem/version"

Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = MyGem::VERSION
  spec.authors       = ["Your Name"]
  spec.email         = ["you@example.com"]

  spec.summary       = "Short summary of your gem"
  spec.description   = "Longer description explaining what your gem does"
  spec.homepage      = "https://github.com/username/my_gem"
  spec.license       = "MIT"

  spec.required_ruby_version = ">= 3.0.0"

  spec.metadata = {
    "homepage_uri"      => spec.homepage,
    "source_code_uri"   => "https://github.com/username/my_gem",
    "changelog_uri"     => "https://github.com/username/my_gem/blob/main/CHANGELOG.md",
    "bug_tracker_uri"   => "https://github.com/username/my_gem/issues",
    "documentation_uri" => "https://rubydoc.info/gems/my_gem",
    "rubygems_mfa_required" => "true"
  }

  # Files to include
  spec.files = Dir.chdir(__dir__) do
    `git ls-files -z`.split("\x0").reject do |f|
      f.match?(%r{\A(?:test|spec|features)/})
    end
  end

  spec.bindir        = "exe"
  spec.executables   = spec.files.grep(%r{\Aexe/}) { |f| File.basename(f) }
  spec.require_paths = ["lib"]

  # Runtime dependencies
  spec.add_dependency "some_gem", "~> 1.0"

  # Development dependencies (prefer Gemfile for these)
  # spec.add_development_dependency "rake", "~> 13.0"
end
```

### Version File

```ruby
# lib/my_gem/version.rb
module MyGem
  VERSION = "0.1.0"
end
```

## Main Entry Point

```ruby
# lib/my_gem.rb
require_relative "my_gem/version"
require_relative "my_gem/configuration"
require_relative "my_gem/client"

module MyGem
  class Error < StandardError; end
  class ConfigurationError < Error; end
  class APIError < Error; end

  class << self
    attr_accessor :configuration
  end

  def self.configure
    self.configuration ||= Configuration.new
    yield(configuration)
  end

  def self.reset_configuration!
    self.configuration = Configuration.new
  end
end
```

### Configuration Pattern

```ruby
# lib/my_gem/configuration.rb
module MyGem
  class Configuration
    attr_accessor :api_key, :timeout, :logger, :debug

    def initialize
      @api_key = nil
      @timeout = 30
      @logger = Logger.new($stdout)
      @debug = false
    end

    def validate!
      raise ConfigurationError, "API key required" if api_key.nil?
    end
  end
end
```

Usage:

```ruby
MyGem.configure do |config|
  config.api_key = "your-key"
  config.timeout = 60
  config.debug = true
end
```

## Testing Your Gem

### Test Helper

```ruby
# test/test_helper.rb
$LOAD_PATH.unshift File.expand_path("../lib", __dir__)
require "my_gem"
require "minitest/autorun"

# Optional: VCR for API testing
require "vcr"
VCR.configure do |config|
  config.cassette_library_dir = "test/fixtures/vcr_cassettes"
  config.hook_into :webmock
end
```

### Example Tests

```ruby
# test/my_gem_test.rb
require "test_helper"

class MyGemTest < Minitest::Test
  def setup
    MyGem.reset_configuration!
  end

  def test_version
    refute_nil MyGem::VERSION
  end

  def test_configuration
    MyGem.configure do |config|
      config.api_key = "test-key"
    end

    assert_equal "test-key", MyGem.configuration.api_key
  end

  def test_requires_api_key
    assert_raises(MyGem::ConfigurationError) do
      MyGem.configuration.validate!
    end
  end
end
```

### Rakefile

```ruby
# Rakefile
require "bundler/gem_tasks"
require "rake/testtask"

Rake::TestTask.new(:test) do |t|
  t.libs << "test"
  t.libs << "lib"
  t.test_files = FileList["test/**/*_test.rb"]
end

require "rubocop/rake_task"
RuboCop::RakeTask.new

task default: %i[test rubocop]
```

## Versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 - Initial stable release
1.0.1 - Bug fix (backwards compatible)
1.1.0 - New feature (backwards compatible)
2.0.0 - Breaking change
```

### Pre-release Versions

```ruby
VERSION = "1.0.0.alpha"
VERSION = "1.0.0.beta1"
VERSION = "1.0.0.rc1"
```

### Updating Version

```ruby
# Use a rake task
# lib/tasks/version.rake
namespace :version do
  desc "Bump patch version"
  task :patch do
    bump_version(:patch)
  end

  desc "Bump minor version"
  task :minor do
    bump_version(:minor)
  end

  desc "Bump major version"
  task :major do
    bump_version(:major)
  end

  def bump_version(type)
    version_file = "lib/my_gem/version.rb"
    content = File.read(version_file)
    current = content.match(/VERSION = "(.+)"/)[1]
    parts = current.split(".").map(&:to_i)

    case type
    when :patch then parts[2] += 1
    when :minor then parts[1] += 1; parts[2] = 0
    when :major then parts[0] += 1; parts[1] = 0; parts[2] = 0
    end

    new_version = parts.join(".")
    new_content = content.gsub(/VERSION = ".+"/, %(VERSION = "#{new_version}"))
    File.write(version_file, new_content)
    puts "Bumped to #{new_version}"
  end
end
```

## Documentation

### YARD Documentation

```ruby
# Add to Gemfile
# gem 'yard', group: :development

# Example documentation
module MyGem
  # Client for interacting with the API
  #
  # @example Basic usage
  #   client = MyGem::Client.new(api_key: "key")
  #   result = client.fetch("resource")
  #
  # @see https://api.example.com/docs API Documentation
  class Client
    # Create a new client instance
    #
    # @param api_key [String] API authentication key
    # @param timeout [Integer] Request timeout in seconds
    # @return [Client] a new client instance
    # @raise [ConfigurationError] if api_key is nil
    def initialize(api_key:, timeout: 30)
      @api_key = api_key
      @timeout = timeout
    end

    # Fetch a resource from the API
    #
    # @param resource [String] Resource path to fetch
    # @param params [Hash] Optional query parameters
    # @option params [Integer] :limit Maximum results
    # @option params [Integer] :offset Pagination offset
    # @return [Hash] Parsed JSON response
    # @raise [APIError] on API errors
    def fetch(resource, params = {})
      # implementation
    end
  end
end
```

Generate docs:

```bash
yard doc
yard server  # View at http://localhost:8808
```

### README Template

```markdown
# MyGem

Short description of what your gem does.

## Installation

Add to your Gemfile:

    gem 'my_gem'

Or install directly:

    gem install my_gem

## Usage

    require 'my_gem'

    MyGem.configure do |config|
      config.api_key = ENV['API_KEY']
    end

    client = MyGem::Client.new
    result = client.fetch('users')

## Development

    git clone https://github.com/username/my_gem
    cd my_gem
    bin/setup
    rake test

## Contributing

Bug reports and pull requests welcome on GitHub.

## License

MIT License
```

## Publishing

### First-time Setup

```bash
# Create account at rubygems.org
gem signin
```

### Release Process

```bash
# 1. Update version in lib/my_gem/version.rb
# 2. Update CHANGELOG.md
# 3. Commit changes
git add -A
git commit -m "Release v1.0.0"

# 4. Build and push
bundle exec rake release
# This will:
# - Build the gem
# - Tag the version
# - Push to RubyGems
# - Push to GitHub
```

### Manual Release

```bash
# Build
gem build my_gem.gemspec

# Push
gem push my_gem-1.0.0.gem
```

### Yanking a Bad Release

```bash
# Remove a version (use carefully!)
gem yank my_gem -v 1.0.0
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        ruby-version: ['3.0', '3.1', '3.2', '3.3']

    steps:
      - uses: actions/checkout@v4
      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: ${{ matrix.ruby-version }}
          bundler-cache: true
      - name: Run tests
        run: bundle exec rake test
      - name: Run linter
        run: bundle exec rubocop
```

### Auto-publish on Release

```yaml
# .github/workflows/publish.yml
name: Publish

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
      - name: Publish to RubyGems
        run: |
          gem build *.gemspec
          gem push *.gem
        env:
          GEM_HOST_API_KEY: ${{ secrets.RUBYGEMS_API_KEY }}
```
