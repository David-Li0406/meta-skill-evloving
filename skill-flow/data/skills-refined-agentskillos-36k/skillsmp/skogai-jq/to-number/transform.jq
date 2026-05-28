# Convert value to number
# Usage: jq -f to-number/transform.jq --arg path "user.age" input.json
#
# Arguments:
#   path: dot-separated path to value to convert (e.g., "user.age")
#
# Input: any JSON object
# Output: object with value at path converted to number
#
# Conversion rules:
#   - number: pass through unchanged
#   - string: parse as number (returns null if invalid)
#   - boolean: true→1, false→0
#   - null (when path exists): returns 0
#   - array/object: returns null
#   - missing (path doesn't exist): returns null

# Split path into array of keys
($path | split(".")) as $keys |

# Check if path exists using reduce pattern (similar to crud-has)
(reduce $keys[] as $key (
  {obj: ., exists: true};
  if .exists then
    if (.obj | type) == "object" and (.obj | has($key)) then
      {obj: .obj[$key], exists: true}
    else
      {obj: null, exists: false}
    end
  else
    .
  end
) | .exists) as $path_exists |

# Get the value at path
getpath($keys) as $value |

# Determine the converted value based on type
(if $path_exists | not then
  # Path doesn't exist - return null
  null
elif $value == null then
  # Path exists but value is null - convert to 0
  0
else
  ($value | type) as $vtype |

  if $vtype == "number" then
    $value
  elif $vtype == "string" then
    try ($value | tonumber) catch null
  elif $vtype == "boolean" then
    if $value then 1 else 0 end
  else
    null
  end
end) as $converted |

# Set the converted value back at the path
setpath($keys; $converted)
