# Count occurrences of each unique value in an array of objects grouped by field
# Usage: jq -f count-by-field/transform.jq --arg array_path "items" --arg field_name "status" input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "data.items")
#   field_name: field name to group by and count (supports nested paths with dot notation)
#
# Input: any JSON object containing array at path
# Output: object with counts keyed by unique field values, or null if path doesn't exist or value is not an array

# Split path into array of keys and get array value
($array_path | split(".")) as $keys |
getpath($keys) as $array |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  null
elif $array | length == 0 then
  {}
else
  # Split field_name into nested path if needed
  ($field_name | split(".")) as $field_keys |

  # Extract field values, handling missing fields gracefully
  $array | map(
    getpath($field_keys) as $val |
    if $val == null then "null" else $val end
  ) |

  # Group by value and count occurrences
  group_by(.) |
  map({
    key: (.[0] | if type == "string" and . == "null" then "null" else tostring end),
    value: length
  }) |
  from_entries
end
