# Join array elements at path into a string with delimiter
# Usage: jq -f string-join/transform.jq --arg path "data" --arg delimiter "," input.json
#
# Arguments:
#   path: dot-separated path to array field (e.g., "items")
#   delimiter: string to join with (e.g., "," or " ")
#
# Input: any JSON object containing array at path
# Output: joined string, or null if path does not exist or is not an array

# Split path into array of keys and get array value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return joined string if value exists and is an array, otherwise null
if $value != null and ($value | type) == "array" then
  $value | map(tostring) | join($delimiter)
else
  null
end
