---
name: gleam-package-development
description: Guides Claude through creating and publishing Gleam packages to Hex.pm. Use when developing libraries, writing documentation, or preparing packages for publication.
---

# Gleam Package Development Skill

This skill guides Claude Code through creating and publishing Gleam packages.

## Primary Sources

1. **[Writing Gleam](https://gleam.run/writing-gleam/)** - Package structure and organization
2. **[gleam.toml Documentation](https://gleam.run/writing-gleam/gleam-toml/)** - Package configuration
3. **[Hex.pm](https://hex.pm/)** - Package repository
4. **[Gleam Package Interface](https://hexdocs.pm/gleam_package_interface/)** - Package metadata
5. **[Awesome Gleam](https://github.com/gleam-lang/awesome-gleam)** - Ecosystem reference

## Creating a New Package

### Initialize Package

```bash
gleam new my_package
cd my_package
```

This creates the standard structure:
```
my_package/
├── gleam.toml
├── manifest.toml
├── src/
│   └── my_package.gleam
├── test/
│   └── my_package_test.gleam
└── README.md
```

See: [Writing Gleam - Project Structure](https://gleam.run/writing-gleam/)

### Package Configuration

Edit `gleam.toml`:

```toml
name = "my_package"
version = "1.0.0"

description = "A clear, concise description of what the package does"
licences = ["Apache-2.0"]
repository = { type = "github", user = "username", repo = "my_package" }

[dependencies]
gleam_stdlib = ">= 0.34.0 and < 2.0.0"

[dev-dependencies]
gleeunit = ">= 1.0.0 and < 2.0.0"
```

See: [gleam.toml Documentation](https://gleam.run/writing-gleam/gleam-toml/)

## Package Design

### API Design Principles

1. **Make invalid states impossible** - Use types to prevent errors
2. **Qualified imports** - Design for `package.function()` usage
3. **Clear naming** - Follow Gleam conventions
4. **Minimal exports** - Only export public API
5. **Comprehensive documentation** - Every public function

See: [Coding Standards](../../rules/coding-standards.md)

### Module Organization

For packages, organize by feature/domain:

```
src/
├── my_package.gleam           # Main API
├── my_package/
│   ├── internal.gleam         # Internal helpers
│   ├── parser.gleam           # Parser functionality
│   └── encoder.gleam          # Encoder functionality
```

See: [Conventions - Code Organization](https://github.com/gleam-lang/website/blob/patterns/documentation/conventions-patterns-anti-patterns.djot)

### Documentation

Document all public functions:

```gleam
/// Parses a JSON string into a structured value.
///
/// ## Examples
///
/// ```gleam
/// parse("{\"name\": \"Alice\"}")
/// // -> Ok(Object([#("name", String("Alice"))]))
/// ```
///
/// ## Errors
///
/// Returns `Error(ParseError)` if the input is not valid JSON.
///
pub fn parse(input: String) -> Result(Json, ParseError) {
  // Implementation
}
```

## Library vs Application

### Library Packages (MANDATORY)

- **NEVER panic or use `let assert`**
- Always return `Result` for fallible operations
- Export only public API
- Comprehensive test coverage
- Clear documentation

See: [Anti-patterns - Library Panicking](../../rules/coding-standards.md)

### Application Packages

- May panic at top level
- Can use `let assert` for unrecoverable errors
- More relaxed about internal structure

## Dependencies

### Adding Dependencies

```bash
gleam add package_name
gleam add --dev test_package
```

### Dependency Constraints

Use semantic versioning constraints:

```toml
[dependencies]
gleam_stdlib = ">= 0.34.0 and < 2.0.0"  # Caret equivalent
gleam_json = "~> 3.0"                    # Compatible with 3.x
specific_version = "= 1.2.3"             # Exact version
```

See: [gleam.toml - Dependencies](https://gleam.run/writing-gleam/gleam-toml/)

### Dependency Best Practices

- Minimize dependencies
- Use well-maintained packages
- Keep versions up to date
- Don't vendor dependencies in published packages

## Cross-Platform Packages

### Supporting Both Targets

Provide implementations for both Erlang and JavaScript:

```gleam
@external(erlang, "crypto", "strong_rand_bytes")
@external(javascript, "./crypto_ffi.mjs", "randomBytes")
pub fn random_bytes(n: Int) -> BitArray
```

Or use Gleam fallback:

```gleam
@external(erlang, "optimized_module", "fast_function")
pub fn my_function(input: String) -> Result(Output, Error) {
  // Gleam implementation (runs on JavaScript)
  slow_but_correct_implementation(input)
}
```

See: [External Functions](../../rules/external-functions.md)

### Target-Specific Code

Use `@target` attribute when necessary:

```gleam
@target(erlang)
pub fn erlang_only_function() -> Result(Value, Error) {
  // Erlang-specific implementation
}

@target(javascript)
pub fn javascript_only_function() -> Result(Value, Error) {
  // JavaScript-specific implementation
}
```

## Testing

### Test Coverage

- Test all public functions
- Test edge cases
- Test error conditions
- Test both targets if cross-platform

```bash
gleam test                      # Default target
gleam test --target erlang     # Erlang target
gleam test --target javascript # JavaScript target
```

See: [Testing Skill](../skills/gleam-testing/SKILL.md)

### Example-Based Tests

Include examples in documentation and test them:

```gleam
/// ## Examples
///
/// ```gleam
/// add(2, 3)
/// // -> 5
/// ```
pub fn add(a: Int, b: Int) -> Int {
  a + b
}

pub fn add_test() {
  let assert 5 = add(2, 3)
}
```

## Publishing to Hex.pm

### Prerequisites

1. Create account on [hex.pm](https://hex.pm/)
2. Authenticate: `gleam hex auth`

### Pre-publish Checklist

- [ ] All tests passing
- [ ] Documentation complete
- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in gleam.toml
- [ ] License file included
- [ ] .gitignore configured

### Publishing

```bash
gleam hex publish
```

See: [Publishing Packages](https://gleam.run/writing-gleam/)

### Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Package Maintenance

### Updating Dependencies

Check for outdated dependencies:
```bash
gleam deps outdated
```

Update dependencies:
```bash
gleam deps update
```

See: [Gleam v1.10 Features](https://gleam.run/news/the-happy-holidays-2025-release/)

### Deprecation

When deprecating functions, document clearly:

```gleam
/// **Deprecated**: Use `new_function` instead.
///
/// This function will be removed in version 2.0.0.
@deprecated("Use new_function instead")
pub fn old_function() -> Result(Value, Error) {
  new_function()
}
```

### Breaking Changes

When making breaking changes:
1. Bump MAJOR version
2. Document changes in CHANGELOG
3. Provide migration guide
4. Consider deprecation period first

## Package Quality

### README Template

```markdown
# Package Name

Brief description of what the package does.

## Installation

\`\`\`sh
gleam add package_name
\`\`\`

## Usage

\`\`\`gleam
import package_name

pub fn main() {
  package_name.do_something()
}
\`\`\`

## Documentation

[View on HexDocs](https://hexdocs.pm/package_name/)

## Development

\`\`\`sh
gleam test
\`\`\`

## License

[License Name]
```

### CI/CD for Packages

Example GitHub Actions:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: erlef/setup-beam@v1
        with:
          otp-version: "27.0"
          gleam-version: "1.10.0"
      - run: gleam deps download
      - run: gleam test --target erlang
      - run: gleam test --target javascript
      - run: gleam format --check src test
```

## Ecosystem Integration

### Listing on Awesome Gleam

Submit PR to [Awesome Gleam](https://github.com/gleam-lang/awesome-gleam) to increase visibility.

### Package Categories

Common package categories:
- Web frameworks
- Database clients
- Data formats (JSON, XML, CSV, TOML)
- Cryptography
- Testing utilities
- CLI tools
- Utilities

See: [Awesome Gleam](https://github.com/gleam-lang/awesome-gleam)

## Common Package Patterns

### Builder Pattern

```gleam
pub type Config {
  Config(host: String, port: Int, timeout: Int)
}

pub fn new() -> Config {
  Config(host: "localhost", port: 8080, timeout: 5000)
}

pub fn host(config: Config, host: String) -> Config {
  Config(..config, host: host)
}

pub fn port(config: Config, port: Int) -> Config {
  Config(..config, port: port)
}
```

See: [Patterns - Builder](https://github.com/gleam-lang/website/blob/patterns/documentation/conventions-patterns-anti-patterns.djot)

### Result Helpers

```gleam
pub fn try_map(
  result: Result(a, e),
  f: fn(a) -> Result(b, e)
) -> Result(b, e) {
  case result {
    Ok(value) -> f(value)
    Error(error) -> Error(error)
  }
}
```

---

**Remember**: A well-designed package is easy to use correctly and hard to use incorrectly. Focus on clear APIs and excellent documentation.
