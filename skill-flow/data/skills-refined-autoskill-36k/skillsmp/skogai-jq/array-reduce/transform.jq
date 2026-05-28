# Reduce array to single value using operation
# Usage: jq -f array-reduce/transform.jq --arg path "items" --arg operation "sum" input.json
#
# Arguments:
#   path: dot-separated path to array field (e.g., "data.items")
#   operation: reduction operation (sum, product, concat, min, max, count)
#   field: optional field to extract from array of objects before reducing
#
# Input: any JSON object containing array at path
# Output: single reduced value, or null if path doesn't exist or value is not an array

# Split path into array of keys and get array value
($path | split(".")) as $keys |
getpath($keys) as $array |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  null
elif $array | length == 0 then
  # Handle empty arrays based on operation
  if $operation == "concat" then ""
  elif $operation == "count" then 0
  else null
  end
else
  # Extract field if specified, otherwise use array values directly
  (if ($ARGS.named.field // "") != "" then
    $array | map(.[$ARGS.named.field])
  else
    $array
  end) as $values |

  # Perform the reduction operation
  if $operation == "sum" then
    $values | add
  elif $operation == "product" then
    $values | reduce .[] as $item (1; . * $item)
  elif $operation == "concat" then
    $values | map(tostring) | join("")
  elif $operation == "min" then
    $values | min
  elif $operation == "max" then
    $values | max
  elif $operation == "count" then
    $values | length
  else
    null
  end
end
