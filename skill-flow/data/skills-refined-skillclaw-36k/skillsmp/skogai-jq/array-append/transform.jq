# Append item(s) to the end of an array at a specified path
# Usage: jq -f array-append/transform.jq --arg array_path "items" --arg value '{"item":"data"}' input.json
#
# Arguments:
#   array_path: dot-separated path to the array field (e.g., "data.items")
#   value: JSON-encoded value to append (will be parsed if it's valid JSON)
#
# Input: object containing an array at the specified path
# Output: modified object with value(s) appended to the array

($ARGS.named.array_path | split(".")) as $keys |

# Parse value if it's JSON, otherwise use as-is
($ARGS.named.value) as $raw_value |
(try ($raw_value | fromjson) catch $raw_value) as $parsed_value |

# Get current value at path, default to empty array if doesn't exist
(getpath($keys) // []) as $current |

# Type-check: ensure current value is an array or null/missing
if ($current | type) == "array" then
  # Append value to existing array
  setpath($keys; $current + [$parsed_value])
elif $current == null or $current == [] then
  # Path doesn't exist or is empty, create new array with value
  setpath($keys; [$parsed_value])
else
  # Current value is not an array - return error by keeping original
  .
end
