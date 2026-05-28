# Ruby

**Category**: languages
**Description**: Ruby programming language - dynamic, object-oriented language known for elegant syntax and Rails framework
**Homepage**: https://www.ruby-lang.org

## Package Detection

### RUBYGEMS
- `bundler`
- `rake`
- `rubocop`
- `rspec`

## Configuration Files

- `Gemfile`
- `Gemfile.lock`
- `.ruby-version`
- `.ruby-gemset`
- `.rvmrc`
- `Rakefile`
- `.rubocop.yml`
- `.rspec`
- `.simplecov`
- `config.ru`
- `.tool-versions`

## File Extensions

- `.rb`
- `.rake`
- `.gemspec`
- `.erb` (ERB templates)
- `.ru` (Rack config)

## Import Detection

### Ruby
**Pattern**: `^require\s+['"]`
- Require statement
- Example: `require 'json'`

**Pattern**: `^require_relative\s+['"]`
- Require relative
- Example: `require_relative './lib/utils'`

**Pattern**: `^class\s+\w+`
- Class definition
- Example: `class User < ApplicationRecord`

**Pattern**: `^module\s+\w+`
- Module definition
- Example: `module Authentication`

**Pattern**: `^def\s+\w+`
- Method definition
- Example: `def initialize(name)`

**Pattern**: `^gem\s+['"]`
- Gem dependency
- Example: `gem 'rails', '~> 7.0'`

## Environment Variables

- `RUBY_VERSION`
- `GEM_HOME`
- `GEM_PATH`
- `BUNDLE_PATH`
- `BUNDLE_BIN`
- `RAILS_ENV`
- `RACK_ENV`

## Version Indicators

- Ruby 3.3 (current)
- Ruby 3.2 (stable)
- Ruby 3.1 (maintenance)
- Ruby 2.7 (end of life)

## Detection Notes

- Look for `.rb` files in repository
- Gemfile is the primary indicator
- config.ru indicates Rack application
- Check for Rails-specific directories (app/, config/)
- .ruby-version pins Ruby version

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **Gemfile Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
