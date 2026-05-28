# Split string at path by delimiter
# Usage: jq -f string-split/transform.jq --arg path "data" --arg delimiter "," input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.name")
#   delimiter: string to split on (e.g., "," or ".")
#
# Input: any JSON object containing string at path
# Output: array of string parts, or null if path doesn't exist

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return array of split parts if value exists and is a string, otherwise null
if $value != null and ($value | type) == "string" then
  $value | split($delimiter)
else
  null
end
