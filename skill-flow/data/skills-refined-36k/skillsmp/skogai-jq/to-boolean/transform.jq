# Convert value at path to boolean using truthy/falsy rules
# Usage: jq -f to-boolean/transform.jq --arg path "user.enabled" input.json
#
# Arguments:
#   path: dot-separated path to field to convert to boolean (e.g., "user.enabled")
#
# Input: any JSON object
# Output: object with boolean value at path
#
# Truthy/Falsy Rules:
#   Falsy: null, false, 0, "", [], {}
#   Truthy: everything else (non-zero numbers, non-empty strings, true, non-empty arrays/objects)

($path | split(".")) as $keys |
getpath($keys) as $value |

# Determine boolean based on type and value
if $value == null then
  setpath($keys; false)
elif ($value | type) == "boolean" then
  # Pass through boolean values as-is
  .
elif ($value | type) == "number" then
  # 0 is falsy, everything else is truthy
  setpath($keys; $value != 0)
elif ($value | type) == "string" then
  # Empty string is falsy, non-empty is truthy
  setpath($keys; $value != "")
elif ($value | type) == "array" then
  # Empty array is falsy, non-empty is truthy
  setpath($keys; ($value | length) > 0)
elif ($value | type) == "object" then
  # Empty object is falsy, non-empty is truthy
  setpath($keys; ($value | length) > 0)
else
  # Fallback: convert to false for unknown types
  setpath($keys; false)
end
