# JSON Standards (Tier 1)

## Validation
- Valid JSON (use `jq .` to verify)
- Consistent formatting (2-space indent)
- No trailing commas

## Common Issues
| Pattern | Problem | Fix |
|---------|---------|-----|
| Trailing comma | Parse error | Remove |
| Single quotes | Invalid JSON | Double quotes only |
| Comments | Invalid JSON | Remove or use JSONC |
| Unquoted keys | Invalid JSON | Quote all keys |

## JSONL (newline-delimited)
- One JSON object per line
- No trailing newline on last line
- Each line must be valid JSON

## Schema Validation
- Use JSON Schema for validation
- Reference: `"$schema": "https://..."`
- Required fields should be explicit

## Large Files
- Consider JSONL for append-only logs
- Use streaming parsers for large files
- Compress with gzip for storage
