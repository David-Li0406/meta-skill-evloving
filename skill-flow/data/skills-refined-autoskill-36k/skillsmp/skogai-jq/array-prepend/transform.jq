# Prepend value(s) to the start of an array at a specified path
# Usage: jq -f array-prepend/transform.jq --arg array_path "items" --arg value '{"new":"item"}' input.json
#
# Arguments:
#   array_path: dot-separated path to the array field (e.g., "items" or "data.items")
#   value: JSON string of value to prepend (will be parsed as JSON if possible)
#
# Input: object containing an array at the specified path
# Output: object with value prepended to the array

# Parse the array path into keys
($ARGS.named.array_path | split(".")) as $keys |

# Parse value as JSON if possible, otherwise use as string
(try ($ARGS.named.value | fromjson) catch $ARGS.named.value) as $parsed_value |

# Get the current array (or null if doesn't exist)
getpath($keys) as $current |

# Check if path exists and is an array
if ($current | type) == "array" then
  # Prepend value to existing array
  setpath($keys; [$parsed_value] + $current)
elif $current == null then
  # Path doesn't exist - create new array with value
  setpath($keys; [$parsed_value])
else
  # Path exists but is not an array - return original unchanged
  .
end
