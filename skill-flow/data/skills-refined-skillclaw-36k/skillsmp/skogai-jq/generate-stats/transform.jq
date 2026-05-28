# Generate statistics for numeric array (min, max, avg, sum, count)
# Usage: jq -f generate-stats/transform.jq --arg array_path "items" [--arg field "value"] input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "items" or "data.scores")
#   field: optional field to extract from array of objects before calculating stats
#
# Input: JSON object containing an array at the specified path
# Output: object with stats {min, max, avg, sum, count}, or null if path doesn't exist or value is not an array

# Split path into array of keys and get array value
($array_path | split(".")) as $keys |
getpath($keys) as $array |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  null
elif $array | length == 0 then
  {
    min: null,
    max: null,
    avg: null,
    sum: null,
    count: 0
  }
else
  # Extract field if specified, otherwise use array values directly
  (if ($ARGS.named.field // "") != "" then
    $array | map(.[$ARGS.named.field])
  else
    $array
  end) as $values |

  # Filter out non-numeric values (null, strings, booleans, objects, arrays)
  ($values | map(select(type == "number"))) as $numeric_values |

  # If no numeric values after filtering, return null stats
  if $numeric_values | length == 0 then
    {
      min: null,
      max: null,
      avg: null,
      sum: null,
      count: 0
    }
  else
    {
      min: ($numeric_values | min),
      max: ($numeric_values | max),
      avg: (($numeric_values | add) / ($numeric_values | length)),
      sum: ($numeric_values | add),
      count: ($numeric_values | length)
    }
  end
end
