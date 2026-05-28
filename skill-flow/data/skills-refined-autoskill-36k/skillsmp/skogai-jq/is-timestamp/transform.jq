# Check if string value at path is a valid ISO 8601 timestamp
# Usage: jq -f is-timestamp/transform.jq --arg path "created_at" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.created_at")
#
# Input: any JSON object containing a string at path
# Output: boolean (true if valid ISO 8601 timestamp, false otherwise)

# ISO 8601 regex pattern supporting multiple variants:
# - Date only: 2024-01-15
# - Date + time: 2024-01-15T10:30:00
# - Date + time + timezone: 2024-01-15T10:30:00Z, 2024-01-15T10:30:00+01:00
# - With milliseconds: 2024-01-15T10:30:00.123Z
# - With microseconds: 2024-01-15T10:30:00.123456Z
"^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,9})?(Z|[+-]\\d{2}:\\d{2})?)?$" as $iso8601_pattern |

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true/false based on pattern match
if $value != null and ($value | type) == "string" then
  try (
    $value | test($iso8601_pattern)
  ) catch false
else
  false
end
