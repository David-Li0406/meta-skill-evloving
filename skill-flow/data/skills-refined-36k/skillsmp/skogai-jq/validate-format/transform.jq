# Validate string format against common patterns (email, url, uuid, timestamp, etc.)
# Usage: jq -f validate-format/transform.jq --arg path "email" --arg format "email" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.email")
#   format: format type to validate - "email", "url", "uuid", "timestamp", "date"
#
# Input: any JSON object containing string at path
# Output: boolean (true if value matches format, false if invalid or path doesn't exist/isn't string)

# Define format regex patterns
{
  "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  "url": "^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$",
  "uuid": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
  "timestamp": "^\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2}(\\.\\d{1,9})?(Z|[+-]\\d{2}:\\d{2})?)?$",
  "date": "^\\d{4}-\\d{2}-\\d{2}$"
} as $patterns |

# Get format pattern
($patterns[$format] // null) as $pattern |

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true/false based on pattern match
if $pattern == null then
  # Unknown format - return false
  false
elif $value != null and ($value | type) == "string" then
  try (
    $value | test($pattern)
  ) catch false
else
  # Value is null or not a string
  false
end
