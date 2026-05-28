# Query objects from array based on field conditions
# Usage: jq -f crud-query/transform.jq --arg path "items" --arg field "status" --arg value "active" input.json
#
# Arguments:
#   path: dot-separated path to array field (e.g., "data.items")
#   field: field name to match on
#   value: value to match (JSON string)
#
# Input: any JSON object containing array at path
# Output: array of matching objects, or null if path doesn't exist or value is not an array

# Split path into array of keys and get array value
($path | split(".")) as $keys |
getpath($keys) as $array |

# Parse the value argument (could be JSON)
(try ($value | fromjson) catch $value) as $match_value |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  null
else
  $array | map(select(.[$field] == $match_value))
end
