# Trim whitespace from start and end of string at path
# Usage: jq -f string-trim/transform.jq --arg path "data.message" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.name")
#
# Input: any JSON object containing string at path
# Output: object with trimmed string, or original object if path doesn't exist/is not a string

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Only trim if value exists and is a string
if $value != null and ($value | type) == "string" then
  setpath($keys; ($value | gsub("^\\s+|\\s+$"; "")))
else
  .
end
