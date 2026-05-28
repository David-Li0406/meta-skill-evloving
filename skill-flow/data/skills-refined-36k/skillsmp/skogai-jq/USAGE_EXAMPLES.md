# Usage Examples

Real-world examples showing how to use jq-transforms in different scenarios.

## Quick Start

```bash
# Navigate to the library
cd src/jq-transforms

# Basic get operation
echo '{"user":{"name":"skogix"}}' | \
  jq -f crud-get/transform.jq --arg path "user.name"
# Output: "skogix"

# Basic set operation
echo '{}' | \
  jq -f crud-set/transform.jq --arg path "user.name" --arg value "skogix"
# Output: {"user":{"name":"skogix"}}

# Basic delete operation
echo '{"user":{"name":"skogix","email":"test@example.com"}}' | \
  jq -f crud-delete/transform.jq --arg path "user.email"
# Output: {"user":{"name":"skogix"}}
```

## Configuration Management

### Update nested configuration value

```bash
# Update database host in config file
jq -f crud-set/transform.jq \
  --arg path "database.host" \
  --arg value "prod.example.com" \
  config.json > config-updated.json
```

### Remove sensitive data

```bash
# Remove password from config
jq -f crud-delete/transform.jq \
  --arg path "database.credentials.password" \
  config.json > config-sanitized.json
```

### Get current setting

```bash
# Check current timeout value
jq -f crud-get/transform.jq \
  --arg path "api.timeout" \
  --arg default "30" \
  config.json
```

## Data Transformation Pipeline

### Chain multiple operations

```bash
# Update user data: change name, add email, remove old field
cat user.json | \
  jq -f crud-set/transform.jq --arg path "name" --arg value "new-name" | \
  jq -f crud-set/transform.jq --arg path "email" --arg value "new@example.com" | \
  jq -f crud-delete/transform.jq --arg path "old_field" \
  > user-updated.json
```

### Conditional update based on value

```bash
# Get current value and update only if it's old
current=$(jq -f crud-get/transform.jq --arg path "version" data.json)
if [[ "$current" == '"1.0"' ]]; then
  jq -f crud-set/transform.jq \
    --arg path "version" \
    --arg value "2.0" \
    data.json > data-updated.json
fi
```

## API Response Processing

### Extract specific fields from response

```bash
# Get user ID from API response
curl -s https://api.example.com/user | \
  jq -f crud-get/transform.jq --arg path "data.user.id"
```

### Transform API response

```bash
# Extract and reshape API data
curl -s https://api.example.com/users | \
  jq -f crud-get/transform.jq --arg path "data.results" | \
  # Further process the results...
```

## Batch Processing

### Update multiple files

```bash
# Update version in all package files
for file in packages/*/package.json; do
  jq -f crud-set/transform.jq \
    --arg path "version" \
    --arg value "2.0.0" \
    "$file" > "${file}.tmp" && \
  mv "${file}.tmp" "$file"
done
```

### Migrate data format

```bash
# Migrate old format to new format
for file in data/*.json; do
  cat "$file" | \
    jq -f crud-get/transform.jq --arg path "old_field" > /tmp/value.txt && \
  cat "$file" | \
    jq -f crud-set/transform.jq --arg path "new_field" --arg value "$(cat /tmp/value.txt)" | \
    jq -f crud-delete/transform.jq --arg path "old_field" \
    > "migrated/${file}"
done
```

## Testing and Validation

### Verify configuration

```bash
# Check if required fields exist
host=$(jq -f crud-get/transform.jq --arg path "database.host" config.json)
if [[ "$host" == "null" ]]; then
  echo "Error: database.host is required"
  exit 1
fi
```

### Compare configurations

```bash
# Get value from two configs and compare
val1=$(jq -f crud-get/transform.jq --arg path "setting" config1.json)
val2=$(jq -f crud-get/transform.jq --arg path "setting" config2.json)
if [[ "$val1" != "$val2" ]]; then
  echo "Configs differ: $val1 vs $val2"
fi
```

## Advanced Patterns

### Backup and modify

```bash
# Create backup before modification
cp config.json config.json.backup
jq -f crud-set/transform.jq \
  --arg path "updated_at" \
  --arg value "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  config.json.backup > config.json
```

### Atomic updates

```bash
# Update file atomically
jq -f crud-set/transform.jq \
  --arg path "value" \
  --arg value "new" \
  data.json > data.json.tmp && \
mv data.json.tmp data.json
```

### Validation after update

```bash
# Update and verify
jq -f crud-set/transform.jq \
  --arg path "count" \
  --arg value "10" \
  data.json > data-updated.json

# Verify the update
result=$(jq -f crud-get/transform.jq --arg path "count" data-updated.json)
if [[ "$result" == '"10"' ]]; then
  mv data-updated.json data.json
  echo "Update successful"
else
  echo "Update failed, keeping original"
  rm data-updated.json
fi
```

## Working with Complex Paths

### Access deeply nested values

```bash
# Get value 5 levels deep
jq -f crud-get/transform.jq \
  --arg path "data.user.profile.settings.theme" \
  data.json
```

### Create deep structure from empty object

```bash
# Create nested structure
echo '{}' | \
  jq -f crud-set/transform.jq \
    --arg path "a.b.c.d.e" \
    --arg value "deep"
# Output: {"a":{"b":{"c":{"d":{"e":"deep"}}}}}
```

## Error Handling

### Use defaults for missing values

```bash
# Get with fallback
timeout=$(jq -r -f crud-get/transform.jq \
  --arg path "api.timeout" \
  --arg default "30" \
  config.json)
echo "Using timeout: $timeout"
```

### Safe deletion

```bash
# Delete only if path exists
if jq -e -f crud-get/transform.jq --arg path "obsolete_field" data.json >/dev/null; then
  jq -f crud-delete/transform.jq --arg path "obsolete_field" data.json > data-cleaned.json
else
  echo "Field doesn't exist, no cleanup needed"
fi
```

## Integration with Other Tools

### Use with git

```bash
# Update config and commit
jq -f crud-set/transform.jq \
  --arg path "version" \
  --arg value "$(git describe --tags)" \
  package.json > package.json.tmp && \
mv package.json.tmp package.json
git add package.json
git commit -m "Update version from git tag"
```

### Use with environment variables

```bash
# Set value from environment
jq -f crud-set/transform.jq \
  --arg path "database.host" \
  --arg value "$DB_HOST" \
  config.json > config-env.json
```

### Use in CI/CD

```bash
# Update build number in CI
jq -f crud-set/transform.jq \
  --arg path "build.number" \
  --arg value "$CI_BUILD_NUMBER" \
  metadata.json > metadata-updated.json
```

## Tips and Tricks

### Pretty print output

```bash
# Use jq's pretty printing
jq -f crud-set/transform.jq \
  --arg path "key" \
  --arg value "value" \
  data.json | jq .
```

### Compact output for comparison

```bash
# Use -c for compact output
result=$(jq -c -f crud-get/transform.jq --arg path "data" input.json)
```

### Raw output without quotes

```bash
# Use -r for raw strings
jq -r -f crud-get/transform.jq \
  --arg path "message" \
  data.json
```

### Process multiple files

```bash
# Process all JSON files in directory
find . -name "*.json" -exec \
  jq -f crud-set/transform.jq \
    --arg path "processed_at" \
    --arg value "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    {} \; -print
```

## Common Pitfalls

### Path separator

```bash
# Use dots, not slashes
# ✓ Correct
--arg path "user.profile.name"

# ✗ Wrong
--arg path "user/profile/name"
```

### Quoting values

```bash
# Values are always strings via --arg
# If you need numbers/booleans, use jq's type coercion
echo '{}' | \
  jq -f crud-set/transform.jq --arg path "count" --arg value "10" | \
  jq '.count |= tonumber'
```

### Piping order matters

```bash
# Operations are applied left-to-right
cat data.json | \
  jq -f crud-set/transform.jq --arg path "a" --arg value "1" | \
  jq -f crud-set/transform.jq --arg path "b" --arg value "2"
# Both operations are applied
```

## See Also

- [README.md](README.md) - Library overview and documentation
- [patterns.md](../../todo/jq-transforms/patterns.md) - Common jq patterns
- [examples.md](../../todo/jq-transforms/examples.md) - Use case examples
