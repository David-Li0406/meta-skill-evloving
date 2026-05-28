# Check if value at path is an empty string ""
# Usage: jq -f is-empty-string/transform.jq --arg path "user.name" input.json
#
# Arguments:
#   path: dot-separated path to field to check (e.g., "user.name")
#
# Input: any JSON object
# Output: boolean (true if value is exactly "", false otherwise)

# Split path into array of keys and get value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true only if value is string type AND equals empty string
if ($value | type) == "string" then
  $value == ""
else
  false
end
