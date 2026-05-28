# Flatten nested arrays at path
# Usage: jq -f array-flatten/transform.jq --arg path "items" [--arg depth "1"] input.json
#
# Arguments:
#   path: dot-separated path to array field (e.g., "data.items")
#   depth: optional flattening depth (default: 1, use "-1" for complete flatten)
#
# Input: any JSON object containing array at path
# Output: object with flattened array at path, or original object if path doesn't exist or is not an array

def flatten_depth(d):
  if d == 0 then
    .
  elif type != "array" then
    .
  else
    reduce .[] as $item ([]; . + (if ($item | type) == "array" and d != 0 then ($item | flatten_depth(d - 1)) else [$item] end))
  end;

# Split path into array of keys and get array value
($path | split(".")) as $keys |
getpath($keys) as $array |

# Parse depth (default to 1, -1 means infinite)
(($ARGS.named.depth // "1") | tonumber) as $depth |

# Type-check: ensure field is an array before processing
if ($array | type) != "array" then
  .
else
  setpath($keys;
    if $depth == -1 then
      $array | flatten
    else
      $array | flatten_depth($depth)
    end
  )
end
