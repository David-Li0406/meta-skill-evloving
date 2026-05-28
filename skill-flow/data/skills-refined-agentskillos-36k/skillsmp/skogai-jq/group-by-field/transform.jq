# Group array of objects by field value, returning object with grouped arrays
# Usage: jq -f group-by-field/transform.jq --arg array_path "items" --arg field_name "status" input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "data.items")
#   field_name: field name to group by (supports nested paths with dot notation)
#
# Input: any JSON object containing array at path
# Output: object with arrays grouped by field value, or null if path doesn't exist or value is not an array

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

  # Add grouping key to each object, handling missing fields
  $array | map(
    . as $item |
    getpath($field_keys) as $val |
    . + {
      __group_key: (
        if $val == null then "null"
        elif ($val | type) == "string" then $val
        elif ($val | type) == "number" then ($val | tostring)
        elif ($val | type) == "boolean" then ($val | tostring)
        else ($val | tostring)
        end
      )
    }
  ) |

  # Group by the temporary key
  group_by(.__group_key) |

  # Convert to object keyed by group value
  map({
    key: .[0].__group_key,
    value: map(del(.__group_key))
  }) |
  from_entries
end
