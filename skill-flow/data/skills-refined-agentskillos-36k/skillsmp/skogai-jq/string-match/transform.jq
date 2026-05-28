# Test if string at path matches a regex pattern
# Usage: jq -f string-match/transform.jq --arg path "data" --arg pattern "^[a-z]+$" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.email")
#   pattern: regex pattern to test against (e.g., "^[0-9]+$")
#
# Input: any JSON object containing string at path
# Output: boolean (true if matches, false if doesn't match or path doesn't exist/isn't string)

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true/false based on pattern match
if $value != null and ($value | type) == "string" then
  try (
    $value | test($pattern)
  ) catch false
else
  false
end
