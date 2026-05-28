# Convert value to array (wrap non-arrays, pass through arrays)
# Usage: jq -f to-array/transform.jq --arg path "items" input.json
#
# Arguments:
#   path: dot-separated path to value to convert to array
#
# Input: object containing any value at path
# Output: object with value at path converted to array (arrays pass through, other values get wrapped)

# Split path into array of keys
($path | split(".")) as $keys |

# Get current value at path
getpath($keys) as $value |

# If value is already an array, pass through; otherwise wrap it in an array
if ($value | type) == "array" then
  .
elif $value == null then
  setpath($keys; [null])
else
  setpath($keys; [$value])
end
