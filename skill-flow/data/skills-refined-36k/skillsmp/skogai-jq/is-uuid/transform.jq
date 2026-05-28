# Check if string at path is a valid UUID
# Usage: jq -f is-uuid/transform.jq --arg path "data" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.id")
#
# Input: any JSON object containing string at path
# Output: boolean (true if valid UUID, false if invalid or path doesn't exist/isn't string)

# UUID regex pattern: 8-4-4-4-12 hex digits (supports all versions, case-insensitive)
# Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true/false based on UUID pattern match
if $value != null and ($value | type) == "string" then
  try (
    $value | test("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
  ) catch false
else
  false
end
