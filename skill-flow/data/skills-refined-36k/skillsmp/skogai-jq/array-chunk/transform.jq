# Split array into chunks of specified size
# Usage: jq -f array-chunk/transform.jq --arg array_path "items" --arg size "3" input.json
#
# Arguments:
#   array_path: dot-separated path to array field (e.g., "items" or "data.items")
#   size: chunk size (must be positive integer)
#
# Input: any JSON object containing array at path
# Output: object with array field replaced by array of chunks, or object unchanged if path doesn't exist or value is not an array

# Split path into array of keys and get array value
($array_path | split(".")) as $keys |
getpath($keys) as $array |

# Type-check: ensure field is an array and size is valid before processing
if ($array | type) != "array" then
  .
elif ($size | tonumber) <= 0 then
  .
elif $array | length == 0 then
  setpath($keys; [])
else
  ($size | tonumber) as $chunk_size |
  # Build chunks using range and slicing
  ([range(0; $array | length; $chunk_size) as $i | $array[$i:$i+$chunk_size]]) as $chunks |
  setpath($keys; $chunks)
end
