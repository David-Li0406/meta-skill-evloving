# Convert value at path to string
# Usage: jq -f to-string/transform.jq --arg path "user.name" input.json
#
# Arguments:
#   path: dot-separated path to field to convert to string (e.g., "user.name")
#
# Input: any JSON object
# Output: object with value at path converted to string
#
# Conversion rules:
#   - string: pass through unchanged
#   - number: convert to string representation
#   - boolean: "true" or "false"
#   - null: "null"
#   - array/object: JSON stringified representation
#   - missing path: creates field with "null"

($path | split(".")) as $keys |
getpath($keys) as $value |

# Convert based on type
if ($value | type) == "string" then
  # Already a string, pass through
  .
elif $value == null then
  # Null becomes "null" string
  setpath($keys; "null")
elif ($value | type) == "number" then
  # Convert number to string
  setpath($keys; ($value | tostring))
elif ($value | type) == "boolean" then
  # Convert boolean to "true" or "false"
  setpath($keys; ($value | tostring))
elif ($value | type) == "array" or ($value | type) == "object" then
  # Convert array/object to JSON string
  setpath($keys; ($value | tostring))
else
  # Fallback: convert to string
  setpath($keys; ($value | tostring))
end
