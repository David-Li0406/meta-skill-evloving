# Filter array items by field value
# Usage: jq -f array-filter/transform.jq --arg array_field "items" --arg field "status" --arg value "active" input.json
#
# Arguments:
#   array_field: name of the field containing the array to filter
#   field: name of the field within array items to check
#   value: value to match against
#
# Input: object containing an array (e.g., {"items": [...]})
# Output: object with filtered array

# Get the array from the specified field
getpath([$array_field]) as $array |

# If array exists and is an array, filter it; otherwise return original
if ($array | type) == "array" then
  setpath(
    [$array_field];
    $array | map(select(.[$field] == (try ($value | fromjson) catch $value)))
  )
else
  .
end
