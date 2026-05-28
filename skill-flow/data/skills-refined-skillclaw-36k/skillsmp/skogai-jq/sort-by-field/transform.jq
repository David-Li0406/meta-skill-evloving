# Sort array of objects by field value
# Usage: jq -f sort-by-field/transform.jq --arg array_path "items" --arg field_name "name" [--arg order "asc"] input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "items" or "data.results")
#   field_name: field name to sort by (supports nested paths with dots)
#   order: sort order - "asc" (ascending, default) or "desc" (descending)
#
# Input: object containing an array at the specified path
# Output: object with sorted array (missing fields and nulls sort together: first in asc, last in desc)

# Parse path and get array
($array_path | split(".")) as $keys |
getpath($keys) as $array |

# Parse field_name for nested access
($field_name | split(".")) as $field_keys |

# Get sort order (default to ascending)
($ARGS.named.order // "asc") as $sort_order |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  .
elif $array | length == 0 then
  .
else
  # Sort the array by field value
  # Use getpath for nested field access
  # Nulls are handled by sort_by (sorts to beginning by default)
  if $sort_order == "desc" then
    setpath($keys; $array | sort_by(getpath($field_keys)) | reverse)
  else
    setpath($keys; $array | sort_by(getpath($field_keys)))
  end
end
