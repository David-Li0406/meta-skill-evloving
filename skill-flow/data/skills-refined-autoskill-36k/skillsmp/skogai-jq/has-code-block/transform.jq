# Check if string contains code blocks (``` delimited)
# Usage: jq -f has-code-block/transform.jq --arg path "content" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "data.content")
#
# Input: any JSON object containing string at path
# Output: boolean (true if code blocks found, false otherwise)

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true if value exists, is a string, and contains code blocks
if $value != null and ($value | type) == "string" then
  try (
    $value | test("```")
  ) catch false
else
  false
end
