# Remove duplicate values from an array
# Usage: jq -f array-unique/transform.jq [--arg array "items"] input.json
#
# Arguments:
#   array: name of the array field in the input object (optional, defaults to "items")
#
# Input: object containing an array (e.g., {items: [...]})
# Output: object with deduplicated array

# Get the array field name (default to "items" if not specified)
($ARGS.named.array // "items") as $arrayField |

# Get the array value
getpath([$arrayField]) as $arrayValue |

# Type-check: ensure field is an array before processing
if ($arrayValue | type) == "array" then
  setpath(
    [$arrayField];
    $arrayValue | unique
  )
else
  .
end
