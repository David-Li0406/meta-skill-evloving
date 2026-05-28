# Filter array items where a specified field matches a regex pattern
# Usage: jq -f filter-by-pattern/transform.jq --arg array_path "items" --arg field_name "email" --arg pattern "^[a-z]+@" input.json
#
# Arguments:
#   array_path: dot-separated path to the array field (e.g., "data.items")
#   field_name: name of the field within array items to test against pattern
#   pattern: regex pattern to test against (e.g., "^[0-9]+$", "[a-z]+")
#
# Input: object containing an array at the specified path
# Output: object with filtered array (only items where field matches pattern)

# Split path into array of keys
($array_path | split(".")) as $keys |

# Get the array from the specified path
getpath($keys) as $array |

# If array exists and is an array, filter it; otherwise return original
if ($array | type) == "array" then
  setpath(
    $keys;
    $array | map(
      select(
        if has($field_name) and (.[$field_name] | type) == "string" then
          try (.[$field_name] | test($pattern)) catch false
        else
          false
        end
      )
    )
  )
else
  .
end
