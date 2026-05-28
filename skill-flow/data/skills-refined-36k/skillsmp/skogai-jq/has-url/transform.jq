# Check if string at path contains any URLs
# Usage: jq -f has-url/transform.jq --arg path "data" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "content.text")
#
# Input: any JSON object containing string at path
# Output: boolean (true if contains URL, false if no URLs or path doesn't exist/isn't string)

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Return true if string contains URL, false otherwise
if $value != null and ($value | type) == "string" then
  try (
    # Test for URL pattern: http://, https://, ftp://
    $value | test("(?:https?|ftp)://"; "i")
  ) catch false
else
  false
end
