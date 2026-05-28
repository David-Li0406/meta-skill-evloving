# Extract @mentions from text
# Usage: jq -f extract-mentions/transform.jq --arg path "message" input.json
#
# Arguments:
#   path: dot-separated path to string field (e.g., "user.message")
#
# Input: any JSON object containing string at path
# Output: array of @mentions (strings with @ prefix, e.g., ["@user1", "@user2"])

# Split path into array of keys and get string value
($path | split(".")) as $keys |
getpath($keys) as $value |

# Extract mentions or return empty array
if $value != null and ($value | type) == "string" then
  try (
    [$value | scan("@\\w+")]
  ) catch []
else
  []
end
