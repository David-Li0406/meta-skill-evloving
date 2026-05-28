# Extract a field from each item in an array
# Usage: jq -f array-map/transform.jq --arg field "fieldname" [--arg array "items"] input.json
#
# Arguments:
#   field: field name to extract from each array item (e.g., "name")
#   array: name of the array field in the input object (optional, defaults to "items")
#
# Input: object containing an array (e.g., {items: [...]})
# Output: array of extracted values

# Get the array field name (default to "items" if not specified)
($ARGS.named.array // "items") as $arrayField |

# Access the array from input and map over each item
# Type-check: ensure field is an array before mapping
(.[$arrayField] // []) |
if type == "array" then
  map(if type == "object" then .[$ARGS.named.field] else null end)
else
  []
end
