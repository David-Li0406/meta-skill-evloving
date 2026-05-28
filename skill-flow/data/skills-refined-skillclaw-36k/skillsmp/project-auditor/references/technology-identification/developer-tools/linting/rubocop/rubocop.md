# RuboCop

**Category**: developer-tools/linting
**Description**: RuboCop - Ruby static code analyzer and formatter
**Homepage**: https://rubocop.org

## Package Detection

### RUBYGEMS
- `rubocop`
- `rubocop-rails`
- `rubocop-rspec`
- `rubocop-performance`
- `rubocop-minitest`
- `rubocop-rake`
- `rubocop-thread_safety`

## Configuration Files

- `.rubocop.yml`
- `.rubocop_todo.yml`
- `.rubocop-*.yml`

## Detection Notes

- Look for .rubocop.yml in repository root
- Check for rubocop in Gemfile
- .rubocop_todo.yml contains auto-generated cops to fix
- Often configured in CI/CD pipelines

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
